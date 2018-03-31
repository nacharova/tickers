# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TickersParserPipeline(object):
    def __init__(self):
        engine = create_engine('postgresql+psycopg2://tickers:tickers@192.168.0.71/postgres')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        params = dict(item)
        item.save(self.session, params)

        return item
