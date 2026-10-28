# CP-SAT reference solver

A second, independent solver for the meal-plan puzzles in `puzzles/`, built on Google's
[OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver) constraint solver.
It exists to check the project solver in `src/`:

1. **Are the project's plans valid?** Every plan is re-checked by `validate.py`.
2. **Is each UNSOLVABLE answer really unsolvable?** CP-SAT runs a complete search and reports
   `INFEASIBLE` only when it has proven that no plan exists.
3. **Are the project's plans optimal?** CP-SAT reports `OPTIMAL` only when it has proven that no
   valid plan has a lower penalty.

The package does not import anything from `src/`. It reads `puzzles/*.json` and `dishes.json`
directly, so a bug in the project's constraint classes cannot leak into the reference answers.

## Setup

```
python -m pip install -r cpsat/requirements.txt
```

This installs `ortools` (pinned to 9.15.6755). Nothing else is needed. All commands below are run from the repository root.

## Usage

Solve puzzles (all of them by default):

```
python -m cpsat.solve                         # every puzzle, 60 s limit each
python -m cpsat.solve hard_01 impossible_02   # selected puzzles
python -m cpsat.solve --time-limit 120        # longer limit per puzzle
```

Each result is written to `cpsat/results/<puzzle>.json` and summarised in a table.

Check the project solver's latest answers (run `python -m src.main` first so `results/` is up to date):

```
python -m cpsat.compare
```

For each puzzle this prints one of:

| Level | Meaning |
|---|---|
| `OK` | The project's answer is valid and optimal, or both solvers agree there is no solution. |
| `WARN` | The project's plan is valid but CP-SAT found a cheaper valid plan, or CP-SAT could not decide in time. |
| `FAIL` | An answer is wrong: the project's plan breaks a rule or its penalty is miscalculated, the project says UNSOLVABLE when a plan exists, or CP-SAT's own plan fails validation. |

The command exits with code 1 if any puzzle is `FAIL`.

## Result statuses

| Status | Meaning |
|---|---|
| `OPTIMAL` | A valid plan, proven to have the lowest possible penalty. |
| `FEASIBLE` | A valid plan, but the time limit ran out before optimality was proven. `objective_bound` is the best proven lower bound on the penalty. |
| `INFEASIBLE` | Proven that no valid plan exists by CP-SAT's complete search. |
| `UNKNOWN` | The time limit ran out before anything was found or proven. |

Every plan CP-SAT returns is re-checked by `validate.py`, which does not use the CP-SAT model.
Any rule it breaks is listed in `validation_failures`, so a mistake in the model shows up as a
failure.

## How it works

### Formulation

| CSP part | In this model |
|---|---|
| Variables | `slot[d][m]`: the dish for meal `m` of day `d`. 21 variables for 7 days x 3 meals. |
| Domains | The eligible dishes: mains from stalls meeting the minimum store rating. |
| Unary constraints | Dish is a main; store rating >= the minimum. Applied by filtering the domain before the model is built (`data.eligible_dishes`). |
| Global constraints | `AllDifferent` over all 21 slots (when each dish may be used once a week). Each dish used at most `max_times_per_dish_per_week` times. Daily and weekly sum ranges. Daily and weekly presence counts. |

Each slot is linked to one true/false variable per dish (`pick[d, m, i]` is true exactly when
`slot[d][m] == i`). This lets the sum constraints and the objective be written as plain linear sums.

Numbers are multiplied by 100 so every sum and bound is an exact integer. This works because every
value in the data has at most 2 decimal places, and `data.to_int` raises an error otherwise.

**Symmetry breaking.** Meals within a day are interchangeable, and so are days, because every day has
the same rules and the penalty does not depend on the day. So the model requires each day's dishes to
be in increasing order and the days to be ordered by their first dish. Any valid plan can be
rearranged to satisfy this, so no solutions are lost, and CP-SAT does not have to search through
rearrangements of the same plan.

### Objective

The penalty is the same as the project's (`src/constraints/soft/optimise_constraint.py`). It is the
sum, over the 21 dishes chosen, of `weight × normalised value`. Values are normalised over all mains
on the menu, and maximised attributes are flipped. This sum is linear in the dish choices, so CP-SAT
minimises it exactly. CP-SAT needs integer coefficients, so each dish's penalty is rounded to 6 decimal places. 
The penalty reported in the results is recomputed from the data without rounding. Over 21 dishes the rounding 
can shift the total by at most about 0.00001, so `compare` treats differences below 0.0001 as equal.

### Search

The search done internally by CP-SAT. It runs several strategies in parallel (8 workers by
default), using clause learning, linear relaxations and large-neighbourhood search. Its search is
complete: given enough time, it either proves the best plan it found is optimal or proves that no
plan exists. 

## Results

Run on 2026-10-28, 60 s limit per puzzle, 8 workers, on a Windows 11 laptop. "Dishes" is the
number of eligible dishes (mains meeting the store rating). "Bound" is CP-SAT's proven lower bound
on the penalty.

