import scrapy
import requests
from hashlib import md5

from github import settings
from github.items import PStatsItem
from scrapy.loader import ItemLoader


class ProjectStatsSpider(scrapy.Spider):
    name = 'pstats'
    allowed_domains = [
        'github.com',
    ]

    def __init__(self, *args, **kwargs):
        super(ProjectStatsSpider, self).__init__(*args, **kwargs)
        self.next_page_url = None

    def _fetch_project(self, next_page_url=None):
        if next_page_url is None:
            params = {
                'size': 30,
            }
            res = requests.get(url=settings.SERVER_URL,
                               params=params,
                               headers=settings.SERVER_HEADER)
        else:
            res = requests.get(next_page_url, headers=settings.SERVER_HEADER)
        return res.json()

    def start_requests(self):
        data = self._fetch_project()
        self.cache_info = dict()
        for row in data['results']:
            self.logger.info(row['github_url'])
            key = md5(row['github_url']).hexdigest()
            self.cache_info.update(
                {
                    key: {
                        'id': row['id'],
                    }
                }
            )
            yield scrapy.Request(url=row['github_url'], callback=self.parse)
        self.next_page_url = data['next']
        # self.logger.info(next_page_url)
        while True:
            if self.next_page_url:
                data = self._fetch_project(next_page_url=self.next_page_url)
                for row in data['results']:
                    key = md5(row['github_url']).hexdigest()
                    self.cache_info.update(
                        {
                            key: {
                                'id': row['id'],
                            }
                        }
                    )
                    yield scrapy.Request(row['github_url'], self.parse)
                self.next_page_url = data['next']
            else:
                break

    def parse(self, response):
        key = md5(response.url).hexdigest()
        info = self.cache_info.pop(key)
        item = ItemLoader(item=PStatsItem(), response=response)
        item.add_css('watch', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('star', 'ul.pagehead-actions >li >a.social-count')
        item.add_css('fork', 'ul.pagehead-actions >li >a.social-count')
        item.add_value('project', info['id'])

        # self.logger.info(item.load_item())
        return item.load_item()
