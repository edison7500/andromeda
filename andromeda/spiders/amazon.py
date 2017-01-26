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

            key     = md5(url).hexdigest()
            self.queue_dict.update(
                {
                    key: asin,
                }
            )

            yield SplashRequest(url, self.parse_book,
                                args={'wait':0.5},
                                dont_send_headers=True,
                                )

    def parse_book(self, response):
        # o       = urlparse(response.url)
        key     = md5(response.url).hexdigest()
        item    = ItemLoader(item=BookItem(), response=response)

        item.add_css('title', 'html > head > title')
        item.add_css('desc', 'div#bookDescription_feature_div > noscript')
        item.add_css('price', 'span.a-color-price', re='(\d+\.\d+)')
        item.add_value('asin', self.queue_dict[key])
        item.add_value('origin_link', response.url)
        item.add_css('image_urls', 'div.imageThumb > img::attr(src)')
        # print item.load_item()
        return item.load_item()
        # return item.load_item()
