# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TickersParserItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    open_price = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close_last = scrapy.Field()
    volume = scrapy.Field()
