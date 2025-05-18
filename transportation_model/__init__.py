# transportation_model/__init__.py

from .generation import generate_random_problem
from .conditions import format_conditions
from .final_solution import solve_transportation_final
from .detailed_solution import solve_transportation_detailed
import logging

def solve_problem(suppliers, consumers, solution_type, cost=None) -> str:
    """
    Генерирует случайную транспортную задачу и возвращает результат в зависимости от solution_type.
      solution_type: 1 – подробное решение (с итерационными шагами);
                     2 – краткий итог (только ответ);
                     любое другое значение – только условия.
    """
    if cost is None:
        problem = generate_random_problem(suppliers, consumers)
        suppliers = problem["suppliers"]
        consumers = problem["consumers"]
        cost = problem["cost"]
    else:
        problem = {"suppliers": suppliers, "consumers": consumers, "cost": cost}

    logging.info(f'Значения, поставщики:{problem["suppliers"]}, потребители:{problem["consumers"]}, таблица стоимостей:{problem["cost"]}')
    if solution_type == 1:
        return solve_transportation_detailed(suppliers, consumers, cost)
    elif solution_type == 2:
        return solve_transportation_final(suppliers, consumers, cost)
    else:
        return format_conditions(problem)
