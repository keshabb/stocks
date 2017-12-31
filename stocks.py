#!/usr/bin/env python

import os
import sys
import requests
import click
from datetime import date, datetime, timedelta
import collections
import pandas as pd
import robinhood
import config
import etrade_api

today = date.today()
AV_API_KEY = config.AV_API_KEY
etrade_acct_obj = etrade_api.Account()
host = 'https://www.alphavantage.co'

class Stocks(object):
    def __init__(self):
        pass


def get_end_date(days):
    default_days = 30
    week_day = datetime.today().weekday()
    if week_day == 5:
        trade_date = today - timedelta(days=1)
    elif week_day == 6:
        trade_date = today - timedelta(days=2)
    else:
        trade_date = today
    trade_date = trade_date.strftime('%Y-%m-%d')
    if days:
        end_date = today - timedelta(days=days)
    else:
        end_date = today - timedelta(days=default_days)
    return trade_date, end_date


def get_prev_close_date(cur_trade_date):
    """ Returns the day before weekend """
    weekday = cur_trade_date.weekday()
    if weekday == 0:
        prev_close_date = cur_trade_date - timedelta(days=3)
    elif weekday == 5:
        prev_close_date = cur_trade_date - timedelta(days=2)
    else:
        prev_close_date = cur_trade_date - timedelta(days=1)
    return prev_close_date


@click.argument('ticker', nargs=1)
@click.option('--days', type=int, default=None,
              help='No. of days to get stock info of')
@click.command()
def stock_info(ticker, days):
    get_stock_info(ticker, None, days)


def get_stock_info(ticker, name=None, days=None):
    """ Returns ticker info """
    ticker_obj = etrade_api.Equity(etrade_acct_obj, ticker)
    rb_client = robinhood.Equity(ticker)
    trade_date, end_date = get_end_date(days)
    trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
    url = '{}/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(host, ticker, AV_API_KEY)
    sma_15 = ticker_15_sma(ticker, trade_date)
    sma_30 = ticker_30_sma(ticker, trade_date)
    sma_60 = ticker_60_sma(ticker, trade_date)
    sma_200 = ticker_200_sma(ticker, trade_date)
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        if name is not None:
            click.echo("Name: {}".format(name))
        click.echo("Ticker: {}, Date: {}".format(click.style(data['Meta Data']['2. Symbol'], fg='red'), today))
        click.echo("Company Summary: {}".format(rb_client.company_info))
        price_data = data['Time Series (Daily)']
        close_price_list = []
        sorted_price_data = collections.OrderedDict(sorted(price_data.items(),
                                                           reverse=True))
        for k, v in sorted_price_data.items():
            if ':' in k:
                k = datetime.strptime(k, '%Y-%m-%d %H:%M:%S').date()
            else:
                k = datetime.strptime(k, '%Y-%m-%d').date()
            prev_date = get_prev_close_date(k)
            prev_date_str = datetime.strftime(prev_date, '%Y-%m-%d')
            prev_close_date = price_data.get(prev_date_str, None)
            if prev_close_date is None:
                prev_date = get_prev_close_date(k - timedelta(days=1))
            prev_date = datetime.strftime(prev_date, '%Y-%m-%d')
            if k < end_date:
                click.echo("Company Founded: {}, Company CEO: {}, IPO date: {},"
                            "Total Employee: {}".format(click.style(str(rb_client.company_founded), fg='red'),
                            rb_client.company_ceo, click.style(rb_client.company_ipo_date, fg='red'),
                            rb_client.company_employees_total))
                click.echo("Market Cap: {}, PE: {}, EPS: {},"
                           "Dividend Yield: {}, Dividend Per Share: {},"
                           "Estimated EPS: {}".\
                            format(market_cap(rb_client.market_cap),
                            click.style(str(rb_client.company_pe_ratio), fg='red'),
                            ticker_obj.eps,
                            ticker_obj.dividend,
                            ticker_obj.annualDividend,
                            ticker_obj.estEarnings))
#                click.echo("EPS: {}".format(ticker_obj.eps))
                click.echo("Highest: {}, Lowest: {}, Days high: {}, Days low: {},"
                        "52 week high: {}, 52 week low: {}, SMA15: {}, SMA30: {},"
                        "SMA60: {}, SMA200: {}".format(click.style(str(max(close_price_list)), fg='red'),
                                                       click.style(str(min(close_price_list)), fg='red'),
                                                       click.style(str(max(close_price_list)), fg='red'),
                                                       click.style(str(min(close_price_list)), fg='red'),
                                                       click.style(str(rb_client.high_52_weeks), fg='red'),
                                                       click.style(str(rb_client.low_52_weeks), fg='red'),
                                                       sma_15, sma_30, sma_60, sma_200))
                return True
            fluctuate = float(v['2. high']) - float(v['3. low'])
            try:
                fluctuate_percent = (fluctuate / float(v['4. close'])) * 100
            except ZeroDivisionError:
                fluctuate_percent = 9999.99
            try:
                change = float(v['4. close']) - float(price_data[prev_date]['4. close'])
            except KeyError:
                continue
            try:
                change_percent = (change / float(price_data[prev_date]['4. close'])) * 100
            except ZeroDivisionError:
                change_percent = 9999.99
            vol = int(v['5. volume']) / 1000
            close_price_list.append(float(v['4. close']))
            click.echo("Date: {}, Open Price: ${}, Close price: ${},"
                       "Fluctuate: ${}, Fluctuate %: {}, Change: ${},"
                       "Change %: {}, Volume: {} k".
                       format(k, round(float(v['1. open']), 3),
                              round(float(v['4. close']), 3),
                              round(fluctuate, 3), round(fluctuate_percent, 2),
                              round(change, 2), round(change_percent, 2), vol))
    else:
        click.echo("Failed to get data for {}".format(ticker))


def ticker_15_sma(ticker, trade_date):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=15&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = requests.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0


def ticker_30_sma(ticker, trade_date):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=30&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = requests.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def ticker_60_sma(ticker, trade_date):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=60&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = requests.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def ticker_200_sma(ticker, trade_date):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=200&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = requests.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def market_cap(cap):
    if float(cap) < 1000000000:
        market_cap = float(cap) / 1000000
        return str(market_cap) + ' Mil'
    if float(cap) > 1000000000:
        market_cap = float(cap) / 1000000000
        return str(market_cap) + ' Bil'

def _check_status_code(response, content_check=None):
    if response.status_code == 200:
        return 'SUCCESS'
    else:
        return 'FAIL'

def check_success_code(response, content_check=None):

    return _check_status_code(response, content_check=None)

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
