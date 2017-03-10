import scrapy
from urlparse import urlparse

from scrapy.loader import ItemLoader
from github.items import GithubItem


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
        self.logger.info(response.url)
        item    = ItemLoader(item=GithubItem(), response=response)

        item.add_css('author', 'h1.public >span.author >a')
        item.add_css('name', 'h1.public >strong >a')
        item.add_css('desc', 'div.repository-meta-content')
        item.add_css('watch', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('star', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('fork', 'ul.pagehead-actions >li >a.social-count')

        item.add_value('link', response.url)

        # return item.load_item()
        self.logger.info(item.load_item())