from socket import socket, AF_INET, SOCK_STREAM
from Constant import BARRIER_COMMAND, TERMINAL_COMMAND, BARRIERS, SEARCH_DB
import devices as dev

SERV_SOCKET = socket(AF_INET, SOCK_STREAM)

SERV_SOCKET.bind(('', 5020))
SERV_SOCKET.listen(10)

try:
    while True:
        CLIENT_SOCKET, ADDR = SERV_SOCKET.accept()
        DATA = CLIENT_SOCKET.recv(4096)
        client_request = DATA.decode('utf-8')
        print(f"Запрос клиента: {client_request}")

        # СТОЙКА
        if int(client_request[:3]) and int(client_request[:3]) < 215:

            # ПЕРЕЗАГРУЗКА
            if client_request[4:] == BARRIER_COMMAND[0]:
                dev.barrier_device(client_request[:3])
                MSG = f' Идёт перезагрузка устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ТЕСТ СЕТИ
            if client_request[4:] == BARRIER_COMMAND[1]:
                dev.network_test_barrier(client_request[:3])
                MSG = f' Идёт тест сети устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # СБРОС КОРЗИН
            if client_request[4:] == BARRIER_COMMAND[2]:
                layout_en()
                test_pglsvrem()
                dev.reset_tickets(client_request[:3])
                MSG = f' Идёт сброс корзины устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # КОМАНДА 2,3,4 (доделать)
            if client_request[4:] == BARRIER_COMMAND[3]:
                dev.bios_barrier(client_request[:3])
                MSG = f' Выполняется команда 2,3,4 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ОБНОВЛЕНИЕ 94
            if client_request[4:] == BARRIER_COMMAND[4]:
                layout_en()
                test_pglsvrem()
                dev.command_94(client_request[:3])
                MSG = f' Выполняется обновление 94 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # Показать ручные открытия
            if client_request[4:] == BARRIER_COMMAND[5]:
                # dev.command_94(client_request[:3])
                MSG = f' Ручные открытия устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # НЕ РАБОТАЕТ
            if client_request[4:] == BARRIER_COMMAND[6]:
                layout_en()
                test_pglsvrem()
                dev.not_work_bar(client_request[:3])
                MSG = f' Не работает устр-во: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # РАБОТАЕТ
            if client_request[4:] == BARRIER_COMMAND[7]:
                layout_en()
                test_pglsvrem()
                dev.work_bar(client_request[:3])
                MSG = f' В работе устр-во: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # БЛОКИРОВАТЬ
            if client_request[4:] == BARRIER_COMMAND[8]:
                layout_en()
                test_pglsvrem()
                dev.work_bar(client_request[:3])
                MSG = f' Заблокировано устр-во: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # РАЗБЛОКИРОВАТЬ
            if client_request[4:] == BARRIER_COMMAND[9]:
                layout_en()
                test_pglsvrem()
                dev.work_bar(client_request[:3])
                MSG = f' Разблокировано устр-во: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # График СРНЗ по устройству (доделать)
            if client_request[4:] == BARRIER_COMMAND[10]:
                # dev.work_bar(client_request[:3])
                MSG = f' График СРНЗ устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

        # КАССА
        elif int(client_request[:3]) and int(client_request[:3]) > 600:

            # ПЕРЕЗАГРУЗКА
            if client_request[4:] == TERMINAL_COMMAND[0]:
                dev.terminal_device(client_request[:3])
                MSG = f' Идёт перезагрузка устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ТЕСТ СЕТИ
            if client_request[4:] == BARRIER_COMMAND[1]:
                dev.network_test_terminal(client_request[:3])
                MSG = f' Идёт тест сети устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # КОМАНДА 2,3,4 (доделать)
            if client_request[4:] == BARRIER_COMMAND[3]:
                dev.bios_terminal(client_request[:3])
                MSG = f' Выполняется команда 2,3,4 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ОБНОВЛЕНИЕ 94
            if client_request[4:] == BARRIER_COMMAND[4]:
                devices.layout_en()
                devices.test_svrem()
                dev.term_94(client_request[:3])
                MSG = f' Выполняется обновление 94 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ПЕРЕЗАГРУЗКА БТБ
            if client_request[4:] == BARRIER_COMMAND[5]:
                devices.layout_en()
                devices.test_svrem()
                dev.bild_reset(client_request[:3])
                MSG = f' Идёт перезапуск btb устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # X - отчёт
            if client_request[4:] == BARRIER_COMMAND[6]:
                devices.layout_en()
                devices.test_svrem()
                dev.x_report(client_request[:3])
                MSG = f' Идёт снятие x-отчёта устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # Z - отчёт
            if client_request[4:] == BARRIER_COMMAND[7]:
                devices.layout_en()
                devices.test_svrem()
                dev.z_report(client_request[:3])
                MSG = f' Идёт снятие z-отчёта устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # СБРОС ДЕНЕГ
            if client_request[4:] == BARRIER_COMMAND[8]:
                devices.layout_en()
                devices.test_svrem()
                dev.money_down_reset(client_request[:3])
                MSG = f' Сброс денег устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ЗАГРУЗКА ДЕНЕГ
            if client_request[4:] == BARRIER_COMMAND[9]:
                devices.layout_en()
                devices.test_svrem()
                dev.money_up_reset(client_request[:3])
                MSG = f' Загрузка денег устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # СБРОС ОШИБОК 07
            if client_request[4:] == BARRIER_COMMAND[10]:
                devices.layout_en()
                devices.test_svrem()
                dev.comm_07(client_request[:3])
                MSG = f' Сброс ошибок 07 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

            # ВЫХОД cl D
            if client_request[4:] == BARRIER_COMMAND[10]:
                devices.layout_en()
                devices.test_svrem()
                dev.cl_d(client_request[:3])
                MSG = f' Сброс ошибок 07 устр-ва: {client_request[:3]}'
                CLIENT_SOCKET.send(MSG.encode('utf-8'))
                CLIENT_SOCKET.close()

finally:
    SERV_SOCKET.close()
