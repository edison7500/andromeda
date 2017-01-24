import scrapy
from scrapy.loader import ItemLoader
from urlparse import urlparse
from hashlib import md5

from andromeda.items import BookItem
from scrapy_splash import SplashRequest


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = [
        'amazon.cn',
        'amazon.com',
    ]

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        self.start_urls =[
            'https://www.amazon.cn/s?ie=UTF8&page=1&rh=n%3A658390051%2Ck%3APython',
        ]
        self.queue_dict = dict()

    def parse(self, response):
        self.logger.info(response.url)
        o   = urlparse(response.url)
        for row in response.css('ul#s-results-list-atf > li'):
            asin    = row.css('li::attr(data-asin)').extract_first()
            url     = row.css('a::attr(href)').extract_first()
            # yield scrapy.Request(url, self.parse_book)
            yield SplashRequest(url, self.parse_book,
                                args={'wait':0.5},
                                dont_send_headers=True,
                                )

    def parse_book(self, response):

        item    = ItemLoader(item=BookItem(), response=response)

        item.add_css('title', 'span#productTitle')
        item.add_css('desc', 'div#bookDescription_feature_div > noscript')
        item.add_css('price', 'span.a-color-price', re='(\d+\.\d+)')
        item.add_value('link', response.url)
        item.add_css('image_urls', 'div.imageThumb > img::attr(src)')

        return item.load_item()
