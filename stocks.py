#/!/usr/bin/env python

import os
import sys
import requests
import click
from datetime import date, datetime, timedelta
import collections
import robinhood
import config
import etrade_api
from pandas_finance import Equity
import get_yahoo_finance as yahoo_info
from prettytable import PrettyTable

today = date.today()
AV_API_KEY = config.AV_API_KEY
host = 'https://www.alphavantage.co'
etrade_acct_obj = etrade_api.Account()
rh_acct_obj = robinhood.Authenticate()
session = requests.Session()

class Stocks(object):
    def __init__(self):
        pass


class StockHTTPError(requests.HTTPError):
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
    yahoo_ticker_obj = Equity(ticker)
    ticker_obj = etrade_api.Equity(etrade_acct_obj, ticker)
    if ticker_obj.quote_all is None:
        return None
    rb_client = robinhood.Equity(rh_acct_obj, ticker)
    if rb_client.equity_ticker is None:
        return None
    yahoo_summary_info = yahoo_info.get_summary(ticker)
    yahoo_equity_info = yahoo_info.get_stats(ticker)
    trade_date, end_date = get_end_date(days)
    trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
    sma_10 = ticker_10_sma(ticker)
    sma_21 = ticker_21_sma(ticker)
    sma_50 = ticker_50_sma(ticker)
    sma_200 = ticker_200_sma(ticker)
    rsi = get_rsi(ticker)
    url = '{}/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.\
          format(host, ticker, AV_API_KEY)
    resp = session.get(url)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise StockHTTPError(e)
    data = resp.json()
    symbol_table = PrettyTable(['Name', 'Ticker', 'Sector', 'Industry', 'Date', 'Company Founded', 'CEO', 'IPO Date', 'Total Employee', 'Market Cap'])
    if name is not None:
        symbol_table.add_row([name, data['Meta Data']['2. Symbol'], yahoo_ticker_obj.sector, yahoo_ticker_obj.industry, today,
                              rb_client.company_founded, rb_client.company_ceo, rb_client.company_ipo_date,
                              rb_client.company_employees_total, market_cap(rb_client.market_cap)])
        #click.echo("Name: {}".format(name))
    else:
        symbol_table.add_row(['None', data['Meta Data']['2. Symbol'], yahoo_ticker_obj.sector, yahoo_ticker_obj.industry, today,
                              rb_client.company_founded, rb_client.company_ceo, rb_client.company_ipo_date,
                              rb_client.company_employees_total, market_cap(rb_client.market_cap)])
        #symbol_table.add_row(['None', data['Meta Data']['2. Symbol'], yahoo_ticker_obj.sector, yahoo_ticker_obj.industry, today])
    #click.echo("Ticker: {}, Sector: {}, Industry:{}, Date: {}".\
    #           format(click.style(data['Meta Data']['2. Symbol'], fg='red'),
    #                  yahoo_ticker_obj.sector, yahoo_ticker_obj.industry,
    #                  today))
    click.echo(symbol_table)
    click.echo("Company Summary: {}".format(rb_client.company_info))
    price_data = data['Time Series (Daily)']
    close_price_list = []
    sorted_price_data = collections.OrderedDict(sorted(price_data.items(),
                                                       reverse=True))
    ticker_table = PrettyTable(['Date', 'Open Price', 'Close price', 'High ($)', 'Low ($)', 'Fluctuate ($)', 'Fluctuate (%)', 'Change ($)', 'Change (%)', 'Volume(k)'])
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
            click.echo(ticker_table)
            #company_info_table = PrettyTable(['Company Founded', 'CEO', 'IPO Date', 'Total Employee', 'Market Cap'])
            #company_info_table.add_row([rb_client.company_founded, rb_client.company_ceo, rb_client.company_ipo_date,
            #                            rb_client.company_employees_total, market_cap(rb_client.market_cap)])
            #click.echo(company_info_table)
            #click.echo("Company Founded: {}\t\tCEO: {}\tIPO date: {}\t\t"
            #           "Total Employee: {}".format(click.style(str(rb_client.company_founded), fg='red'),
            #            rb_client.company_ceo, click.style(rb_client.company_ipo_date, fg='red'),
            #            rb_client.company_employees_total))
            snap_ratio_table = PrettyTable(['PE', 'EPS', 'Estimated EPS', 'Trailing PE', 'Forward PE',
                                            'P/S (ttm)', 'P/B (mrq)', 'Current Ratio (mrq)', 'Gross Profit(ttm)', 'Profit Margin', 'Operating Margin(ttm)', 'ROE', 'ROA'])
            snap_ratio_table.add_row([rb_client.company_pe_ratio, ticker_obj.eps, ticker_obj.estEarnings, yahoo_equity_info['Trailing P/E'],
                                      yahoo_equity_info['Forward P/E 1'], yahoo_equity_info['Price/Sales (ttm)'], yahoo_equity_info['Price/Book (mrq)'],
                                      yahoo_equity_info['Current Ratio (mrq)'], yahoo_equity_info['Gross Profit (ttm)'],
                                      yahoo_equity_info['Profit Margin'], yahoo_equity_info['Operating Margin (ttm)'],
                                      yahoo_equity_info['Return on Equity (ttm)'], yahoo_equity_info['Return on Assets (ttm)']])
            click.echo(snap_ratio_table)
            #click.echo("Market Cap: {}\tPE: {}\t\tEPS: {}\t\t\t"
            #           "Dividend Yield: {}\t\tDividend Per Share: {}\t"
            #           "Estimated EPS: {}".\
            #            format(market_cap(rb_client.market_cap),
            #            click.style(str(rb_client.company_pe_ratio), fg='red'),
            #            ticker_obj.eps,
            #            ticker_obj.dividend,
            #            ticker_obj.annualDividend,
            #            ticker_obj.estEarnings))
            snap_financial_table = PrettyTable(['Revenue per Share', 'Qtr Revenue Growth (yoy)', 'Qtr Earnings Growth (yoy)', 'Total Debt/Equity (mrq)',
                                                'Book Value/Share (mrq)', 'Total Cash/Share (mrq)'])
            snap_financial_table.add_row([yahoo_equity_info['Revenue Per Share (ttm)'], yahoo_equity_info['Quarterly Revenue Growth (yoy)'],
                                          yahoo_equity_info['Quarterly Earnings Growth (yoy)'], yahoo_equity_info['Total Debt/Equity (mrq)'],
                                          yahoo_equity_info['Book Value Per Share (mrq)'], yahoo_equity_info['Total Cash Per Share (mrq)']])
            click.echo(snap_financial_table)
            #click.echo("Trailing PE: {}\t\tForward PE: {}\tP/S (ttm): {}\t\t\t"
            #           "P/B (mrq): {}\t\t\tBeta: {}\t\t\tProfit Margin: {}\n"
            #           "Operating Margin(ttm): {}\tROE: {}\t\tROA: {}\t\t\tRevenue per Share: {}\t"
            #           "Gross Profit(ttm): {}\tCurrent Ratio (mrq): {}\nQuarterly Revenue Growth (yoy): {}\t\t\t"
            #           "Quarterly Earnings Growth (yoy): {}\t\t\t\tTotal Debt/Equity (mrq): {}\n"
            #           "Book Value Per Share (mrq): {}\t\t\tTotal Cash Per Share (mrq): {}\t\t\t\t 1 yr target: {}".
            #           format(yahoo_equity_info['Trailing P/E'], yahoo_equity_info['Forward P/E 1'],
            #                  yahoo_equity_info['Price/Sales (ttm)'], yahoo_equity_info['Price/Book (mrq)'],
            #                  yahoo_equity_info['Beta'], yahoo_equity_info['Profit Margin'],
            #                  yahoo_equity_info['Operating Margin (ttm)'],
            #                  yahoo_equity_info['Return on Equity (ttm)'],
            #                  yahoo_equity_info['Return on Assets (ttm)'],
            #                  yahoo_equity_info['Revenue Per Share (ttm)'],
            #                  yahoo_equity_info['Gross Profit (ttm)'],
            #                  yahoo_equity_info['Current Ratio (mrq)'],
            #                  yahoo_equity_info['Quarterly Revenue Growth (yoy)'],
            #                  yahoo_equity_info['Quarterly Earnings Growth (yoy)'],
                              #yahoo_equity_info['Total Cash (mrq)'],
            #                  yahoo_equity_info['Total Debt/Equity (mrq)'],
            #                  yahoo_equity_info['Book Value Per Share (mrq)'],
            #                  yahoo_equity_info['Total Cash Per Share (mrq)'],
            #                  yahoo_summary_info['1y Target Est']))
