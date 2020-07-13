from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crowler_settings = Settings()
    crowler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crowler_settings)
    # process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()
    print(1)
