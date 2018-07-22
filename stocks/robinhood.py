#!/usr/bin/env python

import requests
from Robinhood import Robinhood
import config

# Getting Token for robinhood
# resp = requests.post('https://api.robinhood.com/api-token-auth/', json={'username':config.USERNAME, 'password':config.PASSWORD})
# resp.json()
# resp = requests.get('https://api.robinhood.com/watchlists/', headers={'Authorization': 'Token 3d49f8a975a7401a0616deed73397af728e0a1ed'})
# resp.status_code
# resp.json()
# resp = requests.get('https://api.robinhood.com/watchlists/Default', headers={'Authorization': 'Token 3d49f8a975a7401a0616deed73397af728e0a1ed'})
# resp.status_code
# resp.json()


#class Login(object):
#    def __init__(self):
#        self.my_trader = Robinhood.Robinhood()
#        self.logged_in = self.my_trader.login(username=config.USERNAME, password=config.PASSWORD)

class Authenticate(object):
    def __init__(self):
        self.my_trader = Robinhood.Robinhood()
        logged_in = self.my_trader.login(username=config.USERNAME, password=config.PASSWORD)

class Equity(object):
    def __init__(self, acct, ticker):
        #self.my_trader = Robinhood.Robinhood()
        self.ticker = ticker
        #logged_in = self.my_trader.login(username=config.USERNAME, password=config.PASSWORD)
        self.my_trader = acct.my_trader
        try:
            self.equity_ticker = self.my_trader.symbol(self.ticker)
        except Robinhood.RH_exception.InvalidTickerSymbol as e:
            self.equity_ticker = None
            return self.equity_ticker
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
        if self.instrument_info:
            return self.instrument_info[0]['list_date']
        else:
            return "Not Available"

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
