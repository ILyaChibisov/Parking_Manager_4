import sys
# import os
# import time
# import keyboard
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import *
import img.xres_rs
from main import *
from datetime import datetime
# import math
# import devices as dev
# import request_srnz
# import finance as fin
# import avto_in_park as ap
# import device_log as dl
# import xlwt
# import selenium
from pm_tables import search_number_table as snt, search_client_table as sct
from db_scripts import Change_white_list as cwl, searh_card as sc, parsapp

from Constant import BARRIER_COMMAND, TERMINAL_COMMAND, BARRIERS, SEARCH_DB

import client_connect as cc




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
        # self.ui.pushButton_8.clicked.connect(self.tariff_validation)
        # self.ui.pushButton_23.clicked.connect(self.video)
        # self.ui.pushButton_10.clicked.connect(self.srnz)
        # self.ui.pushButton_13.clicked.connect(self.ex_to_main)
        # self.ui.pushButton_15.clicked.connect(self.create_white_list)
        self.ui.pushButton_11.clicked.connect(self.search_number)
        # self.ui.pushButton_12.clicked.connect(self.update_number)
        # self.ui.pushButton_16.clicked.connect(self.fin_table)
        # self.ui.pushButton_17.clicked.connect(self.avto_in)
        # self.ui.pushButton_12.clicked.connect(self.search_client)
        # self.ui.pushButton_19.clicked.connect(self.number_tr)
        # self.ui.pushButton_20.clicked.connect(self.terminal_pay)
        # self.ui.pushButton_21.clicked.connect(self.device_open)
        # self.ui.pushButton_11.clicked.connect(self.srnz_interval)
        # self.ui.pushButton_22.clicked.connect(self.my_clients_tr)
        # self.ui.pushButton_23.clicked.connect(self.del_cl_tr)
        # self.ui.pushButton_24.clicked.connect(self.update)
        # self.ui.pushButton_25.clicked.connect(self.rollback)
        # self.ui.pushButton_27.clicked.connect(self.email)
        # self.ui.pushButton_14.clicked.connect(self.pars_app)

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

        # Установка даты в виджите выбора времени по умолчанию на текущую

        current_date = str(datetime.now().date())
        date_list = current_date.split('-')
        date = self.ui.dateEdit
        date_2 = self.ui.dateEdit

        d = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        date.setDate(d)
        date_2.setDate(d)

    # Чистим от других виджетов...

    def clear_layout(self):
        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().deleteLater()

    # функции управления устройствами:

    def terminal_device(self):
        try:
            status = cc.client_connect(self.ui.comboBox.currentText() + ' ' + self.ui.comboBox_3.currentText())
            self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    def barrier_device(self):
        try:
            status = cc.client_connect(self.ui.comboBox_4.currentText() + ' ' + self.ui.comboBox_5.currentText())
            self.ui.lineEdit_5.setText(status)
        except:
            self.ui.lineEdit_5.setText("нет связи с сервером!")

    # функции поиска по номеру, клиенту , в приложении...

    def search_number(self):
        number = self.ui.lineEdit_2.text()
        convert_number = cwl.convert_number(number)
        value = self.ui.dateEdit.dateTime().toString("yyyy-MM-dd")
        if value <= str(datetime.now().date()):
            number_events = sc.number_tr(value, convert_number)
            table = snt.set_search_number_table(number_events)
            self.ui.gridLayout.addWidget(table, 0, 0)  # Добавляем таблицу

    def search_client(self):
        client_tr = []
        search = self.ui.lineEdit_2.text()
        client_tr = sc.name(search)
        table = sct.set_search_client_table(client_tr)
        self.ui.gridLayout.addWidget(table, 0, 0)

    def pars_app(self):
        search = self.ui.lineEdit_2.text()
        result = parsapp.pars_app(search)
        review = QTextEdit(result)
        self.ui.gridLayout.addWidget(review, 0, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
