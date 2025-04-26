# transportation_model/final_solution

from .utils import balance_problem, northwest_corner, optimize_transportation, total_cost
from .conditions import format_conditions
from .solution import format_solution

def solve_transportation_final(suppliers, consumers, cost) -> str:
    # Блок условии
    problem: dict = {"suppliers": suppliers, "consumers": consumers, "cost": cost}
    output = format_conditions(problem=problem)
    
    suppliers_bal, consumers_bal, _ = balance_problem(suppliers, consumers)
    alloc_initial = northwest_corner(suppliers_bal, consumers_bal)
    alloc_opt, _ = optimize_transportation(cost, alloc_initial)
    total = total_cost(cost, alloc_opt)

    # Блок Выводов
    output += format_solution(total, alloc_opt)
    return output
