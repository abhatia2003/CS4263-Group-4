from src.constraints.base import HardConstraint

class DistinctDishes(HardConstraint):
    def __init__(self, scope, max_dishes_per_dish_per_week):
        super().__init__('distinct_dishes', scope)
        self.max_dishes_per_dish_per_week = max_dishes_per_dish_per_week
    
    def relation(self, assignment):
        counts = {}
        for variable in self.scope:
            if variable in assignment:
                dish = assignment[variable]
                counts[dish] = 1 + (counts[dish] if dish in counts else 0)
                if counts[dish] > self.max_dishes_per_dish_per_week:
                    return False
        return True