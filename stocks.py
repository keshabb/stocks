#!/usr/bin/env python

import sys
import requests
from pandas_yahoo_finance.pandas_finance import api
import click
from datetime import date, datetime, timedelta
import collections
import pandas as pd

today = date.today()

API_KEY = ''


class Stocks(object):
    def __init__(self):
        pass


def get_end_date(days):
    default_days = 20
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


# @click.argument('stock', nargs=1)
@click.option('--days', type=int, default=None,
              help="No. of days to get stock info of")
@click.command()
def get_my_stocks_info(days):
    for ticker in STOCKS:
        get_stock_info(ticker, days)
        click.echo("\n")
        click.pause(info='Press any key to continue ...', err=False)


@click.argument('ticker', nargs=1)
@click.option('--days', type=int, default=None,
              help='No. of days to get stock info of')
@click.command()
def stock_info(ticker, days):
    get_stock_info(ticker, days)


def get_stock_info(ticker, days=None):
    """ Returns ticker info """
    trade_date, end_date = get_end_date(days)
    trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker, API_KEY)
    print "trade_date: {}".format(trade_date)
    sma_15 = ticker_15_sma(ticker, trade_date)
    sma_30 = ticker_30_sma(ticker, trade_date)
    sma_60 = ticker_60_sma(ticker, trade_date)
    sma_200 = ticker_200_sma(ticker, trade_date)
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        click.echo("Ticker: {}, Date: {}".format(click.style(data['Meta Data']['2. Symbol'], fg='blue'), today))
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
            print "K: {}".format(k)
            if k < end_date:
                api_client = api.Equity(ticker)
                # click.echo("Market Cap: {}, P/E: {}, EPS: {}".
                #             format(api_client.mkt_cap, api_client.PE_Ratio,
                #                    api_client.eps))
                click.echo("High: {}, Low: {}, P/E: {}, EPS: {}, SMA15: {},"
                           "SMA30: {}, SMA60: {}, SMA200: {}".
                            format(max(close_price_list), min(close_price_list),
                                   api_client.PE_Ratio, api_client.eps, sma_15[datetime.strftime(trade_date, '%Y-%m-%d')]['SMA'],
                                   sma_30[datetime.strftime(trade_date, '%Y-%m-%d')]['SMA'], sma_60[datetime.strftime(trade_date, '%Y-%m-%d')]['SMA'], sma_200[datetime.strftime(trade_date, '%Y-%m-%d')]['SMA']))
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
    sma_url = 'https://www.alphavantage.co/query?function=SMA&symbol={}&interval=daily&time_period=15&series_type=close&apikey={}'.format(ticker, API_KEY)
    resp = requests.get(sma_url)
    if resp:
        return resp.json()['Technical Analysis: SMA']
    else:
        return 0


def ticker_30_sma(ticker, trade_date):
    sma_url = 'https://www.alphavantage.co/query?function=SMA&symbol={}&interval=daily&time_period=30&series_type=close&apikey={}'.format(ticker, API_KEY)
    resp = requests.get(sma_url)
    if resp:
        return resp.json()['Technical Analysis: SMA']
    else:
        return 0

def ticker_60_sma(ticker, trade_date):
    sma_url = 'https://www.alphavantage.co/query?function=SMA&symbol={}&interval=daily&time_period=60&series_type=close&apikey={}'.format(ticker, API_KEY)
    resp = requests.get(sma_url)
    if resp:
        return resp.json()['Technical Analysis: SMA']
    else:
        return 0

def ticker_200_sma(ticker, trade_date):
    sma_url = 'https://www.alphavantage.co/query?function=SMA&symbol={}&interval=daily&time_period=200&series_type=close&apikey={}'.format(ticker, API_KEY)
    resp = requests.get(sma_url)
    if resp:
        return resp.json()['Technical Analysis: SMA']
    else:
        return 0

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
