import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hw05.books.books.items import BooksItem


class LabirintRuSpider(CrawlSpider):
    name = 'labirint_ru'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['http://www.labirint.ru/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    xpath_next_page = "//a[@class='pagination-next__text']/@href"
    xpath_book = "//div[contains(@data-title,'Все в жанре')]/div[@class='genres-carousel__item']//a[" \
                 "@class='product-title-link']/@href"

    def parse_item(self, response: HtmlResponse):
        next_page = response.xpath(self.xpath_next_page).get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath(self.xpath_book).getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        name = response.xpath("//div[@class='prodtitle']/h1//text()").get()
        authors = response.xpath("//a[@data-event-label='author']//text()").getall()
        publisher = response.xpath("//a[@data-event-label='publisher']//text()").get()
        year = response.xpath("//div[@class='publisher']//text()").getall()
        isbn = response.xpath("//div[@class='isbn']//text()").get()
        price = response.xpath("//span[@class='buying-priceold-val-number']//text()").get()
        price_with_salary = response.xpath("//span[@class='buying-pricenew-val-number']//text()").get()
        price_currency = response.xpath("//span[@class='buying-pricenew-val-currency']//text()").get()
        rate = response.xpath("//div[@id='rate']//text()").get()

        yield BooksItem(
            url=response.url,
            name=name,
            authors=authors,
            publisher=publisher,
            year=year,
            isbn=isbn,
            price=price,
            price_with_salary=price_with_salary,
            price_currency=price_currency,
            rate=rate
        )
