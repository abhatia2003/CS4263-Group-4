from .solver import Solver
from ..output.plan import Plan
from ..constraints.hard import DailyPresence, DailyRange, WeeklyPresence, WeeklyRange
from ..constraints.base import dishes_of

class CSPSolver(Solver):
    def __init__(self):
        super().__init__()
    
    def select_next_variable(self, assignment, csp, domains): # Uses MRV
        variables = csp.variables
        best_variable = None
        least_remaining_values = float('inf')
        for variable in variables:
            if variable not in assignment:
                remaining_values = len(domains[variable])
                if remaining_values < least_remaining_values:
                    best_variable = variable
                    least_remaining_values = remaining_values
        return best_variable
    
    def _search(self, csp):
        domains = self.create_domains(csp)
        res = self.backtrack(csp, domains, {})
        if not res:
            return Plan(())
        return Plan.from_assignment(res)
    
    def backtrack(self, csp, domains, assignment):
        if csp.is_complete(assignment):
            return assignment
        
        next_variable = self.select_next_variable(assignment, csp, domains)
        
        for value in domains[next_variable]:
            assignment[next_variable] = value
            if csp.is_consistent(assignment):
                inferences = self.inference(csp, next_variable, assignment, domains)
                if not self.is_failure(inferences): 
                    self.add_inference(inferences, domains) 
                    result = self.backtrack(csp, domains, assignment)
                    if result is not None:
                        return result
                    self.remove_inference(inferences, domains) 
            assignment.pop(next_variable, None) 
        return None
    
    def create_domains(self, csp):
        domains = {}
        for variable in csp.variables:  
            domains[variable] = list(csp.domains[variable]) # May change to set subsequently
        return domains
    
    def inference(self, csp, next_variable, assignment, domains):
        return self.forward_check(csp, next_variable, assignment, domains) 
    
    def is_failure(self, inferences):
        return inferences is None
    
    def add_inference(self, inferences, domains):
        for variable, value in inferences:
            domains[variable].remove(value)

    def remove_inference(self, inferences, domains):
        for variable, value in inferences:
            domains[variable].append(value)
            
    def forward_check(self, csp, next_variable, assignment, domains):
        to_remove = set()
        vars_to_remove = set()
        constraints = csp.constraints
        relevant_constraints = []
        unassigned = []
        attributes = set()
        flags = set()
        for constraint in constraints:
            if isinstance(constraint, (DailyRange, WeeklyRange)):
                attributes.add(constraint.parameter)
            elif isinstance(constraint, (DailyPresence, WeeklyPresence)):
                flags.update(constraint.nutrients)
        
        for constraint in constraints:
            scope = constraint.scope
            if next_variable not in scope:
                continue
            relevant_constraints.append(constraint)
            for variable in scope: 
                if variable == next_variable:
                    continue
                if variable not in assignment and variable not in unassigned:
                    unassigned.append(variable)
        
        range_summary = {}
        flag_summary = {}
        for variable in unassigned:
            range_summary[variable] = {}
            for attribute in attributes:
                values = [sum(getattr(dish, attribute) for dish in dishes_of(value)) for value in domains[variable]]
                if values:
                    range_summary[variable][attribute] = (min(values), max(values))
                else:
                    range_summary[variable][attribute] = (float('inf'), float('-inf'))
            flag_summary[variable] = {}
            for flag in flags:
                most = max((sum(getattr(dish, flag) for dish in dishes_of(value)) for value in domains[variable]), default=0)
                if most > 0:
                    flag_summary[variable][flag] = most
        for unassigned_var in unassigned:
            for constraint in relevant_constraints:
                if unassigned_var not in constraint.scope:
                    continue
                for val in domains[unassigned_var]:
                    assignment[unassigned_var] = val 
                    if not constraint.relation(assignment) or not constraint.is_reachable(assignment, range_summary, flag_summary):
                        to_remove.add((unassigned_var, val))
                        vars_to_remove.add(unassigned_var)
                    assignment.pop(unassigned_var, None)
        
        for variable in vars_to_remove: 
            all_removed = True
            for value in domains[variable]:
                if (variable, value) not in to_remove:
                    all_removed = False
                    break
            if all_removed:
                return None
        return to_remove
            

        
        
    # def unsolvable(self, csp, domains, assignment):
    #     variables = csp.variables
    #     for variable in variables:
    #         if not domains[variable] and variable not in assignment:
    #             return True
    #     return False