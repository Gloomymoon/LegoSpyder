# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class LegoBaseItem(Item):
    productId = Field()
    file_urls = Field()
    files = Field()
    file_paths = Field()


class LegoProductItem(LegoBaseItem):
    # define the fields for your item here like:
    # name = Field()
    productName = Field()
    productImage = Field()
    theme = Field()
    year = Field()


class LegoBuildingInstructionsItem(LegoBaseItem):
    description = Field()


class LegoImageItem(Item):
    image_urls = Field()
    images = Field()
    image_paths = Field()


class LegoFileItem(Item):
    file_urls = Field()
    files = Field()
    file_paths = Field()

