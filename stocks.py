#!/usr/bin/env python

import sys
import requests
import click
from datetime import date, datetime, timedelta
import collections

today = date.today()

STOCKS = ['TWTR', 'CRM', 'AMD', 'NVDA', 'BABA', 'NFLX', 'MSFT', 'SHOP', 'MOMO', 'SWIR', 'ATVI', 'EXTR', 'PLNT',
          'SIRI', 'TSM', 'BOFI']


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
    return end_date


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



#@click.argument('stock', nargs=1)
@click.option('--days', type=int, default=None, help="No. of days to get stock info of")
@click.command()
def get_my_stocks_info(days):
    for ticker in STOCKS:
        get_stock_info(ticker, days)
        click.echo("\n")
        click.pause(info='Press any key to continue ...', err=False)


@click.argument('ticker', nargs=1)
@click.option('--days', type=int, default=None, help='No. of days to get stock info of')
@click.command()
def stock_info(ticker, days):
    get_stock_info(ticker, days)


def get_stock_info(ticker, days=None):
    """ Returns ticker info """
    end_date = get_end_date(days)
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker, API_KEY)
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        click.echo("Ticker: {}, Date: {}".format(click.style(data['Meta Data']['2. Symbol'],fg='blue'), today))
        price_data = data['Time Series (Daily)']
        close_price_list = []
        sorted_price_data = collections.OrderedDict(sorted(price_data.items(), reverse=True))
        for k, v in sorted_price_data.items():
            if ':' in k:
                k = datetime.strptime(k, '%Y-%m-%d %H:%M:%S').date()
            else:
                k = datetime.strptime(k, '%Y-%m-%d').date()
            prev_date = get_prev_close_date(k)
            prev_date_str = datetime.strftime(prev_date,'%Y-%m-%d')
            prev_close_date = price_data.get(prev_date_str, None)
            if prev_close_date is None:
                prev_date = get_prev_close_date(k - timedelta(days=1))
            prev_date = datetime.strftime(prev_date,'%Y-%m-%d')
            if k < end_date:
                click.echo("High: {}, Low: {}".format(max(close_price_list), min(close_price_list)))
                return True
            fluctuate = float(v['2. high']) - float (v['3. low'])
            fluctuate_percent = (fluctuate / float(v['4. close'])) * 100
            change = float(v['4. close']) - float(price_data[prev_date]['4. close'])
            change_percent = (change / float(price_data[prev_date]['4. close'])) * 100
            vol = int(v['5. volume']) / 1000
            close_price_list.append(float(v['4. close']))
            click.echo("Date: {}, Open Price: ${}, Close price: ${}, Fluctuate: ${}, Fluctuate %: {},"
                       "Change: ${}, Change %: {}, Volume: {} k".format(k, round(float(v['1. open']), 3),
                        round(float(v['4. close']), 3), round(fluctuate, 3), round(fluctuate_percent, 2),
                        round(change, 2), round(change_percent, 2),  vol))
    else:
        click.echo("Failed to get data for {}".format(ticker))
     

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
