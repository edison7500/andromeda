import scrapy
import requests

from hashlib import md5
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from github import settings
from github.items import GithubItem



class FetchProjectSpider(scrapy.Spider):
    name = 'fetch-project'

    def __init__(self, *args, **kwargs):
        super(FetchProjectSpider, self).__init__(*args, **kwargs)
        self.cache_info = dict()
        # self.next_page_url  = None

    def _fetch_project(self, next_page_url=None):
        if next_page_url is None:
            fetch_url = "{base_url}fetch/project/".format(base_url=settings.SERVER_URL)
        else:
            fetch_url = next_page_url
        res = requests.get(fetch_url, headers=settings.SERVER_HEADER)
        # data        = res.json()['results']
        return res.json()

    def start_requests(self):
        data = self._fetch_project()

        for row in data['results']:
            key = md5(row['url']).hexdigest()
            self.cache_info.update(
                {
                    key: {
                        'url': row['url'],
                        'category': row['category']
                    }
                }
            )
            yield scrapy.Request(row['url'], self.parse)
        next_page_url = data['next']
        while True:
            if next_page_url:
                data = self._fetch_project(next_page_url=next_page_url)
                for row in data['results']:
                    key = md5(row['url']).hexdigest()
                    self.cache_info.update(
                        {
                            key: {
                                'url': row['url'],
                                'category': row['category']
                            }
                        }
                    )
                    yield scrapy.Request(row['url'], self.parse)
                next_page_url = data['next']
            else:
                break

    def parse(self, response):
        key = md5(response.url).hexdigest()
        info = self.cache_info.pop(key)

        item = ItemLoader(item=GithubItem(), response=response)

        item.add_css('author', 'h1.public >span.author >a')
        item.add_css('name', 'h1.public >strong >a')
        item.add_css('desc', 'div.repository-meta-content')
        # if response.css('article.markdown-body').extract_first():
        #     item.add_css('readme', 'article.markdown-body')
        # else:
        #     item.add_css('readme', 'div.plain')
        #

        readme_name = remove_tags(response.css("div#readme >h3").extract_first())
        readme_name = readme_name.strip()
        # self.logger.info(response.url)
        readme_url = "{base_url}/master/{readme}".format(
            base_url=response.url,
            readme=readme_name,
        )
        item.add_value('readme', readme_url)
        item.add_value('github_url', response.url)
        item.add_value('category', info['category'])
        # self.logger.info(item.load_item())
        return item.load_item()