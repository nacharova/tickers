import scrapy
import os
from ..items import TickersParserItem
import datetime


class TickersSpider(scrapy.Spider):
    name = "tickers"
    # target = 'price'

    def __init__(self, name=None, **kwargs):
        super(TickersSpider, self).__init__(name, **kwargs)
        self.start_urls = self.get_urls()

    def get_urls(self):
        start_urls = []
        with open(os.path.join(os.curdir, '..', 'tickers.txt'), 'r') as tickers_file:
            tickers = tickers_file.read()
            tickers = tickers.split('\n')
            for ticker in tickers:
                start_urls.append('http://www.nasdaq.com/symbol/%s/historical' % ticker.lower())
        return start_urls

    def parse(self, response):
        rows = response.css('div.genTable table tbody tr')
        for row in rows:
            cols = tuple(map(str.strip, row.css('td::text').extract()))
            item = TickersParserItem()
            item['ticker'] = response.url.split('/')[-2]
            if cols[0] and any(cols[1:]):
                try:
                    date = datetime.datetime.strptime(cols[0], '%m/%d/%Y')
                except:
                    import re
                    if re.search(r'\d{1,2}:\d{1,2}', cols[0]):
                        date = datetime.datetime.today()

                item['date'] = date
                item['open_price'] = float(cols[1]) if cols[1] else None
                item['high'] = float(cols[2]) if cols[2] else None
                item['low'] = float(cols[3]) if cols[3] else None
                item['close_last'] = float(cols[4]) if cols[4] else None
                item['volume'] = float(cols[5].replace(',', '')) if cols[5] else None

                yield item

