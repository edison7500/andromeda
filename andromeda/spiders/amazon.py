import scrapy
from urlparse import urlparse


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

    def parse(self, response):
        self.logger.info(response.url)
        o   = urlparse(response.url)
        for row in response.css('ul#s-results-list-atf > li'):
            dp_id   = row.css('li::attr(data-asin)').extract_first()
            url     = "{scheme}:://{host}/dp/{production}".format(
                scheme=o.scheme,
                host=o.hostname,
                production=dp_id,
            )
            self.logger.info(url)
            yield scrapy.Request(url, self.parse_book)

    def parse_book(self, response):
        self.logger.info(response.url)


