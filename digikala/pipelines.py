# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class DigikalaPipeline:
    def process_item(self, item, spider):
        return item

'''
class MyImagesPipeline(ImagesPipeline):

    def image_key(self, url):
        image_guid = url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        # use 'accession' as name for the image when it's downloaded
        return [scrapy.Request(x, meta={'image_name': item["accession"]})
                for x in item.get('image_urls', [])]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']
'''