#            click.echo("Market Cap: {}, PE: {},".\
#                        format(market_cap(rb_client.market_cap),
#                        click.style(str(rb_client.company_pe_ratio), fg='red')))
            snap_low_high_table = PrettyTable(['1 yr target', 'RSI', 'Beta', 'Dividend Yield', 'Dividend/Share', 'Highest', 'Lowest', '52 week high', '52 week low', 'SMA10', 'SMA21', 'SMA50', 'SMA200'])
            snap_low_high_table.add_row([yahoo_summary_info['1y Target Est'], str(rsi), yahoo_equity_info['Beta'], ticker_obj.dividend, ticker_obj.annualDividend,
                                         str(max(close_price_list)), str(min(close_price_list)), str(rb_client.high_52_weeks),
                                         str(rb_client.low_52_weeks), sma_10, sma_21, sma_50, sma_200])
            click.echo(snap_low_high_table)
            #click.echo("RSI: {}\tHighest: {}\tLowest: {}\t52 week high: {}\t"
            #           "52 week low: {}\tSMA10: {}\tSMA21: {}\tSMA50: {}\t"
            #           "SMA200: {}".format(click.style(str(rsi), fg='red'),
            #                               click.style(str(max(close_price_list)), fg='red'),
            #                               click.style(str(min(close_price_list)), fg='red'),
            #                               click.style(str(rb_client.high_52_weeks), fg='red'),
            #                               click.style(str(rb_client.low_52_weeks), fg='red'),
            #                               sma_10, sma_21, sma_50, sma_200))
            return True
        fluctuate = get_volatility(float(v['2. high']), float(v['3. low']))
        fluctuate_percent = get_volatility_percent(fluctuate, float(v['4. close']))
        try:
            change = get_price_change(float(v['4. close']), float(price_data[prev_date]['4. close']))
        except KeyError:
            continue
        change_percent = get_price_change_percent(change, float(price_data[prev_date]['4. close']))
        vol = int(v['5. volume']) / 1000
        close_price_list.append(float(v['4. close']))
        ticker_table.add_row([k, round(float(v['1. open']), 3),
                              round(float(v['4. close']), 3),
                              round(float(v['2. high']),3),
                              round(float(v['3. low']),3),
                              round(fluctuate, 3),
                              round(fluctuate_percent, 2),
                              round(change, 2),
                              round(change_percent, 2), vol])

