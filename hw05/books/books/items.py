# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    isbn = scrapy.Field()
    price = scrapy.Field()
    price_with_salary = scrapy.Field()
    price_currency = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
