from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main import *

device = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 113, 201, 202, 203, 204, 205, 206, 207, 208, 209,
          210, 211, 212]


def srnz_table(srnz):

    my_srnz_nolpn = srnz[0]
    my_srnz_good = srnz[1]


    # создаём таблицу для вывода на экран данных

    table = QTableWidget()  # Создаём таблицу
    table.setColumnCount(4)  # Устанавливаем четыре колонки
    table.setRowCount(len(device))  # 24 строки в таблице

    # Устанавливаем заголовки таблицы

    table.setHorizontalHeaderLabels(["Уст-во", "Проезды", "Не Расп.", " % Не Расп."])
    table.verticalHeader().setVisible(False)


    # Устанавливаем выравнивание на заголовки

    table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
    table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
    table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
    # table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignRight)
    # заполняем строки

    for i in range(len(device)):
        table.setItem(i, 0, QTableWidgetItem(str(device[i])))
        # if i <= len(my_srnz_good) - 1:
        table.setItem(i, 1, QTableWidgetItem(str(my_srnz_good[i])))
        table.setItem(i, 2, QTableWidgetItem(str(my_srnz_nolpn[i])))
        if my_srnz_good[i] == 0:
            my_srnz_good[i] = 1  # избегаем деления на ноль
        present_nolpn = round(float(my_srnz_nolpn[i]) / (float(my_srnz_good[i]) / 100), 2)
        table.setItem(i, 3, QTableWidgetItem(str(present_nolpn)))


    # делаем ресайз колонок по содержимому

    table.resizeColumnsToContents()
    table.updateGeometry()

    # масштабируем таблицу
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    return table
