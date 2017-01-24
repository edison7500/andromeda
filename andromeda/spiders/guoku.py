# coding=utf-8
import scrapy
from urlparse import urlparse
from andromeda.items import EntityItem

from scrapy.loader import ItemLoader


class GKSpider(scrapy.Spider):

    name    = "guoku" #定义爬虫名字
    allowed_domains = [
        'guoku.com',
    ]

    def __init__(self, uri, *args, **kwargs):
        super(GKSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
                "http://www.guoku.com/{uri}/".format(uri=uri),
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

        item            = ItemLoader(item=EntityItem(), response=response)
        item.add_css('brand', 'div.brand')
        item.add_css('title', 'div.entity-title')
        item.add_css('price', 'div.price-tag > span', re='(\d+\.\d+)')
        item.add_css('image_urls', 'div.other-pic-list > a > img::attr(src)')
        item.add_css('origin_link', response.url)
        # item.add_value('image_urls', image_urls)
        return item.load_item()
