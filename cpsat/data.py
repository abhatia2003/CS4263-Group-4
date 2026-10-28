import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUZZLE_DIR = ROOT / 'puzzles'
RESULTS_DIR = Path(__file__).resolve().parent / 'results'

# Every number in dishes.json and the puzzle files has at most 2 decimal places,
# so multiplying by 100 turns all sums and bounds into exact integers.
SCALE = 100
# Dish penalties are real numbers; CP-SAT needs integer objective coefficients.
COST_SCALE = 10 ** 6


def load_puzzle(path):
    with open(path, 'r', encoding='utf-8') as f:
        puzzle = json.load(f)
    with open(ROOT / puzzle['menu'], 'r', encoding='utf-8') as f:
        menu = json.load(f)
    return puzzle, menu


def puzzle_paths(ids=None):
    paths = sorted(p for p in PUZZLE_DIR.glob('*.json') if not p.name.endswith('.solution.json'))
    if ids:
        paths = [p for p in paths if p.stem in ids]
    return paths


def to_int(value):
    scaled = round(value * SCALE)
    if abs(value * SCALE - scaled) > 1e-6:
        raise ValueError(f'{value} has more than 2 decimal places')
    return scaled


def bounds(bound):
    lo, hi = bound
    return (None if lo is None else to_int(lo)), (None if hi is None else to_int(hi))


def mains(menu):
    return [dish for dish in menu.values() if dish['item_type'] == 'main']


def eligible_dishes(puzzle, menu):
    """Dishes allowed in any slot: mains from stalls meeting the minimum store rating."""
    min_rating = puzzle.get('min_store_rating')
    return [dish for dish in mains(menu) if min_rating is None or dish['store_rating'] >= min_rating]


def dish_costs(puzzle, menu):
    """Penalty of each dish, using the same formula as src/constraints/soft/optimise_constraint.py:
    weight * (value - min) / (max - min) when minimising, weight * (max - value) / (max - min) when
    maximising, with min and max taken over every main on the menu."""
    all_mains = mains(menu)
    terms = [(attr, w, 1) for attr, w in puzzle['objective'].get('minimize', {}).items()]
    terms += [(attr, w, -1) for attr, w in puzzle['objective'].get('maximize', {}).items()]
    costs = {dish_id: 0.0 for dish_id in menu}
    for attr, weight, direction in terms:
        lo = min(dish[attr] for dish in all_mains)
        hi = max(dish[attr] for dish in all_mains)
        for dish_id, dish in menu.items():
            if direction > 0:
                costs[dish_id] += weight * (dish[attr] - lo) / (hi - lo)
            else:
                costs[dish_id] += weight * (hi - dish[attr]) / (hi - lo)
    return costs
