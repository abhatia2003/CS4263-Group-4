from .optimise_constraint import OptimiseConstraint

class Objective(): 
    def __init__(self, constraints):
        self.constraints = constraints
    
    @classmethod
    def add_soft_constraints(cls, puzzle, scope):
        soft_constraints = []
        menu = puzzle.menu
        min_objectives = puzzle.objective['minimize'] if 'minimize' in puzzle.objective else {}
        max_objectives = puzzle.objective['maximize'] if 'maximize' in puzzle.objective else {} 
        for param, weight in min_objectives.items():
            soft_constraints.append(OptimiseConstraint(f'minimize_{param}', scope, param, menu, weight, 1))
        for param, weight in max_objectives.items():
            soft_constraints.append(OptimiseConstraint(f'maximize_{param}', scope, param, menu, weight, -1))
        return cls(soft_constraints)

    def total_penalty(self, assignment):
        cost = 0
        for constraint in self.constraints:
            cost += constraint.penalty(assignment)
        return cost