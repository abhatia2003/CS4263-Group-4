import json
import time
from pathlib import Path

from src.data.puzzle import Puzzle
from src.model.builder import Builder
from src.output.plan import Plan
from src.solver.cop_solver import COPSolver
from src.evaluation.validator import validate
from src.output.writer import write_result

ROOT = Path(__file__).resolve().parents[1]
PUZZLE_DIR = ROOT / 'puzzles'
SLOT_MODEL_THRESHOLD = 5000
TIME_LIMIT = 10


def solve_puzzle(path):
    puzzle = Puzzle.create_puzzle(path)
    menu = puzzle.menu
    builder = Builder(puzzle, menu)
    start = time.perf_counter()
    day_cop = builder.build_day_cop()
    build_time = time.perf_counter() - start

    if len(day_cop.domains[0]) > SLOT_MODEL_THRESHOLD:
        model, problem = 'slot', builder.build_cop()
        solver = COPSolver(time_limit=TIME_LIMIT, order_by_cost=True)
    else:
        model, problem = 'day', day_cop
        solver = COPSolver(time_limit=TIME_LIMIT, order_by_cost=False)
    plan = solver.solve(problem)
    solve_time = build_time + solver.solve_time

    slot_cop = builder.build_cop()
    if plan.is_valid():
        failures = validate(puzzle, plan, menu)
        penalty = slot_cop.total_penalty(plan.to_assignment(menu))
    else:
        failures = []
        penalty = None

    with open(PUZZLE_DIR / f'{puzzle.id}.solution.json', 'r', encoding='utf-8') as f:
        expected = Plan.load_plan(json.load(f))
    expected_penalty = slot_cop.total_penalty(expected.to_assignment(menu)) if expected.is_valid() else None

    write_result(puzzle.id, solver.status, len(builder.eligible_dishes()), solve_time, plan, penalty)
    return {
        'id': puzzle.id,
        'model': model,
        'status': solver.status,
        'valid': plan.is_valid() and not failures,
        'time': solve_time,
        'penalty': penalty,
        'expected_penalty': expected_penalty,
    }


def format_number(value):
    return '-' if value is None else f'{value:.4f}'


def main():
    paths = sorted(path for path in PUZZLE_DIR.glob('*.json') if not path.name.endswith('.solution.json'))
    print(f"{'puzzle':<9} {'model':<5} {'status':<11} {'valid':<6} {'time_s':>7} {'penalty':>9} {'expected':>9}")
    for path in paths:
        row = solve_puzzle(path)
        print(f"{row['id']:<9} {row['model']:<5} {row['status']:<11} {str(row['valid']):<6} {row['time']:>7.2f} "
              f"{format_number(row['penalty']):>9} {format_number(row['expected_penalty']):>9}")


if __name__ == '__main__':
    main()