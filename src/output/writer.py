import json
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parents[2] / 'results'


def write_result(puzzle_id, status, eligible_dishes, solve_time, plan, penalty):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        'status': status,
        'eligible_dishes': eligible_dishes,
        'solve_time_s': round(solve_time, 2),
        'plan': plan.parse_plan(),
        'penalty': None if penalty is None else round(penalty, 4),
    }
    path = RESULTS_DIR / f'{puzzle_id}.solution.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    return path