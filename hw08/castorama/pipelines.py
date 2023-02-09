# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
import pymongo
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter


class CastoramaPipeline:
    """
    Финальный шаг паплайна для вывода в лог информации о товаре
    """
    def process_item(self, item, spider):
        print(item)
        return item


class CastoramaMongoPipeline:
    """
    Шаг сохранения товара в mongodb
    """
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'castorama'),
            collection_name=crawler.settings.get('MONGODB_COLLECTION', 'goods')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class CastoramaUseFirstPhotoIfSmallsNotExistPipeline:
    """
    Шаг для использования первой фотографии, если миниатюрок не нашли.
    На это же шаге удаляем значение технического поля firstPhoto
    """
    def process_item(self, item, spider):
        if not item.get("photos"):
            if item.get("firstPhoto"):
                item['photos'] = [item.get("firstPhoto")]
        item['firstPhoto'] = None
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    """
    Шаг скачивания фотографий товара
    """
    def get_media_requests(self, item, info):
        if item.get('photos'):
            for img in item.get('photos'):
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        if item:
            return f'full/{item.get("name")}_{image_guid}.jpg'
        else:
            return f'full/unknown_type/{image_guid}.jpg'
