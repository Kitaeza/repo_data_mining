# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

def price_mod(value):
    if not value: return []
    return value.replace(' ', '')

def specification_value_mod(value):
    if not value: return []
    return value.strip()


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    href = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_mod), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    spec_keys = scrapy.Field()
    spec_vals = scrapy.Field(input_processor=MapCompose(specification_value_mod))
    specifications = scrapy.Field()
    photos = scrapy.Field()
