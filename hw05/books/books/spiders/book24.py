import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Book24Spider(CrawlSpider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = [
        'https://book24.ru/catalog/tekhnicheskie-nauki-2023/',
        'https://book24.ru/catalog/informatsionnye-tekhnologii-1357/',
        'http://book24.ru/'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
