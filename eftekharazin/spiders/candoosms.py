import scrapy


class CandoosmsSpider(scrapy.Spider):
    name = 'candoosms'
    allowed_domains = ['candoosms.com']
    start_urls = ['http://candoosms.com/']

    def parse(self, response):
        pass
