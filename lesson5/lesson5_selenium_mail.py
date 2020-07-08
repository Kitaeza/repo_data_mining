from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
import time

# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://mail.ru')

sleep = 1

time.sleep(sleep)

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

time.sleep(sleep)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

time.sleep(sleep + 2)

mail_list = []

main_link = 'https://e.mail.ru'

while True:
    elem = driver.find_elements_by_class_name('js-letter-list-item')
    for e in elem:
        mail = {}
        mail['from'] = e.find_element_by_class_name('ll-crpt').get_attribute('title')
        mail['date'] = e.find_element_by_class_name('llc__item_date').get_attribute('title')
        mail['title'] = e.find_element_by_class_name('ll-sj__normal').text
        mail['href'] = e.get_attribute('href')
        if mail['href'] not in [m['href'] for m in mail_list]:
            mail_list.append(mail)
            print(mail)
        if e == elem[-1]:
            actions = ActionChains(driver)
            actions.move_to_element(e)
            actions.perform()
            print('last_element_in_block')
            #не разобрался почему не находит последнее письмо в ящике
    if len(driver.find_elements_by_class_name('list-letter-spinner_hidden')) > 0:
        break

#раелизация входа в тело письма, но без реализации функционала парсинга текста
for mail in mail_list:
    driver.get(mail['href'])
    try:
        time.sleep(0.5)
        elem = driver.find_element_by_class('html-expander')
    except:
        continue

driver.quit()

client = MongoClient('localhost', 27017)
db = client['mailru_mails']
mails_collection = db['mails']
mails_collection.insert_many(mail_list)




