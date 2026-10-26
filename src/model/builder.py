from collections import Counter
from itertools import combinations

from .cop import COP
from .csp import CSP
from ..constraints.soft.objective import Objective
from ..constraints.hard import DistinctDishes, DailyRange, DailyPresence, DayOrder, ItemType, StoreRating, WeeklyRange, WeeklyPresence

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
        

    def eligible_dishes(self):
        min_rating = self.puzzle.min_store_rating
        return [
            dish for dish in self.menu.get_all_dishes()
            if dish.item_type == 'main'
            and (min_rating is None or dish.store_rating >= min_rating)
        ]

    def create_domains(self):
        eligible = self.eligible_dishes()
        domains = {}
        for variable in self.variables:
            domains[variable] = list(eligible)
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
    
    def create_day_triples(self):
        day_scope = self.daily_scopes[0]
        daily_constraints = [
            constraint for constraint in self.hard_constraints
            if isinstance(constraint, (DailyRange, DailyPresence)) and constraint.scope == day_scope
        ]
        eligible = sorted(self.eligible_dishes(), key=lambda dish: dish.dish_id)
        triples = []
        for triple in combinations(eligible, self.meals_per_day):
            assignment = {slot: dish for slot, dish in zip(day_scope, triple)}
            if all(constraint.relation(assignment) for constraint in daily_constraints):
                triples.append(triple)
        usage = Counter(dish for triple in triples for dish in triple)
        triples.sort(key=lambda triple: sum(usage[dish] for dish in triple))
        return triples

    def build_day_cop(self):
        day_variables = tuple(range(self.days))
        triples = self.create_day_triples()
        positions = {triple: i for i, triple in enumerate(triples)}
        domains = {day: list(triples) for day in day_variables}
        constraints = [DistinctDishes(day_variables, self.puzzle.max_times_per_dish_per_week)]
        for parameter, bound in self.puzzle.weekly.items():
            constraints.append(WeeklyRange(day_variables, parameter, bound))
        constraints.append(WeeklyPresence(day_variables, self.puzzle.weekly_presence))
        constraints.append(DayOrder(day_variables, positions))
        objective = Objective.add_soft_constraints(self.puzzle, day_variables)
        return COP(day_variables, domains, constraints, objective)