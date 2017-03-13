import scrapy

# from chaojiin.items import ChaojiinItem
from scrapy.loader import ItemLoader
from chaojiin.items import ChaoJiInItem

class CJISpider(scrapy.Spider):

    name = 'chaojiin'
    allowed_domains = [
        'chaoji.in',
    ]

    def __init__(self, *args, **kwargs):
        super(CJISpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://chaoji.in/d3/',
        ]

    def parse(self, response):
        for row in response.css('div.picture-box'):
            _url = row.css('h2.grid-title >a::attr(href)').extract_first()
            self.logger.info(_url)
            yield scrapy.Request(_url, callback=self.parse_item)

        nex_page_url    = response.css('div.nav-links >a.next::attr(href)').extract_first()
        if nex_page_url is not None:
            yield scrapy.Request(nex_page_url, callback=self.parse)

    def parse_item(self, response):
        conetnt     = response.css('div.entry-content >div.single-content')

        image_urls  = conetnt.css('a.fancybox >img::attr(src)').extract()

        self.logger.info(image_urls)

        item = ItemLoader(item=ChaoJiInItem(), response=response)
        item.add_css('title', 'h1.entry-title')
        item.add_value('image_urls', image_urls)


        return item.load_item()