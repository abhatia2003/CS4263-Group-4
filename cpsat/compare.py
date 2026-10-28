"""Check the project solver's answers (results/*.solution.json) against CP-SAT."""
import argparse
import json

from .data import ROOT, load_puzzle, puzzle_paths
from .model import solve
from .validate import check_plan, penalty

# CP-SAT optimises integer costs (each dish penalty rounded to 1e-6), and the project rounds
# penalties to 4 decimal places, so differences below this are not real.
TOLERANCE = 1e-4


def verdict(project, cpsat, puzzle, menu):
    """Return (level, message) for one puzzle. FAIL means an answer is wrong (invalid plan, wrong
    penalty, or a wrong UNSOLVABLE). WARN means the answer is valid but not optimal, or unverified."""
    if cpsat['validation_failures']:
        return 'FAIL', 'CP-SAT plan breaks rules (CP-SAT model bug): ' + '; '.join(cpsat['validation_failures'])

    if project['status'] == 'SOLVABLE':
        plan = [project['plan'][f'day_{d + 1}'] for d in range(len(project['plan']))]
        failures = check_plan(puzzle, menu, plan)
        if failures:
            return 'FAIL', 'project plan breaks rules: ' + '; '.join(failures)
        actual = penalty(puzzle, menu, plan)
        if project.get('penalty') is not None and abs(actual - project['penalty']) > TOLERANCE:
            return 'FAIL', f"project reports penalty {project['penalty']}, plan actually scores {actual:.4f}"
        if cpsat['status'] == 'INFEASIBLE':
            return 'FAIL', 'project plan is valid but CP-SAT says infeasible (CP-SAT model bug)'
        if cpsat['status'] == 'OPTIMAL':
            gap = actual - cpsat['penalty']
            if gap > TOLERANCE:
                return 'WARN', f"valid but not optimal: {actual:.4f} vs optimum {cpsat['penalty']:.4f}"
            if gap < -TOLERANCE:
                return 'FAIL', f"project beats CP-SAT 'optimum' {cpsat['penalty']:.4f} (CP-SAT model bug)"
            return 'OK', 'valid and optimal'
        return 'WARN', f"valid; optimality unverified (CP-SAT {cpsat['status']}, bound {cpsat['objective_bound']})"

    if cpsat['status'] == 'INFEASIBLE':
        return 'OK', 'both say no solution (CP-SAT proved it)'
    if cpsat['status'] in ('OPTIMAL', 'FEASIBLE'):
        return 'FAIL', 'project says no solution, but CP-SAT found one'
    return 'WARN', 'project says no solution; CP-SAT could not decide in time (unverified)'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ids', nargs='*', help='puzzle ids (default: every puzzle)')
    parser.add_argument('--time-limit', type=float, default=60, help='CP-SAT seconds per puzzle (default 60)')
    args = parser.parse_args()

    counts = {'OK': 0, 'WARN': 0, 'FAIL': 0}
    print(f"{'puzzle':<14} {'project':<11} {'cp-sat':<10} {'proj pen':>9} {'cp-sat pen':>10}  verdict")
    for path in puzzle_paths(args.ids):
        result_path = ROOT / 'results' / f'{path.stem}.solution.json'
        if not result_path.exists():
            print(f'{path.stem:<14} no project result; run python -m src.main first')
            continue
        with open(result_path, 'r', encoding='utf-8') as f:
            project = json.load(f)
        puzzle, menu = load_puzzle(path)
        cpsat = solve(puzzle, menu, args.time_limit)
        level, message = verdict(project, cpsat, puzzle, menu)
        counts[level] += 1
        proj_pen = '-' if project.get('penalty') is None else f"{project['penalty']:.4f}"
        cp_pen = '-' if cpsat['penalty'] is None else f"{cpsat['penalty']:.4f}"
        print(f"{path.stem:<14} {project['status']:<11} {cpsat['status']:<10} {proj_pen:>9} {cp_pen:>10}  "
              f"{level:<4} {message}")
    print(f"\nOK {counts['OK']}  WARN {counts['WARN']}  FAIL {counts['FAIL']}")
    raise SystemExit(1 if counts['FAIL'] else 0)


if __name__ == '__main__':
    main()
