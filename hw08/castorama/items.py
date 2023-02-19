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
    if value:
        return value.replace("resize_cache/", "").replace("80_80_1/", "")


def process_img(x):
    if x:
        return "https://www.castorama.ru/" + x


def process_name(x):
    return x.replace('\n', '').strip()


def process_categories(x):
    return x[1:]


class CastoramaItem(scrapy.Item):
    """
    Класс описания итема паплайна. Основные параметры:
    name - название товара
    categories - категории товара
    description - описание товара
    parameters - параметры товара
    currentPrice - текущая цена. Если на товар действует скидка, то цена с учетом скидки
    oldPrice - цена без учета скидки. Если на товар не действует скидка - не заполняется
    photos - ссылка на фотографии
    firstPhoto - техническое поле. Если миниатюр нет - будет использоваться это поле для получения картинок
    url - ссылка на товар
    """
    name = scrapy.Field(input_processor=MapCompose(process_name), output_processor=TakeFirst())
    categories = scrapy.Field(input_processor=Compose(process_categories))
    description = scrapy.Field(output_processor=TakeFirst())
    parameters = scrapy.Field(input_processor=MapCompose(process_trim_value),
                              output_processor=Compose(process_parameters_to_dict))
    currentPrice = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    oldPrice = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_img, process_small_img_to_origin))
    firstPhoto = scrapy.Field(input_processor=MapCompose(process_img), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
