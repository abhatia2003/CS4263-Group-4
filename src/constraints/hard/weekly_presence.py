from src.constraints.base import HardConstraint, dishes_of

class WeeklyPresence(HardConstraint):
    def __init__(self, scope, nutrients):
        super().__init__('weekly_presence', scope)
        self.nutrients = nutrients
    
    def relation(self, assignment):
        if any([True if variable not in assignment else False for variable in self.scope]):
            return True # As long as some meal is not assigned, we return True, until all meals are assigned
        nutrients_remaining = self.nutrients.copy()
        for variable in self.scope: 
            for dish in dishes_of(assignment[variable]):
                for nutrient in nutrients_remaining:
                    if getattr(dish, nutrient) and nutrients_remaining[nutrient] > 0: 
                        nutrients_remaining[nutrient] -= 1
        return not any(nutrients_remaining.values())
    
    def is_reachable(self, assignment, range_summary, flag_summary):
        nutrients_remaining = self.nutrients.copy()
        for variable in self.scope:
            if variable in assignment:
                for dish in dishes_of(assignment[variable]):
                    for nutrient in nutrients_remaining:
                        if getattr(dish, nutrient) and nutrients_remaining[nutrient] > 0: 
                            nutrients_remaining[nutrient] -= 1
            else:
                for nutrient in nutrients_remaining:
                    available = flag_summary[variable].get(nutrient, 0)
                    nutrients_remaining[nutrient] = max(0, nutrients_remaining[nutrient] - available)
        return not any(nutrients_remaining.values())
