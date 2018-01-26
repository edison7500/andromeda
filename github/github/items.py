# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import requests

from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
import html2text


def trim_string(value):
    return value.strip()


def get_count(value):
    value = value.replace(',', '')
    return int(value)


def process_readme(value):
    # _readme = remove_tags(value)
    # print(value)
    raw_readme_url = value.replace("github.com", "raw.githubusercontent.com")

    res = requests.get(raw_readme_url)

    return res.text
    # return html2text.html2text(_readme)
    # return h.handle(_readme)


class TakeSecond(object):
    def __call__(self, values):
        if len(values) >= 2:
            return values[1]
        return 0


class TakeThird(object):
    def __call__(self, values):
        if len(values) == 3:
            return values[-1]
        return 0


class GithubItem(scrapy.Item):
    author = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        output_processor=TakeFirst(),
    )
    desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, trim_string),
        output_processor=TakeFirst(),
    )
    readme = scrapy.Field(
        input_processor=MapCompose(process_readme, ),
        output_processor=TakeFirst(),
    )

    github_url = scrapy.Field(
        output_processor=TakeFirst(),
    )


class PStatsItem(scrapy.Item):
    project = scrapy.Field(
        output_processor=TakeFirst(),
    )
    watch = scrapy.Field(
        input_processor=MapCompose(remove_tags, trim_string, get_count),
        output_processor=TakeFirst(),
    )
    star = scrapy.Field(
        input_processor=MapCompose(remove_tags, trim_string, get_count),
        output_processor=TakeSecond(),
    )
    fork = scrapy.Field(
        input_processor=MapCompose(remove_tags, get_count),
        output_processor=TakeThird(),
    )
