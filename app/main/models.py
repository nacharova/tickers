# -*- coding: utf-8 -*-
from .. import db
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import ForeignKey


# справочник с названиями акций
class Ticker(db.Model):
    __tablename__ = 'ticker'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(1024), default="")

    @staticmethod
    def add(name):
        ticker = Ticker(name=name,
                        )
        db.session.add(ticker)
        db.session.commit()
        return ticker.id

    def __repr__(self):
        return '<Ticker %s>' % str(self.name)

    def __str__(self):
        return self.name


# цены на акции
class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(Integer, primary_key=True)
    ticker_id = db.Column(Integer, ForeignKey(Ticker.id), nullable=False)
    ticker = db.relationship("Ticker")
    date = db.Column(Date, nullable=False)
    open_price = db.Column(Float, nullable=True)
    high = db.Column(Float, nullable=True)
    low = db.Column(Float, nullable=True)
    close_last = db.Column(Float, nullable=True)
    volume = db.Column(Integer, nullable=True)

    @staticmethod
    def add(ticker, date, open_price, high, low, close_last, volume):
        price = Price(ticker=ticker,
                      date=date,
                      open_price=open_price,
                      high=high,
                      low=low,
                      close_last=close_last,
                      volume=volume,
                      )
        db.session.add(price)
        db.session.commit()
        return price.id

    def __repr__(self):
        return '<Price %s>' % str(self.close_last)

    def __str__(self):
        return self.close_last


# справочник с инсайдерами
class Insider(db.Model):
    __tablename__ = 'insider'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(1024), default="")

    @staticmethod
    def add(name):
        insider = Insider(name=name,
                          )
        db.session.add(insider)
        return insider.id

    def __repr__(self):
        return '<Insider %s>' % str(self.name)

    def __str__(self):
        return self.name


# инсайдерские сделки
class InsiderTrade(db.Model):
    __tablename__ = 'insider_trade'
    id = db.Column(Integer, primary_key=True)
    ticker_id = db.Column(Integer, ForeignKey(Ticker.id), nullable=False)
    ticker = db.relationship("Ticker")
    insider_id = db.Column(Integer, ForeignKey(Insider.id), nullable=False)
    insider = db.relationship("Insider")
    relation = db.Column(String(1024), nullable=True)
    last_date = db.Column(Date, nullable=False)
    transaction_type = db.Column(String(1024), nullable=True)
    owner_type = db.Column(String(1024), nullable=True)
    shares_traded = db.Column(Integer, nullable=True)
    last_price = db.Column(Float, nullable=True)
    shares_held = db.Column(Integer, nullable=True)

    @staticmethod
    def add(ticker, insider, relation, last_date, transaction_type, owner_type, shares_traded, last_price, shares_held):
        insider_trade = InsiderTrade(ticker=ticker,
                                     insider=insider,
                                     relation=relation,
                                     last_date=last_date,
                                     transaction_type=transaction_type,
                                     owner_type=owner_type,
                                     shares_traded=shares_traded,
                                     last_price=last_price,
                                     shares_held=shares_held,
                                     )
        db.session.add(insider_trade)
        return insider_trade.id

    def __repr__(self):
        return '<InsiderTrade %s>' % str(self.last_price)

    def __str__(self):
        return self.last_price
