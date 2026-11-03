import time

from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self):
        self.solve_time = 0
        self.status = ""
        self.timed_out = False
        self.optimal = False
    
    def solve(self, problem):
        self.solve_time = 0
        self.status = ""
        self.timed_out = False
        start = time.perf_counter()
        plan = self._search(problem)
        self.solve_time = time.perf_counter() - start
        if plan.is_valid():
            self.status = "SOLVABLE"
        elif self.timed_out:
            self.status = "UNKNOWN"
        else:
            self.status = "UNSOLVABLE"
        self.optimal = plan.is_valid() and not self.timed_out
        return plan
        
    @abstractmethod
    def _search(self, problem):
        pass