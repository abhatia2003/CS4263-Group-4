import json
import time
from pathlib import Path

from src.data.puzzle import Puzzle
from src.model.builder import Builder
from src.model.day_table import DayTable
from src.output.plan import Plan
from src.solver.day_solver import DaySolver
from src.evaluation.validator import validate
from src.output.writer import write_result

ROOT = Path(__file__).resolve().parents[1]
PUZZLE_DIR = ROOT / 'puzzles'
TIME_LIMIT = 60


def solve_puzzle(path):
    puzzle = Puzzle.create_puzzle(path)
    menu = puzzle.menu
    builder = Builder(puzzle, menu)
    start = time.perf_counter()
    day_cop = builder.build_day_cop()
    table = DayTable(puzzle, day_cop, builder.eligible_dishes())
    build_time = time.perf_counter() - start

    solver = DaySolver(time_limit=TIME_LIMIT)
    plan = solver.solve(table)
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

    write_result(puzzle.id, solver.status, solver.optimal, len(builder.eligible_dishes()), solve_time, plan, penalty)
    return {
        'id': puzzle.id,
        'status': solver.status,
        'optimal': solver.optimal,
        'valid': plan.is_valid() and not failures,
        'time': solve_time,
        'penalty': penalty,
        'expected_penalty': expected_penalty,
    }


def format_number(value):
    return '-' if value is None else f'{value:.4f}'


def main():
    paths = sorted(path for path in PUZZLE_DIR.glob('*.json') if not path.name.endswith('.solution.json'))
    print(f"{'puzzle':<14} {'status':<11} {'optimal':<8} {'valid':<6} {'time_s':>7} {'penalty':>9} {'expected':>9}")
    for path in paths:
        row = solve_puzzle(path)
        print(f"{row['id']:<14} {row['status']:<11} {str(row['optimal']):<8} {str(row['valid']):<6} {row['time']:>7.2f} "
              f"{format_number(row['penalty']):>9} {format_number(row['expected_penalty']):>9}", flush=True)


if __name__ == '__main__':
    main()