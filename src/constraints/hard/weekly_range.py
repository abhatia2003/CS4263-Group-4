from src.constraints.base import HardConstraint

class WeeklyRange(HardConstraint):
    def __init__(self, scope, parameter, bound):
        super().__init__('weekly_range', scope)
        self.parameter = parameter
        self.lower_bound = bound[0] if bound[0] is not None else float('-inf')
        self.upper_bound = bound[1] if bound[1] is not None else float('inf')
    
    def relation(self, assignment):
        total_sum = 0
        all_assigned = True
        for variable in self.scope:
            if variable in assignment:
                dish = assignment[variable]
                if total_sum + getattr(dish, self.parameter) > self.upper_bound:
                    return False
                total_sum += getattr(dish, self.parameter)
            else:
                all_assigned = False
        if all_assigned:
            return total_sum >= self.lower_bound
        return True # Return true if incomplete and total_sum does not exceed upper bound

    def is_reachable(self, assignment, range_summary, flag_summary):
        min_possible = 0
        max_possible = 0
        for variable in self.scope:
            if variable in assignment:
                dish = assignment[variable]
                if min_possible + getattr(dish, self.parameter) > self.upper_bound:
                    return False
                min_possible += getattr(dish, self.parameter)
                max_possible += getattr(dish, self.parameter) 
            else:
                min_score, max_score = range_summary[variable][self.parameter]
                min_possible += min_score
                max_possible += max_score
        return min_possible <= self.upper_bound and max_possible >= self.lower_bound
