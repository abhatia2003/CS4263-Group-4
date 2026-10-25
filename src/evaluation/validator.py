from ..model.builder import Builder

def validate(puzzle, plan, menu): 
    failures = []
    builder = Builder(puzzle, menu)
    assignment = plan.to_assignment(menu)
    constraints = builder.hard_constraints
    for constraint in constraints:
        if not constraint.relation(assignment):
            failures.append(constraint)
    return failures
