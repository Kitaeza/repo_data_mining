# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipelineHh:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        salary = item['salary']
        item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(salary)
        del item['salary']
        collection.insert_one(item)
        print(1)
        return item

    def process_salary(self, salary:list):
        salary_list = []
        if 'от ' in salary:
            salary_min: str = salary[salary.index('от ') + 1]
            salary_min = salary_min.replace(u'\xa0','')
            salary_list.append(int(salary_min))
            if ' до ' not in salary: salary_list.append(None)
        if 'до ' in salary:
            salary_list.append(None)
            salary_max: str = salary[salary.index('до ') + 1]
            salary_max = salary_max.replace(u'\xa0', '')
            salary_list.append(int(salary_max))
        if ' до ' in salary:
            salary_max: str = salary[salary.index(' до ') + 1]
            salary_max = salary_max.replace(u'\xa0', '')
            salary_list.append(int(salary_max))
        if len(salary) > 1:
            currency = salary[-2]
            salary_list.append(currency)
        if len(salary) == 1:
            currency = salary[0]
            salary_list.append(None)
            salary_list.append(None)
            salary_list.append(currency)
        return salary_list

    def __del__(self):
        self.client.close()

class JobparserPipelineSj:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # salary = item['salary']
        collection.insert_one(item)
        return item

    def process_salary(self, salary:list):
        pass

    def __del__(self):
        self.client.close()