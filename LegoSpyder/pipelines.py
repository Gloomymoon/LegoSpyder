# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LegoImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        if 'image_urls' in item:
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem('Image download failed: %s' % image_paths)
            item['image_paths'] = image_paths
        return item


class LegoFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        file_guid = request.url.split('?')[0].split('/')[-1]
        group = request.url.split('?')[0].split('.')[-1]
        #group is the subdirectory of the downloaded files or images
        if group not in ['jpg', 'jpeg', 'png', 'gif', 'pdf']:
            group = 'unknown'
        return '%s/%s' % (group, file_guid)

    def get_media_requests(self, item, info):
        if 'file_urls' in item:
            for file_url in item['file_urls']:
                yield Request(file_url)

    def item_completed(self, results, item, info):
        if 'file_urls' in item:
            file_paths = [x['path'] for ok, x in results if ok]
            if not file_paths:
                raise DropItem('File download failed: %s' % file_paths)
            item['file_paths'] = file_paths
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('lego.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
