from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main import *


def set_search_number_table(events):
    table = QTableWidget()  # Создаём таблицу
    table.setColumnCount(3)  # Устанавливаем  колонки
    table.setRowCount(len(events))  # строки в таблице

    # Устанавливаем заголовки таблицы

    table.setHorizontalHeaderLabels(["Время", "Уст-во", "Номер"])
    table.verticalHeader().setVisible(False)

    # Выравниваем влево название столбцов

    for i in range(3):
        table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

    # заполняем строки

    for i in range(len(events)):
        table.setItem(i, 0, QTableWidgetItem(str(events[i][0])))
        table.setItem(i, 1, QTableWidgetItem(str(events[i][1])))
        table.setItem(i, 2, QTableWidgetItem(str(events[i][2])))

    # делаем ресайз колонок по содержимому

    table.resizeColumnsToContents()
    table.updateGeometry()

    # масштабируем таблицу
    # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


if __name__ == "__main__":
    main()
