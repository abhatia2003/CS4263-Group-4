"""
Scorer for the meal planning project. Same script checks the CSP plans and the LLM plans.

Reads the puzzle json + dishes.json directly (doesn't use the CSP code) and writes
one json report per run.

Run files can be .json or .txt, raw LLM text is fine, it just grabs the first {...} block.
Name them puzzle__label__run, e.g. hard_01__baseline__run3.json
CSP files (easy_01.solution.json) get labelled "csp" automatically.

A run counts as "declared infeasible" if it has "status": "infeasible" (or unsolvable /
no_solution) or "infeasible": true. For impossible puzzles put "difficulty": "impossible"
in the puzzle json.

  python scorer.py --puzzle-dir puzzles --menu dishes.json --plan-dir results --out reports_csp
  python scorer.py --puzzle-dir puzzles --menu dishes.json --plan-dir llm_runs --out reports_llm
  python scorer.py --summarise reports_csp reports_llm

The last command prints a summary and writes run_scores.csv (one row per run),
results.md (same thing as tables), summary.csv and constraint_rates.csv.
"""

"""
input:
- puzzles/*.json (with daily and weekly constraints)
- dishes.json (menu)
- results/ (csp output) or llm_runs/ (llm output)
objectivity: does not rely on the CSP code, just checks the constraints and computes the soft penalty

segments:
- loading -> loads menu and each run, parses the plan into 7x3 days
- reading the answer -
"""
import argparse
import csv
import glob
import json
import os
import re
from collections import Counter, defaultdict

EPS = 1e-9
INFEASIBLE = {"infeasible", "unsolvable", "no_solution", "no solution", "impossible"}
EXTRA_KEYS = ["tokens", "time_s", "rounds"]  # optional, copied from the run file if there


def load_menu(path):
    with open(path) as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "dishes" in raw:
        raw = raw["dishes"]
    if isinstance(raw, list):
        raw = {d.get("dish_id") or d.get("id"): d for d in raw}
    return {str(k): dict(v) for k, v in raw.items()}


def load_run(path):
    with open(path) as f:
        text = f.read()
    try:
        return json.loads(text)
    except ValueError:
        pass
    # llm output with extra text around the json
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except ValueError:
            pass
    return None


def get_days(plan):
    # needs 7 days with exactly 3 dishes each, otherwise None
    if not isinstance(plan, dict):
        return None
    days = []
    for d in range(1, 8):
        v = plan.get(f"day_{d}")
        if not isinstance(v, list) or len(v) != 3:
            return None
        days.append([str(x) for x in v])
    return days


def in_bounds(v, lo, hi):
    if lo is not None and v < lo - EPS:
        return False
    if hi is not None and v > hi + EPS:
        return False
    return True


def soft_penalty(puzzle, menu, ids):
    # same as the csp: scale each attribute over the mains only, times the weight
    mains = [d for d in menu.values() if d.get("item_type") == "main"]
    total = 0.0
    for direction, items in puzzle.get("objective", {}).items():
        for attr, w in items.items():
            vals = [float(d[attr]) for d in mains]
            lo, hi = min(vals), max(vals)
            for i in ids:
                x = (float(menu[i][attr]) - lo) / ((hi - lo) or 1)
                total += w * (x if direction == "minimize" else 1 - x)
    return total


