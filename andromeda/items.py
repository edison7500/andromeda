# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from HTMLParser import HTMLParser

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from urlparse import urlparse




# def filter_price(value):
#     if value.isdigit():
#         return value

class EntityItem(scrapy.Item):
    brand   = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    title   = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    price   = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    origin_link = scrapy.Field()

    image_urls  = scrapy.Field()
    images      = scrapy.Field()



def filter_image(value):
    # if value.isdigit():
    o       = urlparse(value)
    path    = o.path.split('.')
    image_url   = "{scheme}://{host}{path}.{ext}".format(
        scheme=o.scheme,
        host=o.netloc,
        path=path[0],
        ext=path[-1],
    )
    return image_url

def filter_desc(value):
    h       = HTMLParser()
    content = h.unescape(value)
    content = remove_tags(content.strip())

    return content


class BookItem(scrapy.Item):

    title       = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    desc        = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_desc),
        output_processor=TakeFirst(),
    )
    price       = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    source      = scrapy.Field()
    link        = scrapy.Field()
    image_urls  = scrapy.Field(
        input_processor=MapCompose(filter_image),
    )
    images      = scrapy.Field()
