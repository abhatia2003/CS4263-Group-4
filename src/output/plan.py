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