def score(puzzle, menu, run, run_id=""):
    extra = {k: run[k] for k in EXTRA_KEYS if isinstance(run, dict) and k in run}

    declared = False
    plan = None
    if isinstance(run, dict):
        declared = str(run.get("status", "")).lower() in INFEASIBLE or run.get("infeasible") is True
        plan = run.get("plan", run)
    days = None if declared else get_days(plan)

    expect_feasible = puzzle.get("difficulty") != "impossible" and puzzle.get("feasible") is not False

    checks = {}      # constraint name -> passed?
    violations = []

    def check(name, ok, **info):
        checks[name] = checks.get(name, True) and ok
        if not ok:
            violations.append({"type": name, **info})

    daily_totals = []
    weekly_totals = {}

    if days is None and not declared:
        violations.append({"type": "not_delivered", "detail": "no parseable 7x3 plan"})

    if days:
        # register every constraint first so a pass still shows up in the pass rates
        for name in ["known_ids", "mains_only", "no_repeat"]:
            checks[name] = True
        if puzzle.get("min_store_rating") is not None:
            checks["store_rating"] = True
        for key in ["daily", "weekly", "daily_presence", "weekly_presence"]:
            for attr in puzzle.get(key, {}):
                checks[f"{key}:{attr}"] = True

        flat = [i for d in days for i in d]
        for di, d in enumerate(days, 1):
            for i in d:
                check("known_ids", i in menu, day=di, dish=i)

        # everything below only uses dishes that exist in the menu
        known = [[i for i in d if i in menu] for d in days]

        min_rating = puzzle.get("min_store_rating")
        for di, d in enumerate(known, 1):
            for i in d:
                check("mains_only", menu[i].get("item_type") == "main",
                      day=di, dish=i, item_type=menu[i].get("item_type"))
                if min_rating is not None:
                    check("store_rating", float(menu[i]["store_rating"]) >= min_rating - EPS,
                          day=di, dish=i, required=min_rating, actual=menu[i]["store_rating"])

        cap = puzzle.get("max_times_per_dish_per_week", 1)
        for dish, n in Counter(flat).items():
            check("no_repeat", n <= cap, dish=dish, count=n, max=cap)

        for di, d in enumerate(known, 1):
            totals = {}
            for attr, (lo, hi) in puzzle.get("daily", {}).items():
                v = round(sum(float(menu[i][attr]) for i in d), 4)
                totals[attr] = v
                check(f"daily:{attr}", in_bounds(v, lo, hi), day=di, min=lo, max=hi, actual=v)
            for attr, need in puzzle.get("daily_presence", {}).items():
                have = sum(1 for i in d if menu[i].get(attr))
                check(f"daily_presence:{attr}", have >= need, day=di, required=need, actual=have)
            daily_totals.append(totals)

        week = [i for d in known for i in d]
        for attr, (lo, hi) in puzzle.get("weekly", {}).items():
            v = round(sum(float(menu[i][attr]) for i in week), 4)
            weekly_totals[attr] = v
            check(f"weekly:{attr}", in_bounds(v, lo, hi), min=lo, max=hi, actual=v)
        for attr, need in puzzle.get("weekly_presence", {}).items():
            have = sum(1 for i in week if menu[i].get(attr))
            weekly_totals["count_" + attr] = have
            check(f"weekly_presence:{attr}", have >= need, required=need, actual=have)

    valid = days is not None and all(checks.values())
    correct = valid if expect_feasible else declared

    if declared:
        outcome = "declared_infeasible"
    elif days is None:
        outcome = "not_delivered"
    else:
        outcome = "valid" if valid else "invalid"

    penalty = None
    if valid:
        penalty = round(soft_penalty(puzzle, menu, [i for d in days for i in d]), 4)

    report = {
        "run_id": run_id,
        "puzzle_id": puzzle["id"],
        "difficulty": puzzle.get("difficulty"),
        "expect_feasible": expect_feasible,
        "outcome": outcome,
        "delivered": declared or days is not None,
        "valid": valid,
        "correct": correct,
        "violation_count": len(violations),
        "violation_types": dict(Counter(v["type"] for v in violations)),
        "violations": violations,
        "checks": checks,
        "soft_penalty": penalty,
        "daily_totals": daily_totals,
        "weekly_totals": weekly_totals,
    }
    report.update(extra)
    return report


