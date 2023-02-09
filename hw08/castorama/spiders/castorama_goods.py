import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from hw08.castorama.items import CastoramaItem


class CastoramaGoodsSpider(scrapy.Spider):
    """
    Паук для сбора информации о товарах с https://www.castorama.ru
    Начинает парсить с главного каталога и дальше до товаров.
    Информация с товара - ценних, название, описание, особенности, фотографии, категории.
    """
    name = 'castorama_goods'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/catalogue/']

    xpath_catalog = "//a[@class='category__link sitemap-level-0-link']/@href"
    xpath_sub_catalog = "//a[@class='category__link sitemap-level-1-link']/@href"
    xpath_item = "//a[@class='product-card__img-link']/@href"
    xpath_next = "//a[@class='next i-next']/@href"

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Код парсинга страницы с основными категориями
        :param response:
        :param kwargs:
        :return:
        """
        items = response.xpath(self.xpath_catalog).getall()
        for item in items:
            yield response.follow(item, callback=self.parse_catalog)

    def parse_catalog(self, response: HtmlResponse):
        """
        Код парсинга подкатегорий основных категорий сайта
        :param response:
        :return:
        """
        items = response.xpath(self.xpath_sub_catalog).getall()
        for item in items:
            yield response.follow(item, callback=self.parse_sub_catalog)

    def parse_sub_catalog(self, response: HtmlResponse):
        """
        Код парсинга подкатегорий для перехода на страницы товара
        :param response:
        :return:
        """
        next_page = response.xpath(self.xpath_next).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_sub_catalog)
        items = response.xpath(self.xpath_item).getall()
        for item in items:
            yield response.follow(item, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        """
        Код парсинга страницы товара
        :param response:
        :return:
        """
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('categories', "//a/span[@itemprop='name']")
        loader.add_xpath('description', "//div[@data-btn-classes='product-read-more-btn']/text()")
        loader.add_xpath('parameters',
                         "//div[@id='specifications']//span[@class='specs-table__attribute-name ']/text() | //div[@id='specifications']//dd[contains(@class,'specs-table__attribute-value')]/text()")
        loader.add_xpath('currentPrice', "//div[@class='current-price']//span[@class='price']/span/span/text()")
        loader.add_xpath('oldPrice', "//div[@class='old-price']//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//img[contains(@class,'thumb-slide__img')]/@data-src")
        loader.add_xpath('firstPhoto', "//span[@itemprop='image']/@content")
        loader.add_value('url', response.url)
        yield loader.load_item()
