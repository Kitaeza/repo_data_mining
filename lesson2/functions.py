import re

def hh_vacancies(hh_vacancies_page):
    hh_vacancies = []
    for vacancy in hh_vacancies_page:
        vacancy_block = vacancy.find('span', {'class': 'g-user-content'})
        name = vacancy_block.getText()
        href = vacancy_block.find('a')['href']
        site = 'https://hh.ru'
        salary = vacancy_block.find_next('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        min_salary = ''
        max_salary = ''
        currency = ''
        if 'от' in salary:
            from_salary = re.findall(r'\d', salary)
            for d in from_salary:
                min_salary += d
            currency_dict = re.findall(r'\D*', salary)
            for w in currency_dict:
                if w == 'от ': continue
                currency += w
        if 'до' in salary:
            to_salary = re.findall(r'\d', salary)
            for d in to_salary:
                max_salary += d
            currency_dict = re.findall(r'\D*', salary)
            for w in currency_dict:
                if w == 'до ': continue
                currency += w
        if '-' in salary:
            range_salary = re.split(r'-', salary)
            for d in re.findall(r'\d', range_salary[0]):
                min_salary += d
            for d in re.findall(r'\d', range_salary[1]):
                max_salary += d
            currency_dict = re.findall(r'\D*', range_salary[1])
            for w in currency_dict:
                currency += w
        vacancy_description = {
            'name': name,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'currency': currency,
            'href': href,
            'site': site,
        }
        hh_vacancies.append(vacancy_description)

    for v in hh_vacancies:
        v['currency'] = v['currency'].replace(' ', '')

    return hh_vacancies