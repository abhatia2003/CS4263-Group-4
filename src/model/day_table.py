from itertools import accumulate


class DayTable:
    def __init__(self, puzzle, day_cop, eligible_dishes):
        if puzzle.max_times_per_dish_per_week != 1:
            raise ValueError('DayTable needs every dish to be used at most once per week')
        self.days = puzzle.days
        costs = {triple: day_cop.total_penalty({0: triple}) for triple in day_cop.domains[0]}
        self.triples = sorted(costs, key=lambda triple: costs[triple])
        self.costs = [costs[triple] for triple in self.triples]
        self.prefix_costs = [0] + list(accumulate(self.costs))

        dish_index = {dish: i for i, dish in enumerate(sorted(eligible_dishes, key=lambda dish: dish.dish_id))}
        self.masks = [sum(1 << dish_index[dish] for dish in triple) for triple in self.triples]

        self.weekly_parameters = list(puzzle.weekly)
        self.lower_bounds = [float('-inf') if bound[0] is None else bound[0] for bound in puzzle.weekly.values()]
        self.upper_bounds = [float('inf') if bound[1] is None else bound[1] for bound in puzzle.weekly.values()]
        self.weekly_totals = [
            [sum(getattr(dish, parameter) for dish in triple) for triple in self.triples]
            for parameter in self.weekly_parameters
        ]

        self.flags = list(puzzle.weekly_presence)
        self.flags_needed = list(puzzle.weekly_presence.values())
        self.flag_counts = [
            [sum(1 for dish in triple if getattr(dish, flag)) for triple in self.triples]
            for flag in self.flags
        ]

    def __len__(self):
        return len(self.triples)

    def to_assignment(self, indices):
        return {day: self.triples[index] for day, index in enumerate(indices)}