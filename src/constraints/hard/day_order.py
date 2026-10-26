from ..base import HardConstraint


class DayOrder(HardConstraint):
    def __init__(self, scope, positions):
        super().__init__('day_order', scope)
        self.positions = positions

    def relation(self, assignment):
        previous = -1
        for variable in self.scope:
            if variable in assignment:
                position = self.positions[assignment[variable]]
                if position <= previous:
                    return False
                previous = position
        return True