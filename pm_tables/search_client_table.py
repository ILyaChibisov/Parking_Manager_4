from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main import *


def set_search_client_table(events):
    table = QTableWidget()  # Создаём таблицу
    table.setColumnCount(5)  # Устанавливаем  колонки
    table.setRowCount(len(events))  # строк в таблице

    # Устанавливаем заголовки таблицы

    table.setHorizontalHeaderLabels(["Карта", "Компания", "ФИО", "Авто", " Срок Действия"])
    table.verticalHeader().setVisible(False)

    # Выравниваем влево название столбцов

    # for i in range(5):
    #     table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

    # заполняем строки

    for i in range(len(events)):
        table.setItem(i, 0, QTableWidgetItem(str(events[i][0])))
        table.setItem(i, 1, QTableWidgetItem(str(events[i][1])))
        table.setItem(i, 2, QTableWidgetItem(str(events[i][2])))
        table.setItem(i, 3, QTableWidgetItem(str(events[i][3])))
        table.setItem(i, 4, QTableWidgetItem(str(events[i][4])))

    # делаем ресайз колонок по содержимому

    table.resizeColumnsToContents()
    table.updateGeometry()

    # масштабируем таблицу
    # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


if __name__ == "__main__":
    main()
