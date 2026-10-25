from abc import ABC, abstractmethod

class HardConstraint(ABC): 
    def __init__(self, name, scope):
        self.name = name
        self.scope = scope
    
    @abstractmethod
    def relation(self, assignment):
        pass