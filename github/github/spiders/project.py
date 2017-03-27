import scrapy
import requests
from hashlib import md5

from github import settings
from github.items import PStatsItem
from scrapy.loader import ItemLoader



class ProjectStatsSpider(scrapy.Spider):
    name    = 'pstats'
    allowed_domains = [
        'github.com',
    ]


    def __init__(self, *args, **kwargs):
        super(ProjectStatsSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        params = {
            'size': 100,
        }
        res = requests.get(url=settings.SERVER_URL,
                           params=params,
                           headers=settings.SERVER_HEADER)
        data            = res.json()['results']
        self.cache_info = dict()
        for row in data:
            self.logger.info(row['github_url'])
            key         = md5(row['github_url']).hexdigest()
            self.cache_info.update(
                {
                    key: {
                        'id': row['id'],
                    }
                }
            )
            yield scrapy.Request(url=row['github_url'], callback=self.parse)
#
    def parse(self, response):
        key     = md5(response.url).hexdigest()
        info    = self.cache_info.pop(key)
        item    = ItemLoader(item=PStatsItem(), response=response)
        item.add_css('watch', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('star', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('fork', 'ul.pagehead-actions >li >a.social-count')
        item.add_value('project', info['id'])

        # self.logger.info(item.load_item())
        return item.load_item()