from .cop import COP
from .csp import CSP
from ..constraints.soft.objective import Objective
from ..constraints.hard import DistinctDishes, DailyRange, DailyPresence, ItemType, StoreRating, WeeklyRange, WeeklyPresence

class Builder:
    
    def __init__(self, puzzle, menu): 
        self.puzzle = puzzle
        self.menu = menu
        self.days = self.puzzle.days
        self.meals_per_day = self.puzzle.meals_per_day
        self.variables = tuple((i, j) for i in range(self.days) for j in range(self.meals_per_day)) 
        self.domains = self.create_domains()
        self.weekly_scope = self.variables
        self.daily_scopes = tuple(tuple((i, j) for j in range(self.meals_per_day)) for i in range(self.days))
        self.soft_constraints = Objective.add_soft_constraints(puzzle, self.weekly_scope)
        self.hard_constraints = self.add_hard_constraints()
        

    def create_domains(self):
        domains = {}
        for variable in self.variables:  
            domains[variable] = list(self.menu.get_all_dishes()) # May change to set subsequently
        return domains
    
    def add_hard_constraints(self):
        weekly = self.puzzle.weekly
        weekly_presence = self.puzzle.weekly_presence
        daily = self.puzzle.daily
        daily_presence = self.puzzle.daily_presence
        constraints = []
        constraints.append(ItemType(self.weekly_scope))
        constraints.append(DistinctDishes(self.weekly_scope, self.puzzle.max_times_per_dish_per_week))
        constraints.append(StoreRating(self.weekly_scope, self.puzzle.min_store_rating))
        
        for parameter, bound in weekly.items(): 
            constraints.append(WeeklyRange(self.weekly_scope, parameter, bound))
        constraints.append(WeeklyPresence(self.weekly_scope, weekly_presence))
        
        for parameter, bound in daily.items():
            for daily_scope in self.daily_scopes:
                constraints.append(DailyRange(daily_scope, parameter, bound))
        for daily_scope in self.daily_scopes:
            constraints.append(DailyPresence(daily_scope, daily_presence))
        return constraints
    
    def build_csp(self):
        return CSP(self.variables, self.domains, self.hard_constraints)
    
    def build_cop(self):
        return COP(self.variables, self.domains, self.hard_constraints, self.soft_constraints)
    