def get_volatility(high, low):
    return high - low

def get_volatility_percent(fluctuate, close):
    try:
        fluctuate_percent = (fluctuate / close) * 100
    except ZeroDivisionError:
        fluctuate_percent = 9999.99
    return fluctuate_percent

def get_price_change(close, prev_close):
    return close - prev_close

def get_price_change_percent(change, prev_close):
    try:
        change_percent = (change / prev_close) * 100
    except ZeroDivisionError:
        change_percent = 9999.99
    return change_percent

#def ticker_15_sma(ticker):
#    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=15&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
#    resp = session.get(sma_url)
#    status = check_success_code(resp)
#    if status == 'SUCCESS':
#        if resp.json()['Technical Analysis: SMA']:
#            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
#            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
#        else:
#            return 0


def get_rsi(ticker):
    rsi_url = '{}/query?function=RSI&symbol={}&interval=daily&time_period=14&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = session.get(rsi_url)
    rsi_date = resp.json()['Meta Data']['3: Last Refreshed']
    rsi_data = resp.json()['Technical Analysis: RSI']
    rsi = rsi_data[rsi_date]['RSI']
    return rsi


def ticker_10_sma(ticker):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=10&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = session.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def ticker_21_sma(ticker):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=21&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = session.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def ticker_50_sma(ticker):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=50&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = session.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def ticker_200_sma(ticker):
    sma_url = '{}/query?function=SMA&symbol={}&interval=daily&time_period=200&series_type=close&apikey={}'.format(host, ticker, AV_API_KEY)
    resp = session.get(sma_url)
    status = check_success_code(resp)
    if status == 'SUCCESS':
        if resp.json()['Technical Analysis: SMA']:
            last_refresh_date = resp.json()['Meta Data']['3: Last Refreshed']
            return resp.json()['Technical Analysis: SMA'][last_refresh_date]['SMA']
        else:
            return 0

def market_cap(cap):
    if cap is not None:
        if float(cap) < 1000000000:
            market_cap = float(cap) / 1000000
            return str(market_cap) + ' Mil'
        if float(cap) > 1000000000:
            market_cap = float(cap) / 1000000000
            return str(market_cap) + ' Bil'
    return cap

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
