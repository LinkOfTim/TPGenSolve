# view.py

from PyQt5 import QtWidgets, QtCore
import logging
import ast
from transportation_model import solve_problem

class MainWindow(QtWidgets.QMainWindow):
    """
    Главное окно с выбором: Решить задачу или Генерировать задачу.
    """
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("Модуль транспортных задач")
        self.setGeometry(100, 100, 300, 150)
        self.initUI()

    def initUI(self):
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        layout = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(layout)

        self.btn_solve = QtWidgets.QPushButton("Решить задачу")
        self.btn_generate = QtWidgets.QPushButton("Генерировать задачу")
        layout.addWidget(self.btn_solve)
        layout.addWidget(self.btn_generate)

        self.btn_solve.clicked.connect(self.open_solve_dialog)
        self.btn_generate.clicked.connect(self.open_generate_dialog)

    def open_solve_dialog(self):
        dialog = SolveDialog(self, self.model)
        dialog.exec()

    def open_generate_dialog(self):
        dialog = GenerateDialog(self, self.model)
        dialog.exec()

class SolveDialog(QtWidgets.QDialog):
    """
    Диалог для ввода данных при решении задачи.
    Теперь включает динамические поля для поставщиков, потребителей и матрицы стоимостей.
    """
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("Решение задачи")
        self.resize(600, 700)
        self.setMinimumSize(400, 300)
        self.setSizeGripEnabled(True)

        # Основной лейаут диалога
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        
        # Создаём QScrollArea
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Создаём внутренний виджет, в котором будут поля ввода
        self.inner_widget = QtWidgets.QWidget()
        self.inner_layout = QtWidgets.QVBoxLayout(self.inner_widget)
        
        # Добавляем внутренний виджет в scroll_area
        self.scroll_area.setWidget(self.inner_widget)
        
        # Теперь добавляем scroll_area в основной лейаут
        main_layout.addWidget(self.scroll_area)

        self.supplier_entries = []
        self.consumer_entries = []
        self.cost_entries = []  # Список списков для матрицы стоимости
        self.initUI()

    def initUI(self):

        # Ввод количества поставщиков и потребителей
        self.n_label = QtWidgets.QLabel("Количество поставщиков (n):")
        self.n_input = QtWidgets.QLineEdit()
        self.m_label = QtWidgets.QLabel("Количество потребителей (m):")
        self.m_input = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(self.n_label)
        self.inner_layout.addWidget(self.n_input)
        self.inner_layout.addWidget(self.m_label)
        self.inner_layout.addWidget(self.m_input)

        # Кнопка для создания динамических полей ввода
        self.btn_create_fields = QtWidgets.QPushButton("Создать поля ввода")
        self.btn_create_fields.clicked.connect(self.create_value_fields)
        self.inner_layout.addWidget(self.btn_create_fields)

        # Область для ввода значений поставщиков
        self.suppliers_widget = QtWidgets.QWidget()
        self.suppliers_layout = QtWidgets.QVBoxLayout()
        self.suppliers_widget.setLayout(self.suppliers_layout)
        self.inner_layout.addWidget(self.suppliers_widget)

        # Область для ввода значений потребителей
        self.consumers_widget = QtWidgets.QWidget()
        self.consumers_layout = QtWidgets.QVBoxLayout()
        self.consumers_widget.setLayout(self.consumers_layout)
        self.inner_layout.addWidget(self.consumers_widget)

        # Область для ввода матрицы стоимостей
        self.cost_widget = QtWidgets.QWidget()
        self.cost_layout = QtWidgets.QGridLayout()
        self.cost_widget.setLayout(self.cost_layout)
        cost_label = QtWidgets.QLabel("Матрица стоимостей:")
        self.inner_layout.addWidget(cost_label)
        self.inner_layout.addWidget(self.cost_widget)

        # Кнопка импорта
        self.btn_import = QtWidgets.QPushButton("Импорт")
        # Подсказка с описанием ожидаемого формата файла
        self.btn_import.setToolTip(
            "Ожидаемый формат TXT:\n"
            "=== Условия транспортной задачи ===\n"
            "Поставщики: [23, 77, 88]\n"
            "Потребители: [1, 168, 19]\n"
            "Матрица стоимостей:\n"
            "4    1    9\n"
            "8    8    5\n"
            "4    18   3\n"
            "===================================="
        )
        self.btn_import.clicked.connect(self.import_file)
        self.inner_layout.addWidget(self.btn_import)

        # Радио кнопки для выбора типа решения
        self.solution_type_group = QtWidgets.QButtonGroup(self)
        self.radio_full = QtWidgets.QRadioButton("Полное решение")
        self.radio_short = QtWidgets.QRadioButton("Только ответ")
        self.radio_full.setChecked(True)
        self.solution_type_group.addButton(self.radio_full, 1)
        self.solution_type_group.addButton(self.radio_short, 2)
        self.inner_layout.addWidget(self.radio_full)
        self.inner_layout.addWidget(self.radio_short)

        # Опция экспорта
        self.export_checkbox = QtWidgets.QCheckBox("Экспортировать результат")
        self.export_checkbox.stateChanged.connect(self.toggle_export_options)
        self.inner_layout.addWidget(self.export_checkbox)

        self.export_options_widget = QtWidgets.QWidget()
        export_layout = QtWidgets.QHBoxLayout()
        self.export_options_widget.setLayout(export_layout)
        self.radio_txt = QtWidgets.QRadioButton("txt")
        self.radio_word = QtWidgets.QRadioButton("Word")
        self.radio_txt.setChecked(True)
        export_layout.addWidget(self.radio_txt)
        export_layout.addWidget(self.radio_word)
        self.export_options_widget.setVisible(False)
        self.inner_layout.addWidget(self.export_options_widget)

        # Кнопка для запуска решения
        self.btn_solve = QtWidgets.QPushButton("Решить задачу")
        self.btn_solve.clicked.connect(self.run_solution)
        self.inner_layout.addWidget(self.btn_solve)

    def toggle_export_options(self):
        self.export_options_widget.setVisible(self.export_checkbox.isChecked())

    def create_value_fields(self):
        # Очищаем предыдущие поля для поставщиков, потребителей и матрицы стоимости
        logging.info("Создание полей ввода для поставщиков, потребителей и матрицы стоимостей")
        for layout in (self.suppliers_layout, self.consumers_layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        # Очистка матрицы стоимости
        for i in reversed(range(self.cost_layout.count())):
            widget = self.cost_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()
        self.supplier_entries = []
        self.consumer_entries = []
        self.cost_entries = []

        try:
            n = int(self.n_input.text())
            m = int(self.m_input.text())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите корректные положительные числа для n и m.")
            return

        # Создаем поля для поставщиков
        sup_label = QtWidgets.QLabel("Значения поставщиков:")
        self.suppliers_layout.addWidget(sup_label)
        for i in range(n):
            le = QtWidgets.QLineEdit()
            le.setPlaceholderText(f"Поставщик {i+1}")
            self.suppliers_layout.addWidget(le)
            self.supplier_entries.append(le)

        # Создаем поля для потребителей
        cons_label = QtWidgets.QLabel("Значения потребителей:")
        self.consumers_layout.addWidget(cons_label)
        for i in range(m):
            le = QtWidgets.QLineEdit()
            le.setPlaceholderText(f"Потребитель {i+1}")
            self.consumers_layout.addWidget(le)
            self.consumer_entries.append(le)

        # Создаем поля для матрицы стоимостей (n строк, m столбцов)
        for i in range(n):
            row_entries = []
            for j in range(m):
                le = QtWidgets.QLineEdit()
                le.setPlaceholderText(f"C[{i+1},{j+1}]")
                self.cost_layout.addWidget(le, i, j)
                row_entries.append(le)
            self.cost_entries.append(row_entries)

    def import_file(self):
        logging.info("Открытие диалога импорта файла")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Импортировать задачу", "", "Text Files (*.txt)")
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            logging.info("Импорт файла: %s", filename)
            lines = content.splitlines()
            suppliers_line = None
            consumers_line = None
            matrix_start = None
            for i, line in enumerate(lines):
                if "Поставщики:" in line:
                    suppliers_line = line
                elif "Потребители:" in line:
                    consumers_line = line
                elif "Матрица стоимостей" in line:
                    matrix_start = i + 1
                    break
            if suppliers_line is None or consumers_line is None or matrix_start is None:
                QtWidgets.QMessageBox.critical(self, "Ошибка импорта", "Неверный формат файла.")
                logging.error("Импорт: неверный формат файла")
                return
            suppliers_str = suppliers_line.split("Поставщики:")[1].strip()
            suppliers = ast.literal_eval(suppliers_str)
            consumers_str = consumers_line.split("Потребители:")[1].strip()
            consumers = ast.literal_eval(consumers_str)
            n = len(suppliers)
            m = len(consumers)
            matrix_lines = []
            for line in lines[matrix_start:]:
                if line.startswith("===") or not line.strip():
                    break
                matrix_lines.append(line.strip())
            cost = []
            for line in matrix_lines:
                row = [float(x) for x in line.split()]
                cost.append(row)
            # Заполняем поля в окне
            self.n_input.setText(str(n))
            self.m_input.setText(str(m))
            self.create_value_fields()
            for i, value in enumerate(suppliers):
                self.supplier_entries[i].setText(str(value))
            for i, value in enumerate(consumers):
                self.consumer_entries[i].setText(str(value))
            for i in range(n):
                for j in range(m):
                    self.cost_entries[i][j].setText(str(cost[i][j]))
            QtWidgets.QMessageBox.information(self, "Импорт", "Задача успешно импортирована.")
            logging.info("Импорт успешен: suppliers=%s, consumers=%s, cost=%s", suppliers, consumers, cost)
        except Exception as e:
            logging.error("Ошибка при импорте: %s", str(e))
            QtWidgets.QMessageBox.critical(self, "Ошибка импорта", str(e))

    def run_solution(self):
        logging.info("Запуск решения задачи")
        try:
            n = int(self.n_input.text())
            m = int(self.m_input.text())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите корректные положительные числа для n и m.")
            return

        suppliers = []
        consumers = []
        cost = []

        try:
            for entry in self.supplier_entries:
                suppliers.append(float(entry.text()))
            for entry in self.consumer_entries:
                consumers.append(float(entry.text()))
            for i in range(n):
                cost_row = []
                for j in range(m):
                    cost_row.append(float(self.cost_entries[i][j].text()))
                cost.append(cost_row)
        except ValueError:
            logging.error("Ошибка преобразования данных в числовой формат")
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите корректные числовые значения для всех полей.")
            return

        solution_type = self.solution_type_group.checkedId()
        export = self.export_checkbox.isChecked()
        export_format = "txt" if self.radio_txt.isChecked() else "word"

        result = solve_problem(suppliers, consumers, solution_type, cost)
        logging.info("Результат решения получен")

        if export:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить результат", "",
                                                                "Text Files (*.txt);;Word Documents (*.docx)")
            if filename:
                try:
                    self.model.export_result(result, export_format, filename)
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Ошибка экспорта", str(e))
                    return

        result_dialog = ResultDialog(self, result)
        result_dialog.exec()

