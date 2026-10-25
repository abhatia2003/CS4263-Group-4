from src.constraints.hard import DistinctDishes, DailyRange, DailyPresence, ItemType, StoreRating, WeeklyRange, WeeklyPresence

def validate(puzzle, plan, menu): 
    days = puzzle.days
    meals_per_day = puzzle.meals_per_day
    weekly_scope = tuple((i, j) for j in range(meals_per_day) for i in range(days))
    daily_scopes = tuple(tuple((i, j) for j in range(meals_per_day)) for i in range(days))
    weekly = puzzle.weekly
    weekly_presence = puzzle.weekly_presence
    daily = puzzle.daily
    daily_presence = puzzle.daily_presence
    assignment = plan.to_assignment(menu)
    
    constraints = []
    failures = []
    constraints.append(ItemType(weekly_scope))
    constraints.append(DistinctDishes(weekly_scope, puzzle.max_times_per_dish_per_week))
    constraints.append(StoreRating(weekly_scope, puzzle.min_store_rating))
    
    for parameter, bound in weekly.items(): 
        constraints.append(WeeklyRange(weekly_scope, parameter, bound))
    constraints.append(WeeklyPresence(weekly_scope, weekly_presence))
    
    for parameter, bound in daily.items():
        for daily_scope in daily_scopes:
            constraints.append(DailyRange(daily_scope, parameter, bound))
    for daily_scope in daily_scopes:
        constraints.append(DailyPresence(daily_scope, daily_presence))
    for constraint in constraints:
        if not constraint.relation(assignment):
            failures.append(constraint)
    return failures
