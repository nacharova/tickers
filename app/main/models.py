# -*- coding: utf-8 -*-
from .. import db

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date


class Tickers(db.Model):
    __tablename__ = "tickers"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(1024), default="")
    date = db.Column(Date, default="")
    open =  db.Column(Integer, default=0)
    high =  db.Column(Integer, default=0)
    low =  db.Column(Integer, default=0)
    close_last =  db.Column(Integer, default=0)
    volume =  db.Column(Integer, default=0)

    @staticmethod
    def add(name, date, open, high, low, close_last, volume):
        tickers = Tickers(name=name,
                          date=date,
                          open=open,
                          high=high,
                          low=low,
                          close_last=close_last,
                          volume=volume,
                          )
        db.session.add(tickers)
        db.session.commit()
        return tickers.id

    def __repr__(self):
        return '<Tickers %s>' % str(self.name)

    def __str__(self):
        return self.name






