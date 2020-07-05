from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests
from datetime import datetime, date, time, timedelta

# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД

client = MongoClient('localhost', 27017)
db = client['data_mining']

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def request_to_yandex_news():
    news_list = []
    main_link = 'https://yandex.ru'
    response = requests.get(f'{main_link}/news/', headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath("//h2[@class = 'story__title']")
    for n in news:
        news_dict = {}
        source_datetime = n.xpath("../../div[@class='story__info']/div[@class='story__date']/text()")
        if 'вчера' in source_datetime[0]:
            news_dict['source'] = source_datetime[0][:-14]
            news_dict['date'] = (date.today() + timedelta(days=-1)).isoformat()
            news_dict['time'] = time.fromisoformat(source_datetime[0][-5:]).isoformat()
        else:
            news_dict['source'] = source_datetime[0][:-6]
            news_dict['date'] = date.today().isoformat()
            news_dict['time'] = time.fromisoformat(source_datetime[0][-5:]).isoformat()
        news_dict['title'] = n.xpath("./a/text()")
        news_dict['href'] = main_link + n.xpath("./a/@href")[0]
        news_list.append(news_dict)
    return news_list

def request_to_lenta_news():
    news_list = []
    main_link = 'https://lenta.ru'
    response = requests.get(f'{main_link}', headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[contains(@class,'item')]/a")
    i = 0
    for n in news:
        news_dict = {}
        if i == 0 :
            news_dict['source'] = 'Lenta.ru'
            news_dict['title'] = n.xpath('../h2/a/text()')
            news_dict['href'] = main_link + n.xpath('../h2/a/@href')[0]
            news_dict['date'] = n.xpath('../h2/a/time/@datetime')[0].split(',')[1][2:]
            news_dict['time'] = n.xpath('../h2/a/time/@datetime')[0].split(',')[0][1:]
            news_list.append(news_dict)
            i = 1
        else:
            news_dict['source'] = 'Lenta.ru'
            news_dict['title'] = n.xpath('text()')
            news_dict['href'] = main_link + n.xpath('@href')[0]
            news_dict['date'] = n.xpath('time/@datetime')[0].split(',')[1][2:]
            news_dict['time'] = n.xpath('time/@datetime')[0].split(',')[0][1:]
            news_list.append(news_dict)
    return news_list

#get first 4 news
def request_to_mail_news():
    news_list = []
    main_link = 'https://news.mail.ru'
    response = requests.get(f'{main_link}', headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath("//li[@class='list__item']")
    i = 0
    for n in news:
        if i < 4:
            news_dict = {}
            news_dict['href'] = main_link + n.xpath('a/@href')[0]
            news_dict['title'] = n.xpath('a/text()')
            inner_response = requests.get(f'{news_dict["href"]}', headers=header)
            inner_dom = html.fromstring(inner_response.text)
            news_dict['date'] = inner_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].split('T')[0]
            news_dict['time'] = inner_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0].split('T')[1]
            news_dict['source'] = inner_dom.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")
            news_list.append(news_dict)
            i += 1
    return news_list

news_yandex_list = request_to_yandex_news()
news_lenta_list = request_to_lenta_news()
news_mail_list = request_to_mail_news()


yandex_news = db.yandex_news
lenta_news = db.lenta_news
mail_news = db.mail_news

yandex_news.delete_many({})
lenta_news.delete_many({})
mail_news.delete_many({})

yandex_news.insert_many(news_yandex_list)
lenta_news.insert_many(news_lenta_list)
mail_news.insert_many(news_mail_list)

print(1)