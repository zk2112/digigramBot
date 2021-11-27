# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DigikalaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    old_price=scrapy.Field()
    price=scrapy.Field()
    percent=scrapy.Field()
    src=scrapy.Field()
    link=scrapy.Field()
    time=scrapy.Field()
    hashtags=scrapy.Field()
    properties=scrapy.Field()
  #  file_urls=scrapy.Field()
   # files=scrapy.Field()
    #image_urls=scrapy.Field()
    #images=scrapy.Field()
   # accession=scrapy.Field()
  
    pass