| Puzzle | Status | Penalty | Bound | Dishes | Time (s) |
|---|---|---|---|---|---|
| easy_01 | OPTIMAL | 6.7987 | 6.7987 | 83 | 9.6 |
| easy_02 | OPTIMAL | 6.7987 | 6.7987 | 83 | 11.4 |
| easy_03 | OPTIMAL | 6.8201 | 6.8201 | 83 | 23.8 |
| easy_04 | OPTIMAL | 6.7987 | 6.7987 | 82 | 11.8 |
| easy_05 | OPTIMAL | 6.7987 | 6.7987 | 83 | 8.4 |
| easy_06 | OPTIMAL | 6.7987 | 6.7987 | 83 | 13.2 |
| easy_07 | OPTIMAL | 6.7987 | 6.7987 | 83 | 9.0 |
| easy_08 | OPTIMAL | 6.7987 | 6.7987 | 83 | 13.7 |
| easy_09 | OPTIMAL | 6.7987 | 6.7987 | 83 | 7.6 |
| easy_10 | OPTIMAL | 6.2729 | 6.2729 | 83 | 11.9 |
| hard_01 | OPTIMAL | 7.7357 | 7.7357 | 82 | 6.2 |
| hard_02 | OPTIMAL | 8.2262 | 8.2262 | 82 | 19.2 |
| hard_03 | OPTIMAL | 7.4762 | 7.4762 | 82 | 3.7 |
| hard_04 | OPTIMAL | 8.4147 | 8.4147 | 82 | 9.5 |
| hard_05 | OPTIMAL | 6.8942 | 6.8942 | 82 | 12.6 |
| impossible_01 | INFEASIBLE | – | – | 82 | 1.9 |
| impossible_02 | INFEASIBLE | – | – | 82 | 3.1 |
| impossible_03 | INFEASIBLE | – | – | 82 | 6.0 |

Every puzzle finished well within the limit (2 to 24 s). For every OPTIMAL puzzle the proven bound
equals the penalty, so no valid plan is cheaper. Every plan passed validation.

`python -m cpsat.compare` against the project's current `results/` (project run with its 10 s limit):

| Puzzle | Project | Project penalty | CP-SAT optimum | Verdict |
|---|---|---|---|---|
| easy_01–02, 04–09 | SOLVABLE | 7.0576 | 6.7987 | WARN: valid, not optimal |
| easy_03 | SOLVABLE | 7.0671 | 6.8201 | WARN: valid, not optimal |
| easy_10 | SOLVABLE | 6.3084 | 6.2729 | WARN: valid, not optimal |
| hard_01 | SOLVABLE | 7.7574 | 7.7357 | WARN: valid, not optimal |
| hard_02 | SOLVABLE | 8.3333 | 8.2262 | WARN: valid, not optimal |
| hard_03 | SOLVABLE | 7.4762 | 7.4762 | OK |
| hard_04 | SOLVABLE | 8.4147 | 8.4147 | OK |
| hard_05 | SOLVABLE | 7.1203 | 6.8942 | WARN: valid, not optimal |
| impossible_01–03 | UNSOLVABLE | – | INFEASIBLE | OK |

All of the project's plans are valid and its penalties are calculated correctly (0 FAIL). The
"not optimal" verdicts do not depend on trusting CP-SAT: each of the 15 CP-SAT plans passes both
this package's validator and the project's own `src.evaluation.validator`, and the project's own
penalty function gives it the same score. So each one is a concrete, cheaper valid plan.

## How to compare penalty and correctness

A CP-SAT answer and a project answer can be compared on three points. Steps 1 and 2 use only the
project's own code, so they do not depend on trusting CP-SAT.

### 1. Is each plan valid?

Check a plan against the project's hard constraints with the project's own validator. An empty
list means every constraint holds. Run from the repository root:

```python
import json
from pathlib import Path
from src.data.puzzle import Puzzle
from src.evaluation.validator import validate
from src.model.builder import Builder
from src.output.plan import Plan

puzzle_id = 'hard_05'
puzzle = Puzzle.create_puzzle(Path('puzzles') / f'{puzzle_id}.json')
menu = puzzle.menu

def load(path):
    days = json.load(open(path))['plan']
    return Plan(tuple(tuple(days[f'day_{d + 1}']) for d in range(len(days))))

for name, path in [('project', f'results/{puzzle_id}.solution.json'),
                   ('cp-sat', f'cpsat/results/{puzzle_id}.json')]:
    plan = load(path)
    failures = validate(puzzle, plan, menu)
    score = Builder(puzzle, menu).build_cop().total_penalty(plan.to_assignment(menu))
    print(name, 'VALID' if not failures else failures, round(score, 4))
```

### 2. Is each penalty right?

Score both plans with the same function, the project's `total_penalty` above. This needs no trust in
CP-SAT, because the project's own code accepts and scores the plan.

Differences below 0.0001 are rounding: the project stores penalties to 4 decimal places, and CP-SAT
rounds each dish's penalty to 6 decimal places internally.

### 3. Is the answer optimal, or truly unsolvable?

Only CP-SAT can show this, through its status:

- `OPTIMAL` with `objective_bound` equal to `penalty`: CP-SAT has proven that no valid plan is
  cheaper. If the project's score equals this penalty, the project's plan is optimal too.
- `INFEASIBLE`: CP-SAT has proven that no valid plan exists. This backs up a project `UNSOLVABLE`.
  `impossible_puzzles.md` also gives a hand-checkable reason for each impossible puzzle.
- `FEASIBLE` or `UNKNOWN`: the time limit ran out, and nothing is proven.

### Doing all three

`python -m cpsat.compare` runs these checks for every puzzle and prints `OK`, `WARN` or `FAIL`
(see Usage). `plan_comparison.md` in the repository root lists, for each puzzle, both plans side by
side, the dishes that differ, and how much each one adds to the penalty.

## Limitations

- `OPTIMAL` and `INFEASIBLE` are only as trustworthy as CP-SAT, a widely used solver. It does not
  produce a proof that can be checked independently.
- Results depend on the time limit. A puzzle that runs out of time is reported as `FEASIBLE` or
  `UNKNOWN`, never as `OPTIMAL` or `INFEASIBLE`.
- CP-SAT with several workers is not guaranteed to be deterministic. If a puzzle has several
  optimal plans, it may return a different one each run, but always with the same penalty.
