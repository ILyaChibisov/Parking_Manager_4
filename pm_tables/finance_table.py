from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main import *


def finance_table(events):
    device = range(601, 630)
    # создаём таблицу для вывода на экран данных
    pay_bank = []
    pay_money = []
    for i in range(len(events)):
        pay_bank.append(int(events[i][0]))
        pay_money.append(int(events[i][1]))

    print(pay_bank)
    print(pay_money)
    table = QTableWidget()  # Создаём таблицу
    table.setColumnCount(4)  # Устанавливаем четыре колонки
    table.setRowCount(30)  # 30 строк в таблице

    # Устанавливаем заголовки таблицы

    table.setHorizontalHeaderLabels(["Касса", "Безналичные", "Наличные", "Итого:"])
    table.verticalHeader().setVisible(False)

    # Выравниваем влево название столбцов

    for i in range(4):
        table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

    # заполняем строки

    for i in range(29):
        table.setItem(i, 0, QTableWidgetItem(str(device[i])))
        table.setItem(i, 1, QTableWidgetItem(str(int(pay_bank[i] / 100))))
        table.setItem(i, 2, QTableWidgetItem(str(int(pay_money[i] / 100))))
        sum_finance = int((pay_bank[i] + pay_money[i]) / 100)
        table.setItem(i, 3, QTableWidgetItem(str(sum_finance)))
    table.setItem(29, 0, QTableWidgetItem(('Итого:')))
    table.setItem(29, 1, QTableWidgetItem(str(int(sum(pay_bank) / 100))))
    table.setItem(29, 2, QTableWidgetItem(str(int(sum(pay_money) / 100))))
    table.setItem(29, 3, QTableWidgetItem(str(int(sum(pay_bank) / 100 + sum(pay_money) / 100))))

    # делаем ресайз колонок по содержимому

    table.resizeColumnsToContents()
    table.updateGeometry()

    # масштабируем таблицу
    # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    return table


if __name__ == "__main__":
    main()
