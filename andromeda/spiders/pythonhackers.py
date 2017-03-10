import scrapy
from urlparse import urlparse


class PyHackerSpider(scrapy.Spider):
    name = 'pythonhackers'

    allowed_domains = [
        'pythonhackers.com',
        'github.com',
    ]

    def __init__(self, *args, **kwargs):
        super(PyHackerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://pythonhackers.com/open-source/'
        ]

    def parse(self, response):
        o = urlparse(response.url)
        # self.logger.info(response.url)
        for row in response.css('.table >tbody >tr'):

            uri = row.css('tr >td >a::attr(href)').extract_first()
            # self.logger.info(uri)
            _url    = "{scheme}://{host}{uri}".format(
                scheme=o.scheme,
                host=o.netloc,
                uri=uri,
            )
            yield scrapy.Request(_url, callback=self.parse_project)

    def parse_project(self, response):
        github_url  = response.css('a.pad10::attr(href)').extract_first()
        yield scrapy.Request(github_url, callback=self.parse_github)

    def parse_github(self, response):
        # self.logger.info(response.body)
        self.logger.info(response.url)