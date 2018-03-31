# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# цены на акции
class TickersParserItem(scrapy.Item):
    # __model__ = Price
    ticker = scrapy.Field()
    date = scrapy.Field()
    open_price = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close_last = scrapy.Field()
    volume = scrapy.Field()


# инсайдерские сделки
class InsidersParserItem(scrapy.Item):
    ticker = scrapy.Field()
    insider = scrapy.Field()
    relation = scrapy.Field()
    last_date = scrapy.Field()
    transaction_type = scrapy.Field()
    owner_type = scrapy.Field()
    shares_traded = scrapy.Field()
    last_price = scrapy.Field()
    shares_held = scrapy.Field()

    def get_model(self):
        return
