from abc import ABC, abstractmethod

class HardConstraint(ABC): 
    def __init__(self, name, scope):
        self.name = name
        self.scope = scope
        self.scope_weight = len(scope)
    
    @abstractmethod
    def relation(self, assignment):
        pass
    
    def is_reachable(self, assignment, range_summary, flag_summary):
        return True