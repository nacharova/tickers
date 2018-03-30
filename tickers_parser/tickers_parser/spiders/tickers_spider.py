import scrapy
import os
from ..items import TickersParserItem


class TickersSpider(scrapy.Spider):
    name = "tickers"

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
            item['name'] = response.url.split('/')[-2]
            item['date'] = cols[0]
            item['open'] = cols[1]
            item['high'] = cols[2]
            item['low'] = cols[3]
            item['close_last'] = cols[4]
            item['volume'] = cols[5]

            yield item

