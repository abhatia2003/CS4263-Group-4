from abc import ABC, abstractmethod

class SoftConstraint(ABC):
    def __init__(self, name, scope, attribute, weight):
        self.name = name
        self.scope = scope
        self.attribute = attribute
        self.weight = weight
        
    
    @abstractmethod
    def penalty(self, assignment):
        pass