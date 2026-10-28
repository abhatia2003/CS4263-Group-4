import argparse
import json

from .data import RESULTS_DIR, load_puzzle, puzzle_paths
from .model import solve


def write(result):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"{result['id']}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    return path


def format_number(value):
    return '-' if value is None else f'{value:.4f}'


def main():
    parser = argparse.ArgumentParser(description='Solve hawker meal-plan puzzles with OR-Tools CP-SAT.')
    parser.add_argument('ids', nargs='*', help='puzzle ids such as hard_01 (default: every puzzle)')
    parser.add_argument('--time-limit', type=float, default=60, help='seconds per puzzle (default 60)')
    parser.add_argument('--workers', type=int, default=8, help='CP-SAT workers (default 8)')
    args = parser.parse_args()

    print(f"{'puzzle':<14} {'status':<10} {'penalty':>9} {'bound':>9} {'dishes':>7} {'time_s':>7}  check")
    for path in puzzle_paths(args.ids):
        puzzle, menu = load_puzzle(path)
        result = solve(puzzle, menu, args.time_limit, args.workers)
        write(result)
        check = 'INVALID: ' + '; '.join(result['validation_failures']) if result['validation_failures'] else 'ok'
        print(f"{result['id']:<14} {result['status']:<10} {format_number(result['penalty']):>9} "
              f"{format_number(result['objective_bound']):>9} {result['eligible_dishes']:>7} {result['solve_time_s']:>7.2f}  {check}")


if __name__ == '__main__':
    main()
