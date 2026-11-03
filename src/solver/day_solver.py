import time

from .solver import Solver
from .cop_solver import TimeLimitReached
from ..output.plan import Plan


class DaySolver(Solver):
    def __init__(self, time_limit=60):
        super().__init__()
        self.time_limit = time_limit

    def _search(self, table):
        self.table = table
        self.start = time.perf_counter()
        self.best_indices = None
        self.best_penalty = float('inf')
        self.solutions_found = 0
        self.nodes = 0
        sums = [0] * len(table.weekly_parameters)
        try:
            self.backtrack(0, 0, 0, 0, sums, list(table.flags_needed), [])
        except TimeLimitReached:
            self.timed_out = True

        if self.best_indices is None:
            return Plan(())
        return Plan.from_assignment(table.to_assignment(self.best_indices))

    def backtrack(self, day, first, used, cost_so_far, sums, flags_needed, chosen):
        self.nodes += 1
        if self.nodes % 1000 == 0 and time.perf_counter() - self.start > self.time_limit:
            raise TimeLimitReached()
        table = self.table
        costs, prefix_costs, masks = table.costs, table.prefix_costs, table.masks
        weekly_totals, flag_counts, upper_bounds = table.weekly_totals, table.flag_counts, table.upper_bounds
        remaining_days = table.days - 1 - day
        last_index = len(table) - remaining_days
        for index in range(first, last_index):
            cost = cost_so_far + costs[index]
            if cost + prefix_costs[index + 1 + remaining_days] - prefix_costs[index + 1] >= self.best_penalty:
                break
            if masks[index] & used:
                continue
            new_sums = [total + weekly_totals[k][index] for k, total in enumerate(sums)]
            if any(total > upper for total, upper in zip(new_sums, upper_bounds)):
                continue
            new_needed = [max(0, needed - flag_counts[k][index]) for k, needed in enumerate(flags_needed)]

            chosen.append(index)
            if remaining_days == 0:
                if self.meets_weekly(new_sums, new_needed):
                    self.on_complete(cost, chosen)
            else:
                self.backtrack(day + 1, index + 1, used | masks[index], cost, new_sums, new_needed, chosen)
            chosen.pop()

    def meets_weekly(self, sums, flags_needed):
        if any(total < lower for total, lower in zip(sums, self.table.lower_bounds)):
            return False
        return not any(flags_needed)

    def on_complete(self, cost, chosen):
        self.solutions_found += 1
        self.best_penalty = cost
        self.best_indices = list(chosen)