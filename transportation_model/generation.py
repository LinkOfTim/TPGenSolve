# transportation_model/generation

import random

def generate_random_problem(n: int, m: int) -> dict:
    """
    Генерирует случайную транспортную задачу:
      - Поставщики: случайные значения от 10 до 100.
      - Потребители: разбиты так, чтобы их сумма равнялась сумме поставщиков.
      - Матрица стоимостей: случайные целые от 1 до 20, размерности n x m.
    Возвращает словарь с ключами "suppliers", "consumers" и "cost".
    """
    suppliers = [random.randint(10, 100) for _ in range(n)]
    total_supply = sum(suppliers)
    if m == 1:
        consumers = [total_supply]
    else:
        cuts = sorted(random.sample(range(1, total_supply), m - 1))
        consumers = [cuts[0]] + [cuts[i] - cuts[i-1] for i in range(1, len(cuts))] + [total_supply - cuts[-1]]
    cost = [[random.randint(1, 20) for _ in range(m)] for _ in range(n)]
    return {"suppliers": suppliers, "consumers": consumers, "cost": cost}
