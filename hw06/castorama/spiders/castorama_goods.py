import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from hw06.castorama.items import CastoramaItem


class CastoramaGoodsSpider(scrapy.Spider):
    name = 'castorama_goods'
    allowed_domains = ['castorama.ru']
    start_urls = [
        'https://www.castorama.ru/gardening-and-outdoor/tovary-dlja-uborki-snega/',
        'https://www.castorama.ru/gardening-and-outdoor/sadovye-napol-nye-pokrytija/'
    ]

    xpath_item = "//a[@class='product-card__img-link']/@href"
    xpath_next = "//a[@class='next i-next']/@href"

    def parse(self, response):
        next_page = response.xpath(self.xpath_next).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        items = response.xpath(self.xpath_item).getall()
        for item in items:
            yield response.follow(item, callback=self.parse_item)
        pass

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('description', "//div[@data-btn-classes='product-read-more-btn']/text()")
        loader.add_xpath('parameters', "//div[@id='specifications']//span[@class='specs-table__attribute-name ']/text() | //div[@id='specifications']//dd[contains(@class,'specs-table__attribute-value')]/text()")
        loader.add_xpath('currentPrice', "//div[@class='current-price']//span[@class='price']/span/span/text()")
        loader.add_xpath('oldPrice', "//div[@class='old-price']//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//img[contains(@class,'thumb-slide__img')]/@src")
        loader.add_xpath('firstPhoto', "//img[@role='presentation']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()