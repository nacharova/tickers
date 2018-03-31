# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from app.main.models import Price
from app.main.models import Ticker
from app.main.models import Insider
from app.main.models import InsiderTrade


class ParserItem(scrapy.Item):
    def save(self, session, params):
        raise NotImplemented


# цены на акции
class TickersParserItem(ParserItem):
    ticker = scrapy.Field()
    date = scrapy.Field()
    open_price = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close_last = scrapy.Field()
    volume = scrapy.Field()

    def save(self, session, params):
        ticker_name = params.pop('ticker')
        ticker = session.query(Ticker).filter(Ticker.name == ticker_name).first()
        if not ticker:
            ticker = Ticker(name=ticker_name)
            session.add(ticker)
            session.commit()
        price = Price(ticker_id=ticker.id, **params)
        session.add(price)
        session.commit()


# инсайдерские сделки
class InsidersParserItem(ParserItem):
    ticker = scrapy.Field()
    insider = scrapy.Field()
    relation = scrapy.Field()
    last_date = scrapy.Field()
    transaction_type = scrapy.Field()
    owner_type = scrapy.Field()
    shares_traded = scrapy.Field()
    last_price = scrapy.Field()
    shares_held = scrapy.Field()

    def save(self, session, params):
        ticker_name = params.pop('ticker')
        insider_name = params.pop('insider')
        ticker = session.query(Ticker).filter(Ticker.name == ticker_name).first()
        if not ticker:
            ticker = Ticker(name=ticker_name)
            session.add(ticker)
            session.commit()

        insider = session.query(Insider).filter(Insider.name == insider_name).first()
        if not insider:
            insider = Insider(name=insider_name)
            session.add(insider)
            session.commit()

        insider_trade = InsiderTrade(ticker_id=ticker.id, insider_id=insider.id, **params)
        session.add(insider_trade)
        session.commit()

