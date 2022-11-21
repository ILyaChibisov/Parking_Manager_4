import cx_Oracle
import datetime


# поиск по дате и номеру
def parking_tracking(device):
    date = str(datetime.date.today())
    date_list = date.split('-')
    today = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    now = str(today)
    year = date_list[0]
    month = date_list[1]
    result = []

    try:
        dsn = cx_Oracle.makedsn('192.168.24.2', '1521', service_name='orcl')
        conn = cx_Oracle.connect(user='db', password='db', dsn=dsn)
        c = conn.cursor()

        request_str = "SELECT  tactiontime, sdevice, clicenseplate " \
                      "FROM udbidentdata_" + year + "M" + month + " WHERE (sdevice like '%" + device + "%'" \
                      " and tactiontime > TO_DATE('" + now + "', 'YYYY/MM/DD')) ORDER BY tactiontime DESC"
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
        result_str1 = result_str.replace('None', 'нет')

    else:
        result_str1 = 'нет данных_нет данных_нет данных'

    return result_str1


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
