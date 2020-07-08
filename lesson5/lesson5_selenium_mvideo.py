from selenium import webdriver
import json
from pymongo import MongoClient
import time

# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.mvideo.ru/')

time.sleep(0.5)

elem = driver.find_elements_by_class_name('sel-hits-block ')

hits = elem[1].find_elements_by_class_name('gallery-list-item')
print(len(hits))

for i in range(4):
    button = elem[1].find_element_by_class_name('sel-hits-button-next')
    button.click()
    time.sleep(1)

elem = driver.find_elements_by_class_name('sel-hits-block ')
hits = elem[1].find_elements_by_class_name('sel-product-tile-title')
print(len(hits))

hits_list = []

for item in hits:
    hit_str = item.get_attribute('data-product-info')
    hit_json = json.loads(hit_str)
    hits_list.append(hit_json)

client = MongoClient('localhost', 27017)
db = client['mvideo']
mails_collection = db['hits']
mails_collection.insert_many(hits_list)

print(1)