class GenerateDialog(QtWidgets.QDialog):
    """
    Диалог для генерации задачи.
    Логика:
      - Одна галочка "Только решение" (по умолчанию включена).
      - Если галочка снята -> появляются радио-кнопки "Только ответ" и "Полное решение".
      - Если галочка снова установлена -> радио-кнопки скрываются и не влияют на итог.
    """
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("Генерация задачи")
        self.resize(400, 300)
        self.setMinimumSize(400, 300)
        self.setSizeGripEnabled(True)

        # Основной лейаут диалога
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Создаем QScrollArea для прокрутки содержимого
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)
        
        # Внутренний виджет, содержащий все элементы
        self.inner_widget = QtWidgets.QWidget()
        self.inner_layout = QtWidgets.QVBoxLayout(self.inner_widget)
        self.scroll_area.setWidget(self.inner_widget)

        self.initUI()

    def initUI(self):
        # Ввод количества поставщиков и потребителей
        self.n_label = QtWidgets.QLabel("Количество поставщиков (n):")
        self.n_input = QtWidgets.QLineEdit()
        self.m_label = QtWidgets.QLabel("Количество потребителей (m):")
        self.m_input = QtWidgets.QLineEdit()
        self.inner_layout.addWidget(self.n_label)
        self.inner_layout.addWidget(self.n_input)
        self.inner_layout.addWidget(self.m_label)
        self.inner_layout.addWidget(self.m_input)

        # Галочка "Только решение"
        # По умолчанию установлена (checked = True)
        self.chk_only_solution = QtWidgets.QCheckBox("Только условие")
        self.chk_only_solution.setChecked(True)
        self.chk_only_solution.stateChanged.connect(self.toggle_solution_options)
        self.inner_layout.addWidget(self.chk_only_solution)

        # Группа радио-кнопок, которая видна только если галочка снята
        self.solution_type_group = QtWidgets.QButtonGroup(self)
        self.radio_detail = QtWidgets.QRadioButton("Полное решение")
        self.radio_short = QtWidgets.QRadioButton("Только ответ")
        # По умолчанию выбираем "Полное решение"
        self.radio_detail.setChecked(True)
        self.solution_type_group.addButton(self.radio_detail, 1)
        self.solution_type_group.addButton(self.radio_short, 2)

        # Контейнер для радио-кнопок
        self.solution_options_widget = QtWidgets.QWidget()
        sol_layout = QtWidgets.QVBoxLayout()
        self.solution_options_widget.setLayout(sol_layout)
        sol_layout.addWidget(self.radio_detail)
        sol_layout.addWidget(self.radio_short)

        # Изначально скрываем, так как "Только решение" включено
        self.solution_options_widget.setVisible(False)
        self.inner_layout.addWidget(self.solution_options_widget)

        # Экспорт результата
        self.export_checkbox = QtWidgets.QCheckBox("Экспортировать результат")
        self.export_checkbox.stateChanged.connect(self.toggle_export_options)
        self.inner_layout.addWidget(self.export_checkbox)

        self.export_options_widget = QtWidgets.QWidget()
        export_layout = QtWidgets.QHBoxLayout()
        self.export_options_widget.setLayout(export_layout)
        self.radio_txt = QtWidgets.QRadioButton("txt")
        self.radio_word = QtWidgets.QRadioButton("Word")
        self.radio_txt.setChecked(True)
        export_layout.addWidget(self.radio_txt)
        export_layout.addWidget(self.radio_word)
        self.export_options_widget.setVisible(False)
        self.inner_layout.addWidget(self.export_options_widget)

        # Кнопка для генерации задачи
        self.btn_generate = QtWidgets.QPushButton("Сгенерировать задачу")
        self.btn_generate.clicked.connect(self.run_generation)
        self.inner_layout.addWidget(self.btn_generate)

    def toggle_export_options(self):
        self.export_options_widget.setVisible(self.export_checkbox.isChecked())

    def toggle_solution_options(self):
        """
        Скрываем/показываем радио-кнопки выбора типа решения
        в зависимости от состояния галочки "Только решение".
        """
        checked = self.chk_only_solution.isChecked()
        # Если галочка установлена, прячем радио-кнопки.
        # Если галочка снята, показываем радио-кнопки.
        self.solution_options_widget.setVisible(not checked)

    def run_generation(self):
        # Считываем n и m
        try:
            n = int(self.n_input.text())
            m = int(self.m_input.text())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите корректные положительные числа для n и m.")
            return

        export = self.export_checkbox.isChecked()
        export_format = "txt" if self.radio_txt.isChecked() else "word"

        # Определяем solution_type:
        # Если "Только решение" включено, используем тип решения по умолчанию (здесь = 0, т.е. "Только условие").
        if self.chk_only_solution.isChecked():
            solution_type = 0
        else:
            # Если галочка снята, берём выбор из радио-кнопок:
            #   1 = Полное решение
            #   2 = Только ответ
            solution_type = self.solution_type_group.checkedId()

        # Вызываем решение задачи
        result = solve_problem(n, m, solution_type)

        # Если выбран экспорт, сохраняем результат
        if export:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить результат", "",
                                                                "Text Files (*.txt);;Word Documents (*.docx)")
            if filename:
                try:
                    self.model.export_result(result, export_format, filename)
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Ошибка экспорта", str(e))
                    return

        # Отображаем результат в диалоговом окне
        result_dialog = ResultDialog(self, result)
        result_dialog.exec()

class ResultDialog(QtWidgets.QDialog):
    """
    Диалог для отображения результата.
    """
    def __init__(self, parent, result):
        super().__init__(parent)
        self.setWindowTitle("Результат")
        self.resize(600, 700)
        self.setMinimumSize(400, 300)
        self.setSizeGripEnabled(True)
        self.result = result
        self.initUI()

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Создаем QScrollArea для содержимого результата
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Внутренний виджет, который будет помещен в scroll_area
        content_widget = QtWidgets.QWidget()
        scroll_area.setWidget(content_widget)
        
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        # Используем QTextEdit с включенными полосами прокрутки (по умолчанию они есть)
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setText(self.result)
        content_layout.addWidget(self.result_text)
        
        # Кнопка "Закрыть" добавляется вне области прокрутки
        self.btn_close = QtWidgets.QPushButton("Закрыть")
        self.btn_close.clicked.connect(self.close)
        main_layout.addWidget(self.btn_close)
