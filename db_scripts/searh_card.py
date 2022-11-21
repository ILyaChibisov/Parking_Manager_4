import cx_Oracle
import datetime


# поиск клиентов по имени
def name(name):
    result = []

    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()

        request_str = "select ccardno,linvcaddrref,clastname,clicenceno,xvalendtimest FROM pt_pta_h where " \
                      "(clastname like '%" + name + "%' or ccardno like '%" + name + "%' or clicenceno like '%" + name + "%')" \
                        " ORDER BY lastchangedate DESC "

        c.execute(request_str)
        i = 0
        for row in c:
            i += 1
            if i < 2:
                result.append(row)
            else:
                break

        for i in range(len(result)):
            result[i] = list(result[i])

        conn.close()
        if len(result) == 1:
            result[0][1] = str(result[0][1])
            result[0][4] = str(result[0][4])
            if result[0][3] == None:
                result[0][3] = "нет"
        else:
            result = [['нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных']]

    except cx_Oracle.DatabaseError:
        print('База данных не доступна!')

    return result


# поиск по дате и номеру
def number_tr(date, number):
    number = convert_number(number)
    date_list = date.split('-')
    today = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    tomorrow = str(today + datetime.timedelta(days=1))
    year = date_list[0]
    month = date_list[1]
    result = []

    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()

        request_str = "SELECT  tactiontime, sdevice, clicenseplate " \
                      "FROM udbidentdata_" + year + "M" + month + " WHERE (clicenseplate like '%" + number + "%') ORDER BY tactiontime DESC"
        c.execute(request_str)

        for row in c:
            result.append(row)

        for i in range(len(result)):
            result[i] = list(result[i])
        conn.close()

    except cx_Oracle.DatabaseError:
        return 'Не удалось подключится к базе данных!'

    if len(result) > 0:
        result = replay(result)
        for i in range(len(result)):
            result[i] = str(result[i][0]) + '_' + str(result[i][1]) + '_' + str(result[i][2])

        result_str = ','.join(result[:100])
    else:
        result_str = 'нет данных_нет данных_нет данных'

    return result_str


# валидация введенного номера
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


# удаление повторов
def replay(transactions):
    temp = []
    for x in transactions:
        if x not in temp:
            temp.append(x)
    transactions = temp
    return transactions


if __name__ == '__menu__':
    menu()


