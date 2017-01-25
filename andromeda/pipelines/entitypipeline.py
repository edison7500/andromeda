# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from hashlib import md5
import requests
import logging

from scrapy.exceptions import DropItem
from andromeda import settings


class DuplicatesPipeline(object):

    def process_item(self, item, spider):
        identified_code     = md5(item['origin_link']).hexdigest()

        check_url           = "{url}/{identified_code}".format(
            url = settings.SERVER_URL,
            identified_code = identified_code,
        )
        res = requests.head(check_url)
        if res.status_code  == 200:
            raise DropItem("Duplicate entity found: %s", item)
        else:
            return item


class PostEntityPipeline(object):

    def process_item(self, item, spider):
        res = requests.post(settings.SERVER_URL, json=dict(item))
        if res.status_code == 200:
            return item
        else:
            logging.error(res.text)


