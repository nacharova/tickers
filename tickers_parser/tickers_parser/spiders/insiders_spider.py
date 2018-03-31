import scrapy
import os
from ..items import InsidersParserItem


class InsidersSpider(scrapy.Spider):
    name = "insiders"

    def __init__(self, name=None, **kwargs):
        super(InsidersSpider, self).__init__(name, **kwargs)
        self.start_urls = self.get_urls()

    def get_urls(self):
        start_urls = []
        with open(os.path.join(os.curdir, '..', 'tickers.txt'), 'r') as tickers_file:
            tickers = tickers_file.read()
            tickers = tickers.split('\n')
            for ticker in tickers:
                start_urls.append('http://www.nasdaq.com/symbol/%s/insider-trades' % ticker.lower())
        return start_urls

    def parse(self, response):
        rows = response.css('div.genTable table > tr')
        for row in rows:
            cols = row.css('td')
            items = []
            for col in cols:
                items.append(col.css('::text').extract_first(default=""))
            items = tuple(map(str.strip, items))
            # cols = tuple(map(str.strip, row.css('td::text').extract()))
            item = InsidersParserItem()
            item['ticker'] = response.url.split('/')[-2]
            item['insider'] = row.css('td>a::text').extract_first()
            item['relation'] = items[0]
            item['last_date'] = items[1]
            item['transaction_type'] = items[2]
            item['owner_type'] = items[3]
            item['shares_traded'] = items[4]
            item['last_price'] = items[5]
            item['shares_held'] = items[6]

            yield item
