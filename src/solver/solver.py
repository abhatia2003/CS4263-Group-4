import time

from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self):
        self.solve_time = 0
        self.status = ""
    
    def solve(self, problem):
        self.solve_time = 0
        self.status = ""
        start = time.perf_counter()
        plan = self._search(problem)
        self.solve_time = time.perf_counter() - start
        if plan.is_valid():
            self.status = "SOLVABLE"
        else:
            self.status = "UNSOLVABLE"
        return plan
        
    @abstractmethod
    def _search(self, problem):
        pass
    