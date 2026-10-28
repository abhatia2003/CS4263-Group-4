from collections import Counter

from .data import bounds, dish_costs, to_int


def check_plan(puzzle, menu, plan):

    failures = []
    if len(plan) != puzzle['days']:
        failures.append(f"expected {puzzle['days']} days, got {len(plan)}")
    for d, day in enumerate(plan, 1):
        if len(day) != puzzle['meals_per_day']:
            failures.append(f"day {d}: expected {puzzle['meals_per_day']} dishes, got {len(day)}")
    unknown = [dish_id for day in plan for dish_id in day if dish_id not in menu]
    if unknown:
        return failures + [f'unknown dishes {unknown}']

    min_rating = puzzle.get('min_store_rating')
    for dish_id in {dish_id for day in plan for dish_id in day}:
        dish = menu[dish_id]
        if dish['item_type'] != 'main':
            failures.append(f"{dish_id} is a {dish['item_type']}, not a main")
        if min_rating is not None and dish['store_rating'] < min_rating:
            failures.append(f"{dish_id} store rating {dish['store_rating']} < {min_rating}")

    for dish_id, count in Counter(dish_id for day in plan for dish_id in day).items():
        if count > puzzle['max_times_per_dish_per_week']:
            failures.append(f'{dish_id} used {count} times in the week')

    for d, day in enumerate(plan, 1):
        dishes = [menu[dish_id] for dish_id in day]
        failures += range_failures(f'day {d}', puzzle.get('daily', {}), dishes)
        failures += presence_failures(f'day {d}', puzzle.get('daily_presence', {}), dishes)
    week = [menu[dish_id] for day in plan for dish_id in day]
    failures += range_failures('week', puzzle.get('weekly', {}), week)
    failures += presence_failures('week', puzzle.get('weekly_presence', {}), week)
    return failures


def range_failures(label, rules, dishes):
    failures = []
    for attr, bound in rules.items():
        lo, hi = bounds(bound)
        total = sum(to_int(dish[attr]) for dish in dishes)
        if lo is not None and total < lo:
            failures.append(f'{label}: {attr} {total / 100} < {lo / 100}')
        if hi is not None and total > hi:
            failures.append(f'{label}: {attr} {total / 100} > {hi / 100}')
    return failures


def presence_failures(label, rules, dishes):
    failures = []
    for flag, needed in rules.items():
        count = sum(1 for dish in dishes if dish[flag])
        if count < needed:
            failures.append(f'{label}: {count} dishes with {flag}, need {needed}')
    return failures


def penalty(puzzle, menu, plan):
    costs = dish_costs(puzzle, menu)
    return sum(costs[dish_id] for day in plan for dish_id in day)
