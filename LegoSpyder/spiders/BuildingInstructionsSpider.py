import scrapy
import json
from urlparse import urlparse, parse_qs
from ..items import LegoProductItem, LegoBuildingInstructionsItem, LegoImageItem, LegoFileItem


class BuildingInstructionsSpider(scrapy.Spider):
    name = 'lego'
    search_base_url = "https://wwwsecure.us.lego.com//service/biservice/searchbythemeandyear?fromIndex=%s&onlyAlternatives=false&theme=%s&year=%s"
    allowed_domains = ['lego.com']
    start_urls = [
        'https://wwwsecure.us.lego.com/en-us/service/buildinginstructions',
    ]

    def parse(self, response):
        year_str = response.css('div.product-search::attr(data-search-years)').extract_first()
        theme_str = response.css('div.product-search::attr(data-search-themes)').extract_first()
        for theme in json.loads(theme_str):
            for year in json.loads(year_str):
                search_url = self.search_base_url % (0, theme['Key'], year)
                yield scrapy.Request(search_url, callback=self.parse_search)

    def parse_search(self, response):
        result = json.loads(response.body)
        param = parse_qs(urlparse(response.url).query)
        if result['count']:
            for p in result['products']:
                product = LegoProductItem()
                product['theme'] = param["theme"][0]
                product['year'] = param["year"][0]
                product['productId'] = p['productId']
                product['productName'] = p['productName']
                product['productImage'] = p['productImage']
                product['file_urls'] = [p['productImage']]
                yield product
                for bi in p['buildingInstructions']:
                    instruction = LegoBuildingInstructionsItem()
                    instruction['productId'] = p['productId']
                    instruction['description'] = bi['description']
                    instruction['file_urls'] = [bi['pdfLocation'], bi['frontpageInfo']]
                    yield instruction
        if result['moreData']:
            search_next = self.search_base_url % (int(param['fromIndex'][0]) + int(result['count']), param["theme"][0], param["year"][0])
            yield scrapy.Request(search_next, callback=self.parse_search)


class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = [
        'https://wwwsecure.us.lego.com//service/biservice/searchbythemeandyear?fromIndex=0&onlyAlternatives=false&theme=10000-20127&year=2015',
    ]

    def parse(self, response):
        result = json.loads(response.body)
        print result['count'], result['moreData']
        productImage = LegoFileItem()
        frontpage = LegoFileItem()
        pdfLocation = LegoFileItem()
        for product in result['products']:
            productImage['file_urls'] = [product['productImage']]
            yield productImage
            for buildingInstruction in product['buildingInstructions']:
                frontpage['file_urls'] = [buildingInstruction['frontpageInfo']]
                yield frontpage
                pdfLocation['file_urls'] = [buildingInstruction['pdfLocation']]
                yield pdfLocation



