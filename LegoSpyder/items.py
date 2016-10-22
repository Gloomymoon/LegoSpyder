# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LegoSpyderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    theme = scrapy.Field()
    year = scrapy.Field()
    productId = scrapy.Field()
    productName = scrapy.Field()
    productImage = scrapy.Field()
    BI_desc = scrapy.Field()
    BI_pdfLoc = scrapy.Field()
    BI_size = scrapy.Field()
    BI_fpimg = scrapy.Field()
    BI_isAlt = scrapy.Field()


class TestItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

