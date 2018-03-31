# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main.models import Price
from app.main.models import Ticker


class TickersParserPipeline(object):
    def __init__(self):
        engine = create_engine('postgresql+psycopg2://tickers:tickers@192.168.0.71/postgres')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        params = dict(item)
        ticker_name = params.pop('ticker')
        query = self.session.query(Ticker).filter(Ticker.name == ticker_name).first()
        if not query:
            ticker = Ticker(name=ticker_name)
            self.session.add(ticker)
            self.session.commit()
            print("ticker id = ", ticker.id)
            query = self.session.query(Ticker).filter(Ticker.name == ticker_name).first()
        price = Price(ticker_id=query.id, **params)
        self.session.add(price)
        self.session.commit()
        return item
