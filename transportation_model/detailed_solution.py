# transportation_model/detailed_solution

from .utils import balance_problem, northwest_corner, optimize_transportation, compute_potentials, compute_deltas, total_cost
from .conditions import format_conditions
from .solution import format_solution

def solve_transportation_detailed(suppliers, consumers, cost) -> str:
    # Блок условии
    problem: dict = {"suppliers": suppliers, "consumers": consumers, "cost": cost}
    output = format_conditions(problem=problem)
    
    # Решение
    output += "=== РЕШЕНИЕ ТРАНСПОРТНОЙ ЗАДАЧИ (ПОДРОБНО) ===\n"
    suppliers_bal, consumers_bal, balanced = balance_problem(suppliers, consumers)
    total_supply = sum(suppliers)
    total_demand = sum(consumers)
    output += "Шаг 1: Балансировка задачи\n"
    output += f"Общее предложение = {total_supply}, общий спрос = {total_demand}\n"
    if balanced:
        output += "Была проведена балансировка:\n"
        output += f"Новые поставщики: {suppliers_bal}\n"
        output += f"Новые потребители: {consumers_bal}\n"
    else:
        output += "Задача сбалансирована.\n"
    output += "\n"
    
    n_bal = len(suppliers_bal)
    m_bal = len(consumers_bal)
    output += "Шаг 2: Матрица стоимостей (после балансировки)\n"
    for i in range(n_bal):
        output += "\t".join(str(cost[i][j]) for j in range(m_bal)) + "\n"
    output += "\n"
    
    output += "Шаг 3: Начальное базисное решение (метод северо‑западного угла)\n"
    alloc = northwest_corner(suppliers_bal, consumers_bal)
    for row in alloc:
        output += "\t".join(str(x) for x in row) + "\n"
    output += "\n"
    
    output += "Шаг 4: Оптимизация базисного решения (метод потенциалов)\n"
    alloc_opt, iter_logs = optimize_transportation(cost, alloc)
    output += iter_logs + "\n"
    
    u, v = compute_potentials(cost, alloc_opt)
    output += "Итоговые потенциалы:\n"
    output += f"\tu (строки): {u}\n"
    output += f"\tv (столбцы): {v}\n\n"
    
    delta = compute_deltas(cost, alloc_opt, u, v)
    output += "Итоговые дельты (для не базисных ячеек):\n"
    for i in range(n_bal):
        row_d = []
        for j in range(m_bal):
            if alloc_opt[i][j] == 0:
                row_d.append(str(delta[i][j]))
            else:
                row_d.append("-")
        output += "\t".join(row_d) + "\n"
    output += "\n"
    total = total_cost(cost, alloc_opt)
    
    # Блок Выводов
    output += format_solution(total, alloc_opt)
    return output
