#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app
from app import db
from flask_script import Manager
from flask_script import Shell
import requests
from bs4 import BeautifulSoup
from app.main.models import Tickers

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))


def get_html():
    with open('tickers.txt', 'r') as tickers_file:
        tickers = tickers_file.read()
        tickers = tickers.split('\n')
        for ticker in tickers:
            url = 'http://www.nasdaq.com/symbol/%s/historical' % ticker.lower()
            print(url)
            r = requests.get(url)
            with open('test_%s.html' % ticker.lower(), 'w') as out_file:
                out_file.write(r.text)
                get_tickers(r.text, ticker)


def get_tickers(text, name):
    soup = BeautifulSoup(text, "html.parser")
    gen_table = soup.find('div', {'class': 'genTable'})
    rows = gen_table.find('table').find('tbody').find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        Tickers.add(name,
                    columns[0].text,
                    float(columns[1].text.replace(',', '')),
                    float(columns[2].text.replace(',', '')),
                    float(columns[3].text.replace(',', '')),
                    float(columns[4].text.replace(',', '')),
                    int(columns[5].text.replace(',', '')))
    db.session.commit()


with app.app_context():
    db.create_all()
    get_html()


if __name__ == '__main__':
    manager.run()


