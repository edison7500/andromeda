# coding=utf-8
import scrapy
from urlparse import urlparse
from andromeda.items import EntityItem



class GKSpider(scrapy.Spider):

    name    = "guoku" #定义爬虫名字
    allowed_domains = [
        'guoku.com',
    ]


    def __init__(self, uri, *args, **kwargs):
        super(GKSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
                "https://www.guoku.com/{uri}/".format(uri=uri),
        ]

    def parse(self, response):
        o = urlparse(response.url)
        urls    = response.css('a.img-entity-link::attr(href)').extract()
        for uri in urls:
            url = "{scheme}://{host}{uri}".format(scheme=o.scheme,
                                                    host=o.netloc,
                                                    uri=uri)
            yield scrapy.Request(url, self.pares_entity)

    def pares_entity(self, response):
        self.logger.info(response.url)

        item            = EntityItem()
        item['brand']   = response.css('div.brand::text').extract_first()
        item['title']   = response.css('div.entity-title::text').extract_first()
        item['price']   = response.css('div.price-tag > span::text').extract_first()
        return item
