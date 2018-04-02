# coding: utf-8
from . import main
from flask import render_template
from app.main.models import Ticker
from app.main.models import Price
from app.main.models import InsiderTrade
from app.main.models import Insider
from sqlalchemy import func
import datetime
from flask import request
from flask import redirect
from flask import url_for


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


@main.route('/<string:ticker>/analytics', methods=['GET', 'POST'])
def analytics_view(ticker):
    if request.method == 'GET':
        difference = dict()
        date_from_value = request.args.get('date_from', None)
        date_to_value = request.args.get('date_to', None)
        try:
            date_to = datetime.datetime.strptime(date_to_value, '%m-%d-%Y')
            date_from = datetime.datetime.strptime(date_from_value, '%m-%d-%Y')
        except:
            return render_template('analytics.html',
                                   title="Указаны неверные данные",
                                   )
        ticker = Ticker.query.filter(Ticker.name == ticker).first()  # находим нужную акцию
        price_from = Price.query.filter(Price.ticker_id == ticker.id).filter(
            Price.date == date_from).first()
        price_to = Price.query.filter(Price.ticker_id == ticker.id).filter(
            Price.date == date_to).first()

        if price_from and price_to:
            difference['open_price'] = round(price_from.open_price - price_to.open_price, 3)
            difference['high'] = round(price_from.high - price_to.high, 3)
            difference['low'] = round(price_from.low - price_to.low, 3)
            difference['close_last'] = round(price_from.close_last - price_to.close_last, 3)
            return render_template('analytics.html',
                                   difference=difference,
                                   title="Разница цен %s с %s по %s" % (ticker, date_from_value, date_to_value),
                                   )
        return render_template('analytics.html',
                               title="Данные отсутствуют",
                               )
    return redirect(url_for('.ticker_view', ticker=ticker))


@main.route('/<string:ticker>/delta', methods=['GET', 'POST'])
def delta_view(ticker):
    type_choices = {'open': 'open_price', 'high': 'high', 'low': 'low', 'close': 'close_last'}
    results = []
    if request.method == 'GET':
        value = int(request.args.get('value', None))
        type = request.args.get('type', None)
        if type in type_choices:
            ticker = Ticker.query.filter(Ticker.name == ticker).first()  # находим нужную акцию
            all_prices = Price.query.filter(Price.ticker_id == ticker.id).order_by(Price.date).all()
            for cur_price in all_prices:
                lost_prices = Price.query.filter(Price.ticker_id == ticker.id).filter(
                    Price.date > cur_price.date).order_by(Price.date).all()
                for price in lost_prices:
                    if getattr(cur_price, type_choices[type]) - getattr(price, type_choices[type]) > value:
                        results.append("%s - %s" % (cur_price.date, price.date))
                        break
            return render_template('delta.html',
                                   title="Минимальные периоды, когда цена %s (%s) изменялась более чем на %d" % (
                                   ticker, type, value),
                                   results=results,
                                   )
        return render_template('delta.html',
                               title="Неправильно указаны параметры (type = open, high, low, close)",
                               results=results,
                               )
    return redirect(url_for('.ticker_view', ticker=ticker))
