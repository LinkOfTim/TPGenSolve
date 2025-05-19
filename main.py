# main.py

import sys
import logging
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from view import MainWindow
from docx import Document
from transportation_model import solve_problem

class ModelWrapper:
    def solve_transportation(self, suppliers, consumers, cost, solution_type):
        logging.info("Выбрано подробное решение")
        return solve_problem(suppliers=suppliers, consumers=consumers, solution_type=solution_type, cost=cost) 

    def generate_problem(self, n, m, solution_type):
        logging.info("Генерация проблемы: n=%s, m=%s", n, m)
        return solve_problem(n, m, solution_type)

    def export_result(self, result, export_format, filename):
        logging.info("Экспорт результата в формате %s, файл: %s", export_format, filename)
        if export_format == "txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
        elif export_format == "word":
            doc = Document()
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
