# coding: utf-8
from . import main
from flask import render_template
from app.main.models import Ticker
from app.main.models import Price
from app.main.models import InsiderTrade
from app.main.models import Insider
from sqlalchemy import func


# главная
@main.route('/', methods=['GET', 'POST'])
def index():
    tickers = Ticker.query.all()
    return render_template('index.html',
                           tickers=tickers,
                           title="Акции",
                           )


@main.route('/<string:ticker>', methods=['GET', 'POST'])
def ticker_view(ticker):
    ticker = Ticker.query.filter(Ticker.name == ticker).first()
    prices = Price.query.filter(Price.ticker_id == ticker.id).all()
    return render_template('tickers.html',
                           ticker=ticker.name,
                           prices=prices,
                           title="Цены на %s" % ticker,
                           )


@main.route('/<string:ticker>/insider', methods=['GET', 'POST'])
def insider_view(ticker):
    ticker = Ticker.query.filter(Ticker.name == ticker).first()
    insiders = InsiderTrade.query.filter(InsiderTrade.ticker_id == ticker.id).all()
    return render_template('insiders.html',
                           ticker=ticker,
                           insiders=insiders,
                           title="Данные торговли совладельцев компании %s" % ticker,
                           )


@main.route('/<string:ticker>/insider/<string:insider_name>', methods=['GET', 'POST'])
def one_insider_view(ticker, insider_name):
    insider_name = insider_name.replace('_', ' ')  # конвертируем обратно
    ticker = Ticker.query.filter(Ticker.name == ticker).first()  # находим нужную акцию
    one_insider = Insider.query.filter(func.lower(Insider.name) == insider_name).first()  # находим нужного инсайдера
    # данные по конкретному инсайдеру
    trades = InsiderTrade.query.filter(InsiderTrade.ticker_id == ticker.id).filter(
        InsiderTrade.insider_id == one_insider.id).all()
    return render_template('insiders.html',
                           insiders=trades,
                           title="Данные торговли совладельцев компании %s" % ticker,
                           )
