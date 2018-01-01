#!/usr/bin/env python

import requests
from Robinhood import Robinhood
import config

class Equity(object):
    def __init__(self, ticker):
        self.my_trader = Robinhood.Robinhood()
        self.ticker = ticker
        logged_in = self.my_trader.login(username=config.USERNAME, password=config.PASSWORD)
        self.equity_info = self.my_trader.fundamentals(self.ticker)
        self.instrument_info = self.my_trader.instruments(self.ticker)
        self.news = self.my_trader.get_news(ticker)

    @property
    def company_info(self):
        return self.equity_info['description'].encode('utf8')

    @property
    def market_cap(self):
        return self.equity_info['market_cap']

    @property
    def company_founded(self):
        return self.equity_info['year_founded']

    @property
    def company_ceo(self):
        return self.equity_info['ceo'].encode('utf8')
    
    @property
    def company_employees_total(self):
        return self.equity_info['num_employees']

    @property
    def high_52_weeks(self):
        return self.equity_info['high_52_weeks']

    @property
    def low_52_weeks(self):
        return self.equity_info['low_52_weeks']

    @property
    def company_dividend(self):
        return self.equity_info['dividend_yield']

    @property
    def company_pe_ratio(self):
        return self.equity_info['pe_ratio']

    @property
    def company_ipo_date(self):
        return self.instrument_info[0]['list_date']

    @property
    def company_news(self):
        news = self.my_trader.get_news(self.ticker)
        comp_news = []
        for item in news['results']:
           comp_news.append({'news_source': item['source'],
                              'news_title': item['title'],
                              'news_published_date': item['published_at'],
                              'news_url': item['url'],
                              'news_summary': item['summary']})
        return comp_news
