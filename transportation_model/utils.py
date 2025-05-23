# transportation_model/utils.py
# PERF: Можно ускорить используя CPython


def balance_problem(suppliers, consumers):
    total_supply = sum(suppliers)
    total_demand = sum(consumers)
    balanced = False
    if total_supply > total_demand:
        consumers = consumers.copy()
        consumers.append(total_supply - total_demand)
        balanced = True
    elif total_demand > total_supply:
        suppliers = suppliers.copy()
        suppliers.append(total_demand - total_supply)
        balanced = True
    return suppliers, consumers, balanced


def northwest_corner(suppliers, consumers):
    n = len(suppliers)
    m = len(consumers)
    alloc = [[0] * m for _ in range(n)]
    i, j = 0, 0
    s = suppliers.copy()
    d = consumers.copy()
    while i < n and j < m:
        allocation = min(s[i], d[j])
        alloc[i][j] = allocation
        s[i] -= allocation
        d[j] -= allocation
        if i == n - 1 and j == m - 1:
            break
        if s[i] == 0 and i < n - 1:
            i += 1
        elif d[j] == 0 and j < m - 1:
            j += 1
        else:
            if s[i] == 0 and d[j] == 0:
                if i < n - 1:
                    i += 1
                if j < m - 1:
                    j += 1
                if i == n - 1 and j == m - 1:
                    break
            else:
                break
    return alloc


def compute_potentials(cost, alloc):
    n = len(cost)
    m = len(cost[0])
    u = [None] * n
    v = [None] * m
    u[0] = 0
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(m):
                if alloc[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = cost[i][j] - u[i]
                        changed = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = cost[i][j] - v[j]
                        changed = True
    for i in range(n):
        if u[i] is None:
            u[i] = 0
    for j in range(m):
        if v[j] is None:
            v[j] = 0
    return u, v


def compute_deltas(cost, alloc, u, v):
    n = len(cost)
    m = len(cost[0])
    delta = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if alloc[i][j] == 0:
                delta[i][j] = cost[i][j] - (u[i] + v[j])
    return delta


def total_cost(cost, alloc):
    total = 0
    n = len(cost)
    m = len(cost[0])
    for i in range(n):
        for j in range(m):
            total += cost[i][j] * alloc[i][j]
    return total


def find_cycle(alloc, start):
    n = len(alloc)
    m = len(alloc[0])
    basic = [(i, j) for i in range(n) for j in range(m) if alloc[i][j] > 0]
    if start not in basic:
        basic.append(start)
    start_cell = start

    def search(path, last_move):
        current = path[-1]
        if len(path) >= 4 and current == start_cell:
            return path
        if last_move is None:
            for direction in ["row", "col"]:
                res = search(path, direction)
                if res:
                    return res
        elif last_move == "row":
            col = current[1]
            for i, j in basic:
                if j == col and i != current[0]:
                    if (i, j) == start_cell and len(path) >= 3:
                        return path + [(i, j)]
                    if (i, j) not in path:
                        res = search(path + [(i, j)], "col")
                        if res:
                            return res
        elif last_move == "col":
            row = current[0]
            for i, j in basic:
                if i == row and j != current[1]:
                    if (i, j) == start_cell and len(path) >= 3:
                        return path + [(i, j)]
                    if (i, j) not in path:
                        res = search(path + [(i, j)], "row")
                        if res:
                            return res
        return None

    cycle = search([start_cell], None)
    if cycle and cycle[0] == cycle[-1]:
        return cycle[:-1]
    return cycle


def optimize_transportation(cost, alloc):
    iteration = 0
    max_iterations = 100
    iteration_logs = ""
    while iteration < max_iterations:
        u, v = compute_potentials(cost, alloc)
        delta = compute_deltas(cost, alloc, u, v)
        entering = None
        min_delta = 0
        for i in range(len(cost)):
            for j in range(len(cost[0])):
                if (
                    alloc[i][j] == 0
                    and delta[i][j] is not None
                    and delta[i][j] < min_delta
                ):
                    min_delta = delta[i][j]
                    entering = (i, j)
        iteration_logs += f"Итерация {iteration}:\n"
        iteration_logs += "Матрица распределения:\n"
        for row in alloc:
            iteration_logs += "\t".join(str(x) for x in row) + "\n"
        iteration_logs += f"Потенциалы: u = {u}, v = {v}\n"
        iteration_logs += "Дельты:\n"
        for i in range(len(cost)):
            row_d = []
            for j in range(len(cost[0])):
                if alloc[i][j] == 0:
                    row_d.append(str(delta[i][j]))
                else:
                    row_d.append("-")
            iteration_logs += "\t".join(row_d) + "\n"
        if entering is None:
            iteration_logs += (
                f"Оптимальное решение достигнуто на итерации {iteration}.\n"
            )
            break
        iteration_logs += f"Входящая ячейка: {entering} с дельтой {min_delta}\n"
        cycle = find_cycle(alloc, entering)
        if not cycle:
            iteration_logs += "Цикл не найден. Прерывание итераций.\n"
            break
        iteration_logs += f"Найден цикл: {cycle}\n"
        minus_positions = cycle[1::2]
        theta = min(alloc[i][j] for (i, j) in minus_positions)
        iteration_logs += (
            f"Theta (минимальное значение на позициях с минусом): {theta}\n"
        )
        for idx, (i, j) in enumerate(cycle):
            if idx % 2 == 0:
                alloc[i][j] += theta
            else:
                alloc[i][j] -= theta
        iteration_logs += "Обновленная матрица распределения:\n"
        for row in alloc:
            iteration_logs += "\t".join(str(x) for x in row) + "\n"
        iteration_logs += "\n"
        iteration += 1
    return alloc, iteration_logs
