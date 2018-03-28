#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app
from app import db
from flask_script import Manager
from flask_script import Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))


def get_html():
    import requests
    with open('tickers.txt', 'r') as tickers_file:
        tickers = tickers_file.read()
        tickers = tickers.split('\n')
        print tickers
        for ticker in tickers:
            print(ticker)
            url = 'http://www.nasdaq.com/symbol/%s/historical' % ticker.lower()
            print(url)
            headers = {}
            r = requests.get(url, headers)
            with open('test_%s.html' % ticker.lower(), 'w') as out_file:
                out_file.write(r.text.encode('cp1251'))


def get_data(text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text)
    tickers_table = soup.find('div', {'class': ''})

with app.app_context():
    db.create_all()
    get_html()


if __name__ == '__main__':
    manager.run()


