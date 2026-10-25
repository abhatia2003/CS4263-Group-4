class CSP():
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
    
    def is_complete(self, assignment):
        return len(assignment) == len(self.variables)

    def is_consistent(self, assignment):
        for constraint in self.constraints:
            if not constraint.relation(assignment):
                return False
        return True
    
        