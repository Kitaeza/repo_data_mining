from pymongo import MongoClient
from pprint import pprint
import pickle

currency_dict = {
    'RUB' : 1,
    'USD' : 70.4413,
    'KZT' : 17.4099,
    'EUR' : 78.9929,
    'BEL_RUB' : 29.2106,
}

vacancies_hh_list = []

with open('hh_vacancies_list.pkl', 'rb') as f:
    vacancies_hh_list = pickle.load(f)

client = MongoClient('localhost', 27017)
db = client['data_mining']

vacancies_hh = db.vacancies_hh

vacancies_hh.delete_many( { } )
vacancies_hh.insert_many(vacancies_hh_list)
print(vacancies_hh.count_documents({}))


#Select vacancies with exact salary

wish_salary = 13000

suitable_vacations = []

for v in vacancies_hh.find({}):
    if v['min_salary'] != '' and v['max_salary'] != '':
        if v['currency'] != '':
            if (int(v['min_salary']) * currency_dict[v['currency']] < wish_salary) and (int(v['max_salary']) * currency_dict[v['currency']] > wish_salary):
                suitable_vacations.append(v)
                continue
        if int(v['min_salary']) < wish_salary and int(v['max_salary']) > wish_salary:
                suitable_vacations.append(v)
                continue
    if v['min_salary'] != '' and v['max_salary'] == '':
        if v['currency'] != '':
            if int(v['min_salary']) * currency_dict[v['currency']] < wish_salary:
                suitable_vacations.append(v)
                continue
        if int(v['min_salary']) < wish_salary:
            suitable_vacations.append(v)
            continue
    if v['max_salary'] != '' and v['min_salary'] == '':
        if v['currency'] != '':
            if int(v['max_salary']) * currency_dict[v['currency']] > wish_salary:
                suitable_vacations.append(v)
                continue
        if int(v['max_salary']) > wish_salary:
            suitable_vacations.append(v)
            continue
    # if w/o salary needed
    #if v['min_salary'] == '' and v['min_salary'] == '' : suitable_vacations.append(v)


# Delete from db documents with vacancy name 'Data scientist'
vacancies_hh.delete_many({'name':'Data scientist'})

print(vacancies_hh.count_documents({}))

# Function for create only new docs in db
for v in vacancies_hh_list:
    if vacancies_hh.count_documents({
        'name': v['name'],
        'min_salary': v['min_salary'],
        'max_salary': v['max_salary'],
        'currency': v['currency'],
        'href': v['href'],
        'site': v['site'],
    }) == 0:
        vacancies_hh.update_one(
            {
                'name': v['name'],
                'min_salary': v['min_salary'],
                'max_salary': v['max_salary'],
                'currency': v['currency'],
                'href': v['href'],
                'site': v['site'],
            },
            {
                '$set':
                    {
                        'name': v['name'],
                        'min_salary': v['min_salary'],
                        'max_salary': v['max_salary'],
                        'currency': v['currency'],
                        'href': v['href'],
                        'site': v['site'],
                    }
            },
            upsert=True
        )

print(vacancies_hh.count_documents({}))


