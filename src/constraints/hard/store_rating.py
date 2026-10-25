from src.constraints.base import HardConstraint

class StoreRating(HardConstraint):
    def __init__(self, scope, min_store_rating):
        super().__init__('store_rating', scope)
        self.min_store_rating = min_store_rating
    
    def relation(self, assignment):
        if not self.min_store_rating:
            return True
        for variable in self.scope:
            if variable in assignment:
                dish = assignment[variable]
                if dish.store_rating < self.min_store_rating:
                    return False
        return True