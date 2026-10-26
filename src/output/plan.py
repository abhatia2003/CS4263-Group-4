from dataclasses import dataclass

@dataclass(frozen = True)
class Plan:
    days: tuple[tuple[str, ...], ...]

    @classmethod
    def load_plan(cls, solution):
        if solution['status'] == 'SOLVABLE':
            plan = solution['plan']
            num_days = len(plan)
            output = []
            for i in range(num_days):
                dishes = plan[f'day_{i+1}']
                output.append(tuple(dishes))
            output = tuple(output)
            return cls(output)
        return cls(())

    def parse_plan(self):
        num_days = len(self.days)
        res = {}
        for i in range(num_days):
            res[f'day_{i+1}'] = list(self.days[i])
        return res

    def to_assignment(self, menu): 
        res = {}
        for i, row in enumerate(self.days):
            for j, dish in enumerate(row):
                res[(i, j)] = menu.get_dish(dish)
        return res
    
    @classmethod
    def from_assignment(cls, assignment):
        res = []
        curr_row = -1
        for (i, j), dish in sorted(assignment.items()):
            if i != curr_row:
                res.append([])
                curr_row = i
            res[-1].append(dish.dish_id)
        res = tuple(tuple(row) for row in res)
        return cls(res)
            

    def is_valid(self):
        return len(self.days) > 0 