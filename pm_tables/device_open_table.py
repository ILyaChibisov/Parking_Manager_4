from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main import *


def set_device_open_table(result):
    # создаём таблицу для вывода на экран данных

    table = QTableWidget()  # Создаём таблицу
    table.setColumnCount(2)  # Устанавливаем 2 колонки
    table.setRowCount(len(result))  # строки в таблице

    # Устанавливаем заголовки таблицы

    table.setHorizontalHeaderLabels(["Время", "Устройство"])
    table.verticalHeader().setVisible(True)

    # Выравниваем влево название столбцов

    # for i in range(2):
    #     table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)

    # заполняем строки

    for i in range(len(result)):
        table.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
        table.setItem(i, 1, QTableWidgetItem(str(result[i][1])))

    # делаем ресайз колонок по содержимому

    table.resizeColumnsToContents()
    table.updateGeometry()

    # масштабируем таблицу
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


if __name__ == "__main__":
    main()
