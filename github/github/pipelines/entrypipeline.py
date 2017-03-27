# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from hashlib import md5
import requests
import logging

from scrapy.exceptions import DropItem
from github import settings



class UpdatePStatsPipeline(object):
    def process_item(self, item, spider):
        # print (spider.name)
        if spider.name == 'pstats':
            spider.logger.info(item['project'])

            update_stats_url    = "{base_url}{project}/stats".format(
                base_url=settings.SERVER_URL,
                project=item['project'],
            )
            res = requests.post(update_stats_url, json=dict(item), headers=settings.SERVER_HEADER)
            if res.status_code == 201:
                spider.logger.info("OK")
            raise DropItem(item)
        else:
            return item


class DuplicatesPipeline(object):

    def process_item(self, item, spider):
        github_url      = item['github_url']
        identified_code = md5(github_url).hexdigest()
        url             = settings.SERVER_URL
        check_url       = "{base_url}{id_code}".format(
            base_url=url,
            id_code=identified_code,
        )
        res             = requests.head(check_url, headers=settings.SERVER_HEADER)
        if res.status_code == 200:
            raise DropItem(item)
        else:
            return item


class PostProjectPipeline(object):

    def process_item(self, item, spider):
        url = settings.SERVER_URL
        res = requests.post(url, json=dict(item), headers=settings.SERVER_HEADER)
        if res.status_code == 201:
            print ("OK")


