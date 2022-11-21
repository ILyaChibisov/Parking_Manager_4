from datetime import datetime
import math


def bad_ticket(value):
    """
    Расчет тарифов буднего и выходного дня по времени въезда, исключаем неправильный ввод данных...
    """
    now = datetime.now()
    time_h = int(now.strftime("%H"))
    time_m = int(now.strftime("%M"))

    try:
        hour = int(value[:2])
        minutes = int(value[3:])
        if (0 <= hour <= 23) and (0 <= minutes <= 59) \
                and (hour <= time_h) or (hour == time_h and minutes <= time_m):
            time_park2free = math.ceil(((time_h * 60 + time_m) - (hour * 60 + minutes + 120)) / 60) * 50
            if time_park2free < 0:
                time_park2free = 0
            time_park = math.ceil(((time_h * 60 + time_m) - (hour * 60 + minutes)) / 60) * 50
            if math.ceil((time_h * 60 + time_m) - (hour * 60 + minutes)) <= 20:
                time_park = 0
            a = 'бдн-' + str(time_park2free) + ' руб, '
            b = 'вых-' + str(time_park) + ' руб, '
            c = 'время: ' + str(math.ceil(((time_h * 60 + time_m) - (hour * 60 + minutes))) // 60) + 'ч ' + str(
                math.ceil(((time_h * 60 + time_m) - (hour * 60 + minutes))) % 60) + 'мин'

        else:
            return "Ошибка"
    except ValueError:
        return "Ошибка"
    return a + b + c
