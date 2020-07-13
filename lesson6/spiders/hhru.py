import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItemHh


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        vacancy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_vac = response.css('h1::text').extract_first()
        salary_vac = response.css('span.bloko-header-2::text').extract()
        href_vac = response.url
        site_vac = self.allowed_domains[0]
        yield JobparserItemHh(name=name_vac, salary=salary_vac, href=href_vac, site=site_vac)