def run_batch(args):
    menu = load_menu(args.menu)
    os.makedirs(args.out, exist_ok=True)

    puzzles = {}
    for p in glob.glob(os.path.join(args.puzzle_dir, "*.json")):
        with open(p) as f:
            j = json.load(f)
        if not isinstance(j, dict) or "daily" not in j:
            print("skipping, not a puzzle:", p)
            continue
        j.setdefault("id", os.path.splitext(os.path.basename(p))[0])
        puzzles[j["id"]] = j

    files = glob.glob(os.path.join(args.plan_dir, "*.json")) + glob.glob(os.path.join(args.plan_dir, "*.txt"))
    for path in sorted(files):
        run_id = os.path.splitext(os.path.basename(path))[0]
        pid = run_id.split("__")[0].split(".")[0]
        if pid not in puzzles:
            print("skipping, no puzzle for:", path)
            continue

        run = load_run(path)
        rep = score(puzzles[pid], menu, run, run_id)

        parts = run_id.split("__")
        if ".solution" in run_id:
            rep["safeguard"] = "csp"
            if isinstance(run, dict):
                rep["csp_status"] = run.get("status")
                rep["time_s"] = run.get("solve_time_s")
                if run.get("penalty") is not None and rep["soft_penalty"] is not None:
                    rep["penalty_matches_file"] = abs(run["penalty"] - rep["soft_penalty"]) < 1e-3
        else:
            rep["safeguard"] = parts[1] if len(parts) > 1 else "none"

        with open(os.path.join(args.out, run_id + ".report.json"), "w") as f:
            json.dump(rep, f, indent=2)
        print(f"{run_id}: {rep['outcome']}, {rep['violation_count']} violations, correct={rep['correct']}")


def avg(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs) / len(xs) if xs else None


def fmt(x, nd=1):
    return "-" if x is None else f"{x:.{nd}f}"


def fmt_cell(x):
    if isinstance(x, float):
        return f"{x:.2f}"
    return "" if x is None else str(x)


def run_number(run_id):
    m = re.search(r"run(\d+)", run_id)
    return int(m.group(1)) if m else 0


def describe(v):
    # turn a violation into a short sentence
    t = v["type"]
    where = f"day {v['day']}: " if "day" in v else ""
    if t == "not_delivered":
        return "no parseable plan"
    if t == "known_ids":
        return f"{where}{v['dish']} is not in the menu"
    if t == "mains_only":
        return f"{where}{v['dish']} is a {v['item_type']}, not a main"
    if t == "store_rating":
        return f"{where}{v['dish']} rating {v['actual']} is below {v['required']}"
    if t == "no_repeat":
        return f"{v['dish']} used {v['count']} times (max {v['max']})"
    name = t.split(":")[-1]
    if t.startswith(("daily_presence", "weekly_presence")):
        return f"{where}{name} in {v['actual']} dishes (need {v['required']})"
    # daily / weekly ranges
    if v.get("max") is not None and v["actual"] > v["max"]:
        return f"{where}{name} {v['actual']:g} is over the max {v['max']:g}"
    return f"{where}{name} {v['actual']:g} is under the min {v['min']:g}"


