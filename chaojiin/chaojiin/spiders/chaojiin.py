import scrapy


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
        # self.logger.info(response.url)

        for row in response.css('div.picture-box'):
            _url = row.css('h2.grid-title >a::attr(href)').extract_first()
            self.logger.info(_url)
            yield scrapy.Request(_url, callback=self.parse_item)

    def parse_item(self, response):
        conetnt     = response.css('div.entry-content >div.single-content')

        image_urls  = conetnt.css('a.fancybox >img::attr(src)').extract()

        self.logger.info(image_urls)