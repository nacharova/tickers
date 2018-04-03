import scrapy
import os
from ..items import InsidersParserItem
import datetime
import re


class InsidersSpider(scrapy.Spider):
    name = "insiders"
    max_page_number = 10

    def __init__(self, name=None, **kwargs):
        super(InsidersSpider, self).__init__(name, **kwargs)
        self.pages = dict()
        self.start_urls = self.get_urls()

    def get_urls(self):
        start_urls = []
        with open(os.path.join(os.curdir, '..', 'tickers.txt'), 'r') as tickers_file:
            tickers = tickers_file.read()
            tickers = tickers.split('\n')
            for ticker in tickers:
                start_urls.append('http://www.nasdaq.com/symbol/%s/insider-trades' % ticker.lower())
                self.pages[ticker.lower()] = 1
        return start_urls

    def parse(self, response):
        rows = response.css('div.genTable table > tr')
        for row in rows:
            cols = row.css('td')
            items = []
            for col in cols:
                items.append(col.css('::text').extract_first(default=""))
            items = tuple(map(str.strip, items[1:]))
            item = InsidersParserItem()
            item['ticker'] = response.url.split('/')[-2]
            item['insider'] = row.css('td>a::text').extract_first()
            if items[1] and any(items[:1]+items[1:]):
                item['relation'] = items[0]
                try:
                    date = datetime.datetime.strptime(items[1], '%m/%d/%Y')
                except:
                    if re.search(r'\d{1,2}:\d{1,2}', items[1]):
                        date = datetime.datetime.today()
                    else:
                        date = 0
                item['last_date'] = date
                item['transaction_type'] = items[2]
                item['owner_type'] = items[3]
                item['shares_traded'] = int(items[4].replace(',', '')) if items[4] else None
                item['last_price'] = float(items[5].replace(',', '')) if items[5] else None
                item['shares_held'] = int(items[6].replace(',', '')) if items[6] else None

                yield item

        next_page = response.css('a#quotes_content_left_lb_NextPage::attr(href)').extract_first()
        if next_page is not None and self.pages[item['ticker']] < self.max_page_number:
            self.pages[item['ticker']] += 1
            yield response.follow(next_page, callback=self.parse)