def summarise(folders):
    reports = []
    for folder in folders:
        for p in glob.glob(os.path.join(folder, "*.report.json")):
            with open(p) as f:
                reports.append(json.load(f))

    groups = defaultdict(list)
    for r in reports:
        groups[(r.get("safeguard", "none"), r.get("difficulty"))].append(r)

    rows = []
    constraint_rows = []
    for (sg, diff), rs in sorted(groups.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        n = len(rs)
        plans = [r for r in rs if r["outcome"] in ("valid", "invalid")]
        rows.append([
            sg, diff, n,
            100 * sum(r["delivered"] for r in rs) / n,
            100 * sum(r["correct"] for r in rs) / n,
            sum(1 for r in plans if not r["expect_feasible"]),
            sum(1 for r in rs if r["expect_feasible"] and r["outcome"] == "declared_infeasible"),
            avg([r["violation_count"] for r in plans]),
            avg([r["soft_penalty"] for r in rs if r["valid"]]),
            avg([r.get("tokens") for r in rs]),
            avg([r.get("time_s") for r in rs]),
        ])
        for c in sorted({c for r in plans for c in r["checks"]}):
            res = [r["checks"][c] for r in plans if c in r["checks"]]
            constraint_rows.append([sg, diff, c, 100 * sum(res) / len(res), len(res)])

    print("pass% = valid plan (feasible puzzles) or declared infeasible (impossible puzzles)")
    print("FalseF = plan given for an impossible puzzle, FalseI = feasible puzzle declared infeasible\n")
    print(f"{'safeguard':<20}{'diff':<12}{'runs':>5}{'deliv%':>8}{'pass%':>7}{'FalseF':>8}{'FalseI':>8}"
          f"{'viol':>7}{'penalty':>9}{'tokens':>9}{'time_s':>8}")
    for r in rows:
        print(f"{r[0]:<20}{str(r[1]):<12}{r[2]:>5}{r[3]:>7.0f}%{r[4]:>6.0f}%{r[5]:>8}{r[6]:>8}"
              f"{fmt(r[7], 2):>7}{fmt(r[8], 2):>9}{fmt(r[9], 0):>9}{fmt(r[10], 1):>8}")

    print("\nconstraints that didn't always pass (over delivered plans):")
    for sg, diff in sorted({(r[0], r[1]) for r in constraint_rows}, key=str):
        bad = [f"{c[2]} {c[3]:.0f}%" for c in constraint_rows
               if c[0] == sg and c[1] == diff and c[3] < 100]
        if bad:
            print(f"  {sg}/{diff}: " + ", ".join(bad))

    summary_head = ["method", "difficulty", "runs", "delivery_pct", "final_pass_pct", "false_feasible",
                    "false_infeasible", "avg_violations", "avg_penalty_valid", "avg_tokens", "avg_time_s"]
    with open("summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(summary_head)
        w.writerows(rows)
    with open("constraint_rates.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["method", "difficulty", "constraint", "pass_pct", "n_plans"])
        w.writerows(constraint_rows)

    # one row per run, this is the file to share
    run_head = ["puzzle", "difficulty", "method", "run", "result", "outcome", "num_violations",
                "penalty", "what_went_wrong"]
    run_rows = []
    for r in sorted(reports, key=lambda r: (r["puzzle_id"], str(r.get("safeguard")), run_number(r["run_id"]))):
        if r["correct"]:
            result = "PASS"
        else:
            result = "FAIL"
        details = "; ".join(describe(v) for v in r["violations"])
        if r["outcome"] == "declared_infeasible" and not r["expect_feasible"]:
            details = "correctly said no solution"
        elif r["outcome"] == "declared_infeasible":
            details = "said infeasible but a solution exists"
        elif not r["expect_feasible"] and r["outcome"] in ("valid", "invalid"):
            details = "gave a plan for an impossible puzzle"
        run_rows.append([r["puzzle_id"], r["difficulty"], r.get("safeguard", "none"), run_number(r["run_id"]),
                         result, r["outcome"], r["violation_count"], r["soft_penalty"] if r["soft_penalty"] is not None else "",
                         details])
    with open("run_scores.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(run_head)
        w.writerows(run_rows)

    with open("results.md", "w") as f:
        f.write("# Scorer results\n\n")
        f.write("PASS = valid plan on a feasible puzzle, or 'no solution' on an impossible puzzle.\n\n")
        f.write("## Summary by method\n\n")
        f.write("| " + " | ".join(summary_head) + " |\n|" + "---|" * len(summary_head) + "\n")
        for r in rows:
            f.write("| " + " | ".join(fmt_cell(x) for x in r) + " |\n")
        f.write("\n## Every run\n\n")
        f.write("| " + " | ".join(run_head) + " |\n|" + "---|" * len(run_head) + "\n")
        for r in run_rows:
            f.write("| " + " | ".join(fmt_cell(x) for x in r) + " |\n")
        f.write("\n## Constraint pass rates\n\n")
        f.write("| method | difficulty | constraint | pass % | plans |\n|---|---|---|---|---|\n")
        for r in constraint_rows:
            f.write("| " + " | ".join(fmt_cell(x) for x in r) + " |\n")
    print("\nsaved run_scores.csv, results.md, summary.csv and constraint_rates.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--puzzle-dir")
    ap.add_argument("--plan-dir")
    ap.add_argument("--menu", default="dishes.json")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--summarise", nargs="+", metavar="REPORT_DIR")
    ap.add_argument("--puzzle")
    ap.add_argument("--plan")
    args = ap.parse_args()

    if args.summarise:
        summarise(args.summarise)
    elif args.puzzle_dir and args.plan_dir:
        run_batch(args)
    elif args.puzzle and args.plan:
        with open(args.puzzle) as f:
            puzzle = json.load(f)
        puzzle.setdefault("id", os.path.splitext(os.path.basename(args.puzzle))[0])
        rep = score(puzzle, load_menu(args.menu), load_run(args.plan), os.path.basename(args.plan))
        print(json.dumps(rep, indent=2))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
