import time

from .csp_solver import CSPSolver
from ..output.plan import Plan


class TimeLimitReached(Exception):
    pass


class COPSolver(CSPSolver):
    def __init__(self, time_limit=10, order_by_cost=False):
        super().__init__()
        self.time_limit = time_limit
        self.order_by_cost = order_by_cost

    def _search(self, cop):
        self.cop = cop
        self.start = time.perf_counter()
        self.best_assignment = None
        self.best_penalty = float('inf')
        self.solutions_found = 0
        self.timed_out = False
        self.costs = {}
        for variable in cop.variables:
            for value in cop.domains[variable]:
                self.costs[(variable, value)] = cop.total_penalty({variable: value})

        domains = self.create_domains(cop)
        try:
            self.backtrack(cop, domains, {})
        except TimeLimitReached:
            self.timed_out = True

        if self.best_assignment is None:
            return Plan(())
        return Plan.from_assignment(self.best_assignment)

    def on_complete(self, cop, assignment):
        penalty = cop.total_penalty(assignment)
        self.solutions_found += 1
        if penalty < self.best_penalty:
            self.best_penalty = penalty
            self.best_assignment = dict(assignment)
        return None

    def should_prune(self, cop, domains, assignment):
        if time.perf_counter() - self.start > self.time_limit:
            raise TimeLimitReached()
        return self.lower_bound(assignment, domains) >= self.best_penalty

    def order_values(self, cop, variable, domains):
        if self.order_by_cost:
            return sorted(domains[variable], key=lambda value: self.costs[(variable, value)])
        return domains[variable]

    def lower_bound(self, assignment, domains):
        bound = self.cop.total_penalty(assignment)
        for variable in self.cop.variables:
            if variable not in assignment:
                bound += min((self.costs[(variable, value)] for value in domains[variable]), default=float('inf'))
        return bound