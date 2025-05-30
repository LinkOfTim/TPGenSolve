# TransportSolver

**TransportSolver** — кроссплатформенное настольное приложение для автоматической генерации и пошагового решения транспортных задач методом потенциалов. Проект ориентирован на использование в учебных целях в университетах, позволяет студентам и преподавателям получать наглядные решения логистических задач.

## 📌 Возможности

- Генерация сбалансированных транспортных задач с заданным числом поставщиков и потребителей.
- Ручной ввод задачи: поставщики, потребители и матрица стоимостей.
- Выбор режима:
  - Только условия (без решения)
  - Только ответ (оптимальный план поставок + итоговая стоимость)
  - Полное пошаговое решение (метод потенциалов)
- Экспорт решения в `.txt` или `.docx` (Word) с форматированной таблицей.
- Импорт задачи из `.txt` файла по шаблону.
- Графический интерфейс (PyQt5).
- Кроссплатформенная сборка под Windows/Linux.

## 🚀 Установка и запуск

### 🐧 Linux (Python 3.12.3+)

```bash
git clone https://github.com/LinkOfTim/TPGenSolve.git
cd TransportSolver
poetry install
poetry run python main.py
```
🛠️ Используемые технологии

| Категория    | Библиотека/Технология                          |
| ------------ | ---------------------------------------------- |
| Язык         | Python 3.12.3 / 3.11                           |
| GUI          | PyQt5                                          |
| Алгоритмы    | Метод северо-западного угла, Метод потенциалов |
| Экспорт      | python-docx                                    |
| Логирование  | logging                                        |
| Тестирование | unittest                                       |
| Сборка (Win) | PyInstaller, NSIS                              |

📑 Формат импорта из TXT
```bash
Поставщики: [30, 40, 50]
Потребители: [20, 60, 40]
Матрица стоимостей:
[ [2, 3, 1],
  [5, 4, 8],
  [5, 6, 8] ]
```
👨‍🎓 Авторы

Проект выполнен в рамках магистерской программы Жубанова (Казахстан), специальность "Вычислительная техника и программное обеспечение".
- Автор: Tairkhan 
- Научный руководитель: доц. Сарсимбаева С.М.
