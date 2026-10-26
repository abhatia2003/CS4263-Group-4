from src.constraints.base import HardConstraint

class ItemType(HardConstraint):
    def __init__(self, scope):
        super().__init__('item_type', scope)
    
    def relation(self, assignment):
        for variable in self.scope:
            if variable in assignment:
                dish = assignment[variable]
                if dish.item_type != 'main':
                    return False
        return True