import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    # API
    # https://leroymerlin.ru/bin/api/regions

    def __init__(self, unit):
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?'
                           f'sortby=8'
                           f'&display=30'
                           f'&tab=products'
                           f'&q={unit}']

    def parse(self, response:HtmlResponse):
        page_wrapper = response.css("div.items-wrapper")
        if page_wrapper:
            wrapper = page_wrapper[0].css('a::attr(data-page)')
            pages = int(wrapper.getall()[-1])
            for p in range(1, pages):
                yield response.follow(f'{self.start_urls[0]}&page={p}', callback=self.get_link)
        else:
            yield response.follow(f'{self.start_urls[0]}', callback=self.get_link)


    def get_link(self, response:HtmlResponse):
        units = response.css('div.ui-product-card__info')
        for u in units:
            link = u.xpath("./div[@class='product-name']/a/@href").extract_first()
            yield response.follow(link, callback=self.parse_unit)


    def parse_unit(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('href', response.url)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('spec_keys', "//dl/div/dt/text()")
        loader.add_xpath('spec_vals', "//dl/div/dd/text()")
        loader.add_xpath('photos', "//uc-pdp-media-carousel/picture/img/@src")
        yield loader.load_item()
        # href = response.url
        # title = response.xpath("//h1/text()").extract_first()
        # price = response.xpath("//span[@slot='price']/text()").extract_first()
        # currency = response.xpath("//span[@slot='currency']/text()").extract_first()
        # unit = response.xpath("//span[@slot='unit']/text()").extract_first()
        # spec_keys = response.xpath("//dl/div/dt/text()").extract()
        # spec_vals = response.xpath("//dl/div/dd/text()").extract()
        # photos = response.xpath("//uc-pdp-media-carousel/picture/img/@src").extract()
        # yield LeroymerlinItem(href=href,
        #                       title=title,
        #                       price=price,
        #                       currency=currency,
        #                       unit=unit,
        #                       spec_keys=spec_keys,
        #                       spec_vals=spec_vals,
        #                       photos=photos)


