import scrapy
from scrapy.selector import Selector
import json
from ..items import TestItem


class BuildingInstructionsSpider(scrapy.Spider):
    name = 'lego'
    search_base_url = "https://wwwsecure.us.lego.com//service/biservice/searchbythemeandyear?fromIndex=0&onlyAlternatives=false&theme=%s&year=%s"
    allowed_domains = ['lego.com']
    start_urls = [
        'https://wwwsecure.us.lego.com/en-us/service/buildinginstructions',
    ]

    def parse(self, response):
        year_str = response.css('div.product-search::attr(data-search-years)').extract_first()
        theme_str = response.css('div.product-search::attr(data-search-themes)').extract_first()
        for theme in json.loads(theme_str):
            #print theme
            for year in json.loads(year_str):
                #print year
                search_url = self.search_base_url % (theme['Key'], year)
                yield scrapy.Request(search_url, callback=self.parse_search)

    def parse_search(self, response):
        print response.body


class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = [
        #'http://tieba.baidu.com/p/4023230951',
        'https://wwwsecure.us.lego.com//service/biservice/searchbythemeandyear?fromIndex=0&onlyAlternatives=false&theme=10000-20127&year=2015',
    ]

    def parse(self, response):
        result = json.loads(response.body)
        print result['count'], result['moreData']
        item = TestItem()
        url_list = []
        for product in result['products']:
            #print product
            url_list.append(product['productImage'])
        print url_list
        item['image_urls'] = url_list
        yield item

        '''
        sel = Selector(response)

        image_url = sel.xpath("//div[@id='post_content_75283192143']/img[@class='BDE_Image']/@src").extract()
        print 'the urls:\n'
        print image_url
        print '\n'

        item = TestItem()
        item['image_urls'] = image_url

        yield item
        '''
