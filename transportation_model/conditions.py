# transportation_model/conditions


def format_conditions(problem: dict) -> str:
    """
    Формирует блок условий транспортной задачи.
    Выводит поставщиков, потребителей и матрицу стоимостей.
    """

    output = "=== Условия транспортной задачи ===\n"
    output += f"Поставщики: {problem['suppliers']}\n"
    output += f"Потребители: {problem['consumers']}\n"
    output += "Матрица стоимостей:\n"
    for row in problem["cost"]:
        output += "\t".join(str(x) for x in row) + "\n"
    output += "====================================\n\n"
    return output
