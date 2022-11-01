import cx_Oracle
import datetime

my_clients = ["H472OO750", "Y946XY799", "K215XM750", "T555EH97", "H882BB799", "H103YC799"]
old_clients = ["C742KA797", "K950HB799", "K215KE797", "E554TB799", "К882ЕТ797", "K103KC797"]


def change_white_list():
    result = []
    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()
        request_str = 'SELECT LPN FROM car_sharing'
        c.execute(request_str)
        for row in c:
            result.append(*row)
        conn.close()

    except cx_Oracle.DatabaseError:
        result.append('База данных не доступна!')

    return result


def search_number(number_avto):
    result = []

    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()
        request_str = "SELECT LPN FROM car_sharing WHERE LPN LIKE '%" + number_avto + "%'"
        c.execute(request_str)
        for row in c:
            result.append(*row)
        conn.close()
        if not result:
            result.append('Данного номера нет в списке!')
    except cx_Oracle.DatabaseError:
        result.append('База данных не доступна!')

    return result


def convert_number(number_avto):
    new_number = []
    convert_rus_big = 'АВЕКМНОРСТУХ'
    convert_rus_lit = 'авекмнорстух'
    convert_eng = 'ABEKMHOPCTYX'
    digit = '0123456789'
    for number in number_avto:
        if number in convert_eng:
            new_number.append(number)
        elif number in convert_rus_big:
            for i in range(len(convert_rus_big)):
                if number == convert_rus_big[i]:
                    new_number.append(convert_eng[i])
        elif number in convert_rus_lit:
            for i in range(len(convert_rus_lit)):
                if number == convert_rus_lit[i]:
                    new_number.append(convert_eng[i])
        elif number in digit:
            for i in range(len(digit)):
                if number == digit[i]:
                    new_number.append(digit[i])
        else:
            pass

    new_number_str = ''.join(new_number)

    return new_number_str


def update_number(number, new_number):
    result = []

    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()
        request_str = "UPDATE car_sharing set LPN = '" + new_number + "' where LPN = '" + number + "'"
        c.execute(request_str)
        conn.commit()
        result.append('Номер успешно записан!')
        conn.close()
    except cx_Oracle.DatabaseError:
        result.append('Не удалось подключится к базе данных!')

    return result

# переписывает транзакции проездов


def rewrite_my_clients(date1, number):
    date = str(datetime.date.today())
    date_list = date.split('-')
    today = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    now = str(today)
    tomorrow = str(today + datetime.timedelta(days=1))
    year = date_list[0]
    month = date_list[1]

    date_list = date1.split('-')
    today1 = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    tomorrow1 = str(today + datetime.timedelta(days=1))
    year1 = date_list[0]
    month1 = date_list[1]
    result1 = []

    i = my_clients.index(number)



    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()
        request_str = "UPDATE udbidentdata_" + year + "M" + month1 + \
                      " set clicenseplate ='" + old_clients[i] + "' WHERE clicenseplate like '%" + my_clients[i] + "%'" \
                      " and tactiontime < TO_DATE('" + now + "', 'YYYY/MM/DD') "
        c.execute(request_str)
        conn.commit()
        conn.close()
    except cx_Oracle.DatabaseError:
        print('Не удалось подключится к базе данных!')

# переписать старые авто на моих клиентов


def update_db():
    result = []

    for i in range(len(my_clients)):
        try:
            dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
            conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
            c = conn.cursor()
            request_str = "UPDATE car_sharing set LPN = '" + my_clients[i] + "' where LPN = '" + old_clients[i] + "'"
            c.execute(request_str)
            conn.commit()
            result.append('Номер успешно записан!')
            conn.close()
        except cx_Oracle.DatabaseError:
            result.append(my_clients[i] + ' номер не записан!')

    return result

# перезаписываем транзакции новых клиентов на старые по месяцам и дням


def update_by_time(number, date):

    index = my_clients.index(number)
    # date = str(datetime.date.today())
    date_list = date.split('-')
    today = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    now = str(today)
    tomorrow = str(today + datetime.timedelta(days=1))
    year = date_list[0]
    month = date_list[1]
    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()
        request_str = "UPDATE udbidentdata_" + year + "M" + month + \
                      " set clicenseplate ='" + old_clients[index] + "' WHERE clicenseplate like '%" + my_clients[index] + "%'" \
                      " and tactiontime < TO_DATE('" + tomorrow + "', 'YYYY/MM/DD') "
        c.execute(request_str)
        conn.commit()
        conn.close()
    except cx_Oracle.DatabaseError:
        print('Не удалось подключится к базе данных!')

# переписать обратно на старых клиентов


def rollback_db():
    result = []

    for i in range(len(my_clients)):
        try:
            dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
            conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
            c = conn.cursor()
            request_str = "UPDATE car_sharing set LPN = '" + old_clients[i] + "' where LPN = '" + my_clients[i] + "'"
            c.execute(request_str)
            conn.commit()
            result.append('Номер успешно записан!')
            conn.close()
        except cx_Oracle.DatabaseError:
            result.append(old_clients[i] + ' номер не записан!')

    return result




if __name__ == '__menu__':
    menu()

