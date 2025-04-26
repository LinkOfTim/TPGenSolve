# transportation_model/solution.py

def format_solution(total: int, alloc_opt) -> str:
    """
    Формирует блок решения или вывода транспортной задачи.
    Выводит стоимость решения и оптимальный план поставок.
    """

    output = "=== Решение ===\n"
    output += f"Итоговая стоимость решения: {total}\n"
    output += "Оптимальный план поставок:\n"
    for row in alloc_opt:
        output += "\t".join(str(x) for x in row) + "\n"
    return output
