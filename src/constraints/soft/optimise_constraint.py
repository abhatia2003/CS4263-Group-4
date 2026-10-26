from .soft_constraint import SoftConstraint
from ..base import dishes_of

class OptimiseConstraint(SoftConstraint):
    def __init__(self, name, scope, attribute, menu, weight, direction):
        super().__init__(name, scope, attribute, weight)
        self.menu = menu
        self.direction = direction # Minimise penalty as much as possible
        self.largest = self.largest_val()
        self.smallest = self.smallest_val()

    def largest_val(self):
        res = float('-inf')
        for dish in self.menu.get_dishes_by_type('main'):
            res = max(res, getattr(dish, self.attribute))
        return res

    def smallest_val(self):
        res = float('inf')
        for dish in self.menu.get_dishes_by_type('main'):
            res = min(res, getattr(dish, self.attribute))
        return res
    
    def normalise_param(self, parameter):
        score_range = self.largest - self.smallest
        if self.direction > 0:
            return (parameter - self.smallest) / score_range
        return (self.largest - parameter) / score_range
    
    def penalty(self, assignment):
        accumulated_penalty = 0
        for variable in self.scope: 
            if variable in assignment: 
                for dish in dishes_of(assignment[variable]):
                    parameter = getattr(dish, self.attribute)
                    normalised_parameter = self.normalise_param(parameter)
                    accumulated_penalty += self.weight * normalised_parameter
        return accumulated_penalty