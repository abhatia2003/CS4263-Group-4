import time

from ortools.sat.python import cp_model

from .data import COST_SCALE, bounds, dish_costs, eligible_dishes, to_int
from .validate import check_plan, penalty

STATUS = {
    cp_model.OPTIMAL: 'OPTIMAL',
    cp_model.FEASIBLE: 'FEASIBLE',
    cp_model.INFEASIBLE: 'INFEASIBLE',
    cp_model.UNKNOWN: 'UNKNOWN',
    cp_model.MODEL_INVALID: 'MODEL_INVALID',
}


def solve(puzzle, menu, time_limit=60, workers=8):
    start = time.perf_counter()
    costs = dish_costs(puzzle, menu)
    domain = sorted(eligible_dishes(puzzle, menu), key=lambda dish: (costs[dish['dish_id']], dish['dish_id']))
    result = {'id': puzzle['id'], 'eligible_dishes': len(domain)}

    days, meals = puzzle['days'], puzzle['meals_per_day']
    if not domain:
        return finish(result, 'INFEASIBLE', None, None, start, proved_by='no dish meets the unary constraints')

    model, slots, picks = build_model(puzzle, domain, costs)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = workers
    solver.parameters.random_seed = 0
    status = STATUS[solver.Solve(model)]

    plan = None
    if status in ('OPTIMAL', 'FEASIBLE'):
        plan = [[domain[solver.Value(slots[d][m])]['dish_id'] for m in range(meals)] for d in range(days)]
    bound = solver.BestObjectiveBound() / COST_SCALE if status in ('OPTIMAL', 'FEASIBLE') else None
    result['branches'] = solver.NumBranches()
    result['conflicts'] = solver.NumConflicts()
    return finish(result, status, plan, bound, start, puzzle=puzzle, menu=menu)


def build_model(puzzle, domain, costs):
    days, meals = puzzle['days'], puzzle['meals_per_day']
    max_uses = puzzle['max_times_per_dish_per_week']
    n = len(domain)
    model = cp_model.CpModel()

    slots = [[model.NewIntVar(0, n - 1, f'slot_d{d + 1}_m{m + 1}') for m in range(meals)] for d in range(days)]
    picks = {}
    for d in range(days):
        for m in range(meals):
            row = [model.NewBoolVar(f'pick_d{d + 1}_m{m + 1}_{dish["dish_id"]}') for dish in domain]
            model.AddExactlyOne(row)
            model.Add(slots[d][m] == sum(i * pick for i, pick in enumerate(row)))
            for i, pick in enumerate(row):
                picks[d, m, i] = pick

    flat = [slot for day in slots for slot in day]
    if max_uses == 1:
        model.AddAllDifferent(flat)
    for i in range(n):
        model.Add(sum(picks[d, m, i] for d in range(days) for m in range(meals)) <= max_uses)

    for d in range(days):
        for m in range(meals - 1):
            if max_uses == 1:
                model.Add(slots[d][m] < slots[d][m + 1])
            else:
                model.Add(slots[d][m] <= slots[d][m + 1])
    for d in range(days - 1):
        model.Add(slots[d][0] <= slots[d + 1][0])

    def total(attr, day_range):
        return sum(to_int(domain[i][attr]) * picks[d, m, i] for d in day_range for m in range(meals) for i in range(n))

    def count(flag, day_range):
        return sum(picks[d, m, i] for d in day_range for m in range(meals) for i in range(n) if domain[i][flag])

    for d in range(days):
        for attr, bound in puzzle.get('daily', {}).items():
            add_range(model, total(attr, [d]), bound)
        for flag, needed in puzzle.get('daily_presence', {}).items():
            model.Add(count(flag, [d]) >= needed)
    for attr, bound in puzzle.get('weekly', {}).items():
        add_range(model, total(attr, range(days)), bound)
    for flag, needed in puzzle.get('weekly_presence', {}).items():
        model.Add(count(flag, range(days)) >= needed)

    model.Minimize(sum(round(costs[domain[i]['dish_id']] * COST_SCALE) * pick for (d, m, i), pick in picks.items()))
    return model, slots, picks


def add_range(model, expr, bound):
    lo, hi = bounds(bound)
    if lo is not None:
        model.Add(expr >= lo)
    if hi is not None:
        model.Add(expr <= hi)


def finish(result, status, plan, bound, start, puzzle=None, menu=None, proved_by=None):
    result['status'] = status
    result['solve_time_s'] = round(time.perf_counter() - start, 2)
    result['plan'] = None if plan is None else {f'day_{d + 1}': day for d, day in enumerate(plan)}
    result['penalty'] = None if plan is None else round(penalty(puzzle, menu, plan), 6)
    result['objective_bound'] = None if bound is None else round(bound, 6)

    result['validation_failures'] = [] if plan is None else check_plan(puzzle, menu, plan)
    if proved_by:
        result['proved_by'] = proved_by
    elif status == 'INFEASIBLE':
        result['proved_by'] = 'CP-SAT exhaustive search'
    return result
