from socket import socket, AF_INET, SOCK_STREAM
from Constant import BARRIER_COMMAND, TERMINAL_COMMAND, BARRIERS, SEARCH_DB
import devices as dev
from db_scripts import parking_tracking as pt, searh_card as sc, parking_board as pb, open_barrier as ob, finance as fin, srnz as sr
import time
from datetime import datetime
import json


SERV_SOCKET = socket(AF_INET, SOCK_STREAM)

SERV_SOCKET.bind(('', 5020))
SERV_SOCKET.listen(10)

try:
    while True:
        CLIENT_SOCKET, ADDR = SERV_SOCKET.accept()
        DATA = CLIENT_SOCKET.recv(8192)
        client_request = DATA.decode('utf-8')
        print(f"Запрос клиента: {client_request}")

        # СТОЙКА
        if int(client_request[:3]) and int(client_request[:3]) < 213:

            # ПЕРЕЗАГРУЗКА
            if client_request[4:] == BARRIER_COMMAND[0]:
                MSG = f' Идёт перезагрузка стойки: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.barrier_device(client_request[:3])

            # ТЕСТ СЕТИ
            if client_request[4:] == BARRIER_COMMAND[1]:
                result = dev.ping_test_barrier(client_request[:3])
                if 'Reply from' in result:
                    MSG = f' Стойка: {client_request[:3]} в сети!'
                else:
                    MSG = f' Пропала сеть на стойке: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # СБРОС КОРЗИН
            if client_request[4:] == BARRIER_COMMAND[2]:
                MSG = f' Идёт сброс корзины стойки: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.reset_tickets(client_request[:3])

            # КОМАНДА 2,3,4 (проверить)
            if client_request[4:] == BARRIER_COMMAND[3]:
                MSG = f' Выполняется команда 2,3,4 на стойке: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.bios_barrier(client_request[:3])

            # ОБНОВЛЕНИЕ 94
            if client_request[4:] == BARRIER_COMMAND[4]:
                MSG = f' Выполняется обновление 94 стойки: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.command_94(client_request[:3])

            # НЕ РАБОТАЕТ
            if client_request[4:] == BARRIER_COMMAND[5]:
                MSG = f' Не работает стойка: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.not_work_bar(client_request[:3])

            # РАБОТАЕТ
            if client_request[4:] == BARRIER_COMMAND[6]:
                MSG = f' В работе стойка: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.work_bar(client_request[:3])

            # БЛОКИРОВАТЬ
            if client_request[4:] == BARRIER_COMMAND[7]:
                MSG = f' Заблокирована стойка: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.work_bar(client_request[:3])

            # РАЗБЛОКИРОВАТЬ
            if client_request[4:] == BARRIER_COMMAND[8]:
                MSG = f' Разблокирована стойка: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_pglsvrem()
                dev.work_bar(client_request[:3])

            # ОТСЛЕЖИВАНИЕ ПРОЕЗДОВ
            if client_request[4:] == BARRIER_COMMAND[9]:
                MSG = pt.parking_tracking(client_request[:3])
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # График СРНЗ по устройству
            if client_request[4:15] == BARRIER_COMMAND[10]:
                Cl_MSG = client_request.split(' ')
                MSG = sr.schedule_srnz(Cl_MSG[0], Cl_MSG[2])
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

        # КАССА
        elif int(client_request[:3]) and int(client_request[:3]) > 600:

            # ПЕРЕЗАГРУЗКА
            if client_request[4:] == TERMINAL_COMMAND[0]:
                MSG = f' Идёт перезагрузка кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.terminal_device(client_request[:3])

            # ТЕСТ СЕТИ
            if client_request[4:] == TERMINAL_COMMAND[1]:
                result = dev.ping_test_terminal(client_request[:3])
                if 'Reply from' in result:
                    MSG = f' Касса: {client_request[:3]} в сети!'
                else:
                    MSG = f' Пропала сеть на кассе: {client_request[:3]}!'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()


            # КОМАНДА 2,3,4
            if client_request[4:] == TERMINAL_COMMAND[2]:
                MSG = f' Выполняется команда 2,3,4 на кассе: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.bios_terminal(client_request[:3])

            # ОБНОВЛЕНИЕ 94
            if client_request[4:] == TERMINAL_COMMAND[3]:
                MSG = f' Выполняется команда 94 на кассе: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.term_94(client_request[:3])

            # ПЕРЕЗАГРУЗКА БТБ
            if client_request[4:] == TERMINAL_COMMAND[4]:
                MSG = f' Идёт перезапуск btb кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.bild_reset(client_request[:3])

            # X - отчёт
            if client_request[4:] == TERMINAL_COMMAND[5]:
                MSG = f' Идёт снятие x-отчёта кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.x_report(client_request[:3])

            # Z - отчёт
            if client_request[4:] == TERMINAL_COMMAND[6]:
                MSG = f' Идёт снятие z-отчёта кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.z_report(client_request[:3])

            # СБРОС ДЕНЕГ
            if client_request[4:] == TERMINAL_COMMAND[7]:
                MSG = f' Сброс денег кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.money_down_reset(client_request[:3])

            # ЗАГРУЗКА ДЕНЕГ
            if client_request[4:] == TERMINAL_COMMAND[8]:
                MSG = f' Загрузка денег в кассу: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.money_up_reset(client_request[:3])

            # СБРОС ОШИБОК 07
            if client_request[4:] == TERMINAL_COMMAND[9]:
                MSG = f' Сброс ошибок 07 кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.comm_07(client_request[:3])

            # ВЫХОД cl D
            if client_request[4:] == TERMINAL_COMMAND[10]:
                MSG = f' Выход из тех. режима кассы: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()
                dev.layout_en()
                dev.test_svrem()
                dev.cl_d(client_request[:3])

            # ОТСЛЕЖИВАНИЕ ОПЛАТ
            if client_request[4:] == TERMINAL_COMMAND[11]:
                print(client_request[4:])
                MSG = fin.terminal_pay(client_request[:3])
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # Другие команды

        # Открыть шлагбаум
        elif int(client_request[:3]) and int(client_request[:3]) == 214:
            MSG_Cl = client_request.split()
            MSG = f' Открытие шлагбаума стойки: {MSG_Cl[1]}'
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()
            dev.layout_en()
            dev.test_svrem()
            dev.open_bar(MSG_Cl[1])

        # Закрыть шлагбаум
        elif int(client_request[:3]) and int(client_request[:3]) == 215:
            MSG_Cl = client_request.split()
            MSG = f' Закрытие шлагбаума стойки: {MSG_Cl[1]}'
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()
            dev.layout_en()
            dev.test_svrem()
            dev.close_bar(MSG_Cl[1])

        # Сброс всех корзин 216
        elif int(client_request[:3]) and int(client_request[:3]) == 216:
            MSG = f' Идёт сброс всех корзин на выездных стойках'
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()
            dev.layout_en()
            dev.test_svrem()
            time.sleep(1.0)
            for barrier in BARRIERS[10:]:
                dev.reset_tickets(barrier)

        # Поиск по номеру 217
        elif int(client_request[:3]) and int(client_request[:3]) == 217:
            MSG_Cl = client_request.split()
            MSG = sc.number_tr(MSG_Cl[2], MSG_Cl[1])
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # Поиск по фамилии 218
        elif int(client_request[:3]) and int(client_request[:3]) == 218:
            MSG_Cl = client_request.split()
            search = MSG_Cl[1]
            client_tr = sc.name(search)

            MSG = ','.join(client_tr[0])
            print(MSG)
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # Значение на табло свободных мест 219
        elif int(client_request[:3]) and int(client_request[:3]) == 219:
            MSG = pb.parking_board()
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # Статистика открытия шлагбаумов 220
        elif int(client_request[:3]) and int(client_request[:3]) == 220:
            MSG = ob.open_bar(client_request[4:])
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # Финансовый отчёт 221
        elif int(client_request[:3]) and int(client_request[:3]) == 221:
            MSG_Cl = client_request.split()
            date = MSG_Cl[1]
            MSG = fin.finance(date)
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # СРНЗ 222
        elif int(client_request[:3]) and int(client_request[:3]) == 222:
            MSG_Cl = client_request.split()
            date = MSG_Cl[1]
            MSG = sr.request_srnz(date)
            CLIENT_SOCKET.send(MSG.encode('utf-8'))
            CLIENT_SOCKET.close()

        # СРНЗ на почту 223
        elif int(client_request[:3]) and int(client_request[:3]) == 223:
            MSG_Cl = client_request.split()
            date = MSG_Cl[1]
            email = MSG_Cl[2]
            CLIENT_SOCKET.close()
            sr.srnz_to_email(date, email)


finally:
    SERV_SOCKET.close()
