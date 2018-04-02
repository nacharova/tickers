# coding: utf-8
import datetime
import json
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Response
from flask import abort
from sqlalchemy import func

from . import main
from app.main.models import Ticker
from app.main.models import Price
from app.main.models import InsiderTrade
from app.main.models import Insider

api = 'api'


def alchemy_encoder(obj):
    """Функция преобразует дату в строку для возможности конвертирования в json"""
    if isinstance(obj, datetime.date):
        return obj.isoformat()


def get_response(items, iterable=True):
    """Функция возвращает данные в формате json, если данные не итерируемы, преобразует их в dict"""
    if not iterable:
        items = [item.to_dict() for item in items]
    return Response(json.dumps(items, default=alchemy_encoder),
                    content_type="text/json; charset=utf-8")


# главная
@main.route('/', methods=['GET', 'POST'])
@main.route('/api/', methods=['GET', 'POST'])
def index():
    tickers = Ticker.query.all()
    if api in request.url:
        return get_response(tickers, iterable=False)
    return render_template('index.html',
                           tickers=tickers,
                           title="Акции",
                           )


@main.route('/api/<string:ticker>', methods=['GET', 'POST'])
@main.route('/<string:ticker>', methods=['GET', 'POST'])
def ticker_view(ticker):
    ticker = Ticker.query.filter(Ticker.name == ticker).first()
    prices = Price.query.filter(Price.ticker_id == ticker.id).all()

    if api in request.url:
        return get_response(prices, iterable=False)

    return render_template('tickers.html',
                           ticker=ticker.name,
                           prices=prices,
                           title="Цены на %s" % ticker,
                           )


@main.route('/api/<string:ticker>/insider', methods=['GET', 'POST'])
@main.route('/<string:ticker>/insider', methods=['GET', 'POST'])
def insider_view(ticker):
    ticker = Ticker.query.filter(Ticker.name == ticker).first()
    insiders = InsiderTrade.query.filter(InsiderTrade.ticker_id == ticker.id).all()

    if api in request.url:
        return get_response(insiders, iterable=False)

    return render_template('insiders.html',
                           ticker=ticker,
                           insiders=insiders,
                           title="Данные торговли совладельцев компании %s" % ticker,
                           )


@main.route('/api/<string:ticker>/insider/<string:insider_name>', methods=['GET', 'POST'])
@main.route('/<string:ticker>/insider/<string:insider_name>', methods=['GET', 'POST'])
def one_insider_view(ticker, insider_name):
    insider_name = insider_name.replace('_', ' ')  # конвертируем обратно
    ticker = Ticker.query.filter(Ticker.name == ticker).first()  # находим нужную акцию
    one_insider = Insider.query.filter(func.lower(Insider.name) == insider_name).first()  # находим нужного инсайдера
    # данные по конкретному инсайдеру
    trades = InsiderTrade.query.filter(InsiderTrade.ticker_id == ticker.id).filter(
        InsiderTrade.insider_id == one_insider.id).all()

    if api in request.url:
        return get_response(trades, iterable=False)

    return render_template('insiders.html',
                           insiders=trades,
                           title="Данные торговли совладельцев компании %s" % ticker,
                           )


@main.route('/api/<string:ticker>/analytics', methods=['GET', 'POST'])
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
            abort(404)
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

            if api in request.url:
                return get_response(difference)

            return render_template('analytics.html',
                                   difference=difference,
                                   title="Разница цен %s с %s по %s" % (ticker, date_from_value, date_to_value),
                                   )
        else:
            abort(404)
    return redirect(url_for('.ticker_view', ticker=ticker))


@main.route('/api/<string:ticker>/delta', methods=['GET', 'POST'])
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

            if api in request.url:
                return get_response(results)

            return render_template('delta.html',
                                   title="Минимальные периоды, когда цена %s (%s) изменялась более чем на %d" % (
                                       ticker, type, value),
                                   results=results,
                                   )
        else:
            abort(404)
    return redirect(url_for('.ticker_view', ticker=ticker))
