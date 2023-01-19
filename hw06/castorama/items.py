# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose, Join


def process_price(value):
    if value:
        money = int(value[0].replace(' ', '').replace('"', ''))
        currency = value[1]
        return {'money': money, 'currency': currency}
    return None


def process_trim_value(value):
    return value.replace("\n", '').strip()


def process_parameters_to_dict(value):
    return dict(zip(value[::2], value[1::2]))


def process_small_img_to_origin(value):
    return value.replace("resize_cache/", "").replace("80_80_1/", "")


class CastoramaItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    parameters = scrapy.Field(input_processor=MapCompose(process_trim_value),
                              output_processor=Compose(process_parameters_to_dict))
    currentPrice = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    oldPrice = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    firstPhoto = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
