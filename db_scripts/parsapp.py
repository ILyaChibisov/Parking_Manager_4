from selenium import webdriver
import time


def pars_app(number):

    url = "https://payparking.ru/ft/1?utm_source=qrindoor&utm_campaign=qrindoor"
    options = webdriver.ChromeOptions()
    options.add_argument("Авиапарк")
    options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path="C:\\chromedriver\\chromedriver",
                              options=options)
    time.sleep(3)

    driver.get(url=url)
    time.sleep(3)
    parking_input = driver.find_element_by_class_name("FindTicket_find_ticket__input__LrpoE")
    parking_input.send_keys(number)
    time.sleep(10)
    button = driver.find_element_by_id("search_button")
    button.click()
    time.sleep(10)

    try:
        info_number = driver.find_element_by_class_name("TicketInfo_ticket_info__acne8")
        result = info_number.text

    except Exception as ex:

        result = 'Нет данных! Проверьте установлен ли драйвер в папку C:\\chromedriver'
    finally:
        driver.close()
        driver.quit()
    return result




