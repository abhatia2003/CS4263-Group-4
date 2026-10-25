from .csp import CSP
class COP(CSP):
    def __init__(self, variables, domains, hard_constraints, soft_constraints):
        super().__init__(variables, domains, hard_constraints)
        self.soft_constraints = soft_constraints
    
    def total_penalty(self, assignment): 
        return self.soft_constraints.total_penalty(assignment)
    