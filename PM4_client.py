import sys
import os
import time
import keyboard
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import *
import img.xres_rs
from main import *
from datetime import datetime
import devices as dev
import bad_ticket as bt
from pm_tables import search_number_table as snt, search_client_table as sct, device_open_table as dot
from pm_tables import terminal_pay_table as tpt, finance_table as ft, srnz_table as srnz, schedule_srnz as ss


from Constant import BARRIER_COMMAND, TERMINAL_COMMAND, BARRIERS, SEARCH_DB

import client_connect as cc


# Конвертация данных в список
def list_convert(our_str):
    convert_result = our_str.split(',')
    convert_result_2 = []
    for i in convert_result:
        convert_result_2.append(i.split('_'))
    return convert_result_2


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui = Ui_ParkingManager4()
        self.ui.setupUi(self)

        # Инициализируем QSystemTrayIcon иконку в трей со своим дизайном

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.ico'))
        '''
            Объявим и добавим действия для работы с иконкой системного трея
            show - показать окно
            hide - свернуть окно
            exit - выход из программы
        '''
        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Свернуть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Прописываем элементы интерфейса

        self.ui.pushButton_18.clicked.connect(self.terminal_device)
        self.ui.pushButton_21.clicked.connect(self.barrier_device)
        self.ui.pushButton_2.clicked.connect(self.parking_board)
        self.ui.pushButton_23.clicked.connect(self.video)
        self.ui.pushButton_35.clicked.connect(self.manual_opening)
        self.ui.pushButton.clicked.connect(self.bad_ticket)
        self.ui.pushButton_15.clicked.connect(self.reset_time_button)
        self.ui.pushButton_22.clicked.connect(self.status_cliner)
        self.ui.pushButton_13.clicked.connect(self.srnz)
        self.ui.pushButton_17.clicked.connect(self.finance)
        self.ui.pushButton_11.clicked.connect(self.search)
        self.ui.pushButton_27.clicked.connect(self.all_baskets)
        self.ui.pushButton_16.clicked.connect(self.set_email_srnz)
        self.ui.pushButton_19.clicked.connect(self.open)
        self.ui.pushButton_20.clicked.connect(self.close)

        # Ставим любой IP камеры по умолчанию

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.load(QUrl("http://192.168.24.121"))
        self.ui.gridLayout.addWidget(self.browser)

        # Прописываем номера устройств в comboBox

        number_terminal = range(601, 630, 1)

        for i in number_terminal:
            self.ui.comboBox_4.addItem("%s" % i)
            i += 1

        for e in TERMINAL_COMMAND:
            self.ui.comboBox_5.addItem("%s" % e)

        for e in BARRIERS:
            self.ui.comboBox.addItem("%s" % e)

        for e in SEARCH_DB:
            self.ui.comboBox_2.addItem("%s" % e)

        for e in BARRIER_COMMAND:
            self.ui.comboBox_3.addItem("%s" % e)

    # Чистим от других виджетов...

    def clear_layout(self):
        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().deleteLater()

    # функции управления устройствами:

    def terminal_device(self):
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        device = self.ui.comboBox.currentText()
        try:
            if self.ui.comboBox_3.currentText() == "Отслеживание проездов":
                status = cc.client_connect(device + ' ' + self.ui.comboBox_3.currentText())
                table = snt.set_search_number_table(list_convert(status))
                self.ui.gridLayout.addWidget(table, 0, 0)  # Добавляем таблицу
                self.ui.lineEdit_5.setText('Отслеживание проездов стойки: ' + device)
            elif self.ui.comboBox_3.currentText() == "График_СРНЗ":
                status = cc.client_connect(device + ' ' + self.ui.comboBox_3.currentText() + ' ' + value)
                ss.schedule_srnz(device, list_convert(status))
                self.ui.lineEdit_5.setText('График СРНЗ стойки: ' + device)
            else:
                status = cc.client_connect(self.ui.comboBox.currentText() + ' ' + self.ui.comboBox_3.currentText())
                self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    def barrier_device(self):
        try:
            if self.ui.comboBox_5.currentText() == "Отслеживание оплат":
                status = cc.client_connect(self.ui.comboBox_4.currentText() + ' ' + self.ui.comboBox_5.currentText())
                table = tpt.set_term_pay(list_convert(status))
                self.ui.gridLayout.addWidget(table, 0, 0)  # Добавляем таблицу
                self.ui.lineEdit_5.setText('Отслеживание оплат кассы ' + self.ui.comboBox_5.currentText())
            else:
                status = cc.client_connect(self.ui.comboBox_4.currentText() + ' ' + self.ui.comboBox_5.currentText())
                self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # ФУНКЦИИ КНОПОК
    ###################################################################################################################
    # Открыть закрыть шлагбаум

    def open(self):
        device = self.ui.comboBox.currentText()
        try:
            status = cc.client_connect('214 ' + device)
            self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    def close(self):
        device = self.ui.comboBox.currentText()
        try:
            status = cc.client_connect('215 ' + device)
            self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # Сброс всех корзин 216

    def all_baskets(self):
        try:
            status = cc.client_connect('216')
            self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # функции поиска по номеру 217 и клиенту 218

    def search(self):
        search = self.ui.lineEdit_2.text()
        type_search = self.ui.comboBox_2.currentText()
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        print(value, search, type_search)

        if type_search == 'По_номеру' and value <= str(datetime.now().date()) and len(search) > 1:
            request = '217 ' + search + ' ' + value
            try:
                self.ui.lineEdit_5.setText("Запрос данных по номеру!")
                result = cc.client_connect(request)
                table = snt.set_search_number_table(list_convert(result))
                self.ui.gridLayout.addWidget(table, 0, 0)  # Добавляем таблицу
            except:
                self.ui.lineEdit_5.setText("нет связи с сервером или нет запрошенных данных!")

        if type_search == 'По_фамилии' and len(search) > 2:
            request = '218 ' + search
            try:
                self.ui.lineEdit_5.setText("Запрос данных по фамилии!")
                status = cc.client_connect(request)
                status = status.split(',')
                status2 = []
                status2.append(status)
                table = sct.set_search_client_table(status2)
                self.ui.gridLayout.addWidget(table, 0, 0)
            except:
                self.ui.lineEdit_5.setText("нет связи с сервером или нет запрошенных данных!")

    # Функция запроса данных для табло 219
    def parking_board(self):
        request = '219 '
        try:
            status = cc.client_connect(request)
            self.ui.lineEdit_3.setText('    ' + status)
            self.ui.lineEdit_5.setText(f'Сейчас машин на парковке - {status}')
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # Функция ручные открытия 220
    def manual_opening(self):
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        request = '220 ' + value
        self.ui.lineEdit_5.setText(f'Запрос всех ручных открытий')
        try:
            result = cc.client_connect(request)
            table = dot.set_device_open_table(list_convert(result))
            self.ui.gridLayout.addWidget(table, 0, 0)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером или нет запрошенных данных!")

    # Финансовый отчёт
    def finance(self):
        self.ui.lineEdit_5.setText("Запрос финансового отчёта")
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        request = '221 ' + value
        try:
            status = cc.client_connect(request)
            table = ft.finance_table(list_convert(status))
            print(table)
            self.ui.gridLayout.addWidget(table, 0, 0)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # Не читаемый билет
    def bad_ticket(self):
        value = self.ui.timeEdit.dateTime().toString("hh-mm")
        result = bt.bad_ticket(value)
        self.ui.lineEdit_5.setText(result)

    # СРНЗ Таблца
    def srnz(self):
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        request = '222 ' + value
        self.ui.lineEdit_5.setText(f'запрос срнз за: {value}')
        try:
            status = cc.client_connect(request)
            table = srnz.srnz_table(list_convert(status))
            self.ui.gridLayout.addWidget(table, 0, 0)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # Отправка срнз на почту
    def set_email_srnz(self):
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        email = self.ui.lineEdit_4.text()
        request = '223 ' + value + ' ' + email
        try:
            status = cc.client_connect(request)
            self.ui.lineEdit_5.setText(f'отчёт срнз отправлен на почту: {email}')
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # Графики срнз
    def test(self):
        ss.graffic()


    # ДОП ФУНКЦИИ
    ####################################################################################################################
    # очистка экрана
    def clear_layout2(self):
        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().deleteLater()

    def status_cliner(self):
        self.ui.lineEdit_5.setText('')

    # поставить текущее время
    def reset_time_button(self):
        current_date = str(datetime.now().date())
        date_list = current_date.split('-')
        date = self.ui.dateEdit
        d = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        date.setDate(d)

    # Вывод видео на экран
    def video(self):
        d = self.ui.comboBox.currentText()
        d = str(int(d) + 20)
        print(d)
        time.sleep(0.3)
        self.browser.close()
        self.clear_layout2()
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.load(QUrl("http://192.168.24.%s" % d))
        self.ui.gridLayout.addWidget(self.browser)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())



