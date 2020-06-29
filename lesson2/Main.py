import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from functions import hh_vacancies

page = 0;

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept':'*/*',
         }

params = {
    'clusters': 'true',
    'enable_snippets':'true',
    'salary':'',
    'st':'searchVacancy',
    'text':'data scientist',
    'fromSearch':'true',
    'page':f'{page}',
         }

main_link = 'https://hh.ru/search/vacancy'

hh_vacancies_page = []

response = requests.get(main_link, headers=header, params=params).text

if bs(response, 'lxml').find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText() != 'дальше':
    soup = bs(response, 'lxml')
    hh_vacancy_page_block = soup.find('div', {'class': 'vacancy-serp'})
    hh_vacancies_list = hh_vacancy_page_block.find_all('div', {'class': 'vacancy-serp-item'})
    hh_vacancies_page.append(hh_vacancies_list)
else:
    soup = bs(response, 'lxml')
    pages = soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})[-1]['data-page']
    for p in range(int(pages) + 1):
        params['page'] = p
        response = requests.get(main_link, headers=header, params=params).text
        soup = bs(response, 'lxml')
        hh_vacancy_page_block = soup.find('div', {'class': 'vacancy-serp'})
        hh_vacancies_list = hh_vacancy_page_block.find_all('div', {'class': 'vacancy-serp-item'})
        hh_vacancies_page.append(hh_vacancies_list)

hh_vacancies_list_pages = []

for p in hh_vacancies_page:
    hh_vacancies_list_pages.append(hh_vacancies(p))

hh_vacancies_list = []

for p in hh_vacancies_list_pages:
    for v in p:
        hh_vacancies_list.append(v)

hh_data_frame = pd.DataFrame(hh_vacancies_list)

hh_data_frame.to_pickle('hh_vacancies_df.pkl')

print(1)



