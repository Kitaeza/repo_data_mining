# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        if 'leroymerlin' in self.client.list_database_names(): self.client.drop_database('leroymerlin')
        self.mongo_base = self.client['leroymerlin']


    def process_item(self, item, spider):
        # item['price'] = item['price'].replace(' ', '')
        # item['spec_vals'] = [key.replace('\n', '').strip() for key in item['spec_vals']]
        item['specifications'] = dict(zip(item['spec_keys'], item['spec_vals']))
        del item['spec_keys']
        del item['spec_vals']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def __del__(self):
        self.client.close()


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
