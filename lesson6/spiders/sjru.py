import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItemSj


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        vacancy_links = response.css('a.icMQ_._6AfZ9::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_vac = response.css('h1::text').extract_first()
        salary_vac = response.css('span._3mfro._2Wp8I.PlM3e._2JVkc::text').extract()
        # Здесь должен быть парсер вакансии
        # if salary_vac[0] == 'По договорённости':
        href_vac = response.url
        site_vac = self.allowed_domains[0]
        yield JobparserItemSj(name=name_vac, href=href_vac, site=site_vac)
