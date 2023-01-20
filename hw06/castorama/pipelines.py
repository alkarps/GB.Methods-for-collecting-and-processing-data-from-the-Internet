# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class CastoramaPipeline:
    def process_item(self, item, spider):
        print(item)
        return item

class CastoramaUseFirstPhotoIfSmallsNotExistPipeline:
    def process_item(self, item, spider):
        if not item.get("photos"):
            if item.get("firstPhoto"):
                item['photos'] = [item.get("firstPhoto")]
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
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
