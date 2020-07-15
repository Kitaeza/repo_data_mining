from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from leroymerlin import settings
from leroymerlin.spiders.lmru import LmruSpider


if __name__ == '__main__':
    unit = 'унитаз'

    photo_settings = settings
    photo_settings.IMAGES_STORE = unit

    crowler_settings = Settings()
    crowler_settings.setmodule(photo_settings)

    process = CrawlerProcess(settings=crowler_settings)
    process.crawl(LmruSpider, unit)

    process.start()


