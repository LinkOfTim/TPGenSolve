# main.py

import sys
import logging
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from view import MainWindow

class ModelWrapper:
    def solve_transportation(self, suppliers, consumers, cost, solution_type):
        if solution_type == 1:
            logging.info("Выбрано подробное решение")
            from transportation_model import detailed_solution
            return detailed_solution.solve_transportation_detailed(suppliers, consumers, cost)
        elif solution_type == 2:
            logging.info("Выбран краткий итог решения")
            from transportation_model import final_solution
            return final_solution.solve_transportation_final(suppliers, consumers, cost)
        else:
            logging.info("Выведены только условия")
            from transportation_model import conditions
            problem = {"suppliers": suppliers, "consumers": consumers, "cost": cost}
            return conditions.format_conditions(problem)
    
    def generate_problem(self, n, m):
        logging.info("Генерация проблемы: n=%s, m=%s", n, m)
        from transportation_model import generation
        return generation.generate_random_problem(n, m)
    
    def export_result(self, result, export_format, filename):
        logging.info("Экспорт результата в формате %s, файл: %s", export_format, filename)
        if export_format == "txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
        elif export_format == "word":
            try:
                from docx import Document
            except ImportError:
                logging.error("Библиотека python-docx не установлена.")
                raise ImportError("Библиотека python-docx не установлена.")
            doc = Document()
            # Можно доработать, чтобы вставлять таблицы
            doc.add_paragraph(result)
            doc.save(filename)
        else:
            logging.error("Неподдерживаемый формат экспорта: %s", export_format)
            raise ValueError("Неподдерживаемый формат экспорта")

def main():
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Приложение запущено.")
    
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("app_icon.ico"))
    model = ModelWrapper()
    main_window = MainWindow(model)
    main_window.show()
    
    exit_code = app.exec()
    logging.info("Приложение закрыто.")
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
