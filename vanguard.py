#!/usr/bin/env python

import sys
import re
import click
import robinhood
import stocks
#from pandas_finance import api as yahoo_api
from pandas_finance import Equity
import get_yahoo_finance as yahoo_info

EQUITY_LIST = {'vg_down': 'vg_down', 'vg_up': 'vg_up', 'vg_active':
               'vg_active', 'vg_top_10_down': 'vg_top_10_down',
               'vg_top_10_up': 'vg_top_10_up'}

@click.command()
@click.argument('equities', nargs=1)
@click.option('--days', type=int, default=20, help='No. of days to get stock info of')
def get_ticker_info(equities, days):
    """
    Loops through ticker symbol and returns info on each symbol.
    equities = vg_down, vg_up, vg_active, vg_top_10_down, vg_top_10_up
    """
    if not validate_stocks_file(equities):
        click.echo("Ticker_file {} doesn't exists".format(equities))
        sys.exit(0)
    equity_file = "vanguard/{}.txt".format(EQUITY_LIST[equities])
    get_vg_ticker_info(equity_file, days)

def validate_stocks_file(tickers):
    if tickers in EQUITY_LIST.keys():
        return True
    else:
        return False


def get_vg_ticker_info(equity_file, days):
    with open(equity_file, 'r') as f:
        excluded_industry = ['Oil & Gas', 'REIT', 'Biotechnology']
        for line in f:
            # Skip if line has 'ETF', 'FUND', 'TRUST', 'THERA', 'PHARMA'
            ticker = re.search(r'\((.*?)\)',line).group(1)
            if ticker:
                #rb_client = robinhood.Equity(ticker)
                yahoo_ticker = Equity(ticker)
                yahoo_equity_summary = yahoo_info.get_summary(ticker)
                profile = yahoo_ticker.profile
                price = float(yahoo_equity_summary['Open'])
                if profile is None or price >= 50:
                    continue
                market_cap = yahoo_equity_summary.get('Market Cap', None)
                if market_cap:
                    if yahoo_equity_summary['Market Cap'].endswith('M'):
                        data = re.split(r'(\d+)', yahoo_equity_summary['Market Cap'])[1]
                        if int(data) < 50:
                            print "Skipping {} because of mkt cap below 50M".format(ticker)
                            continue
                else:
                    continue
                # Skip REIT
                industry = yahoo_ticker.industry
                if industry in excluded_industry:
                    continue
                stocks.get_stock_info(ticker, days)
                click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    sys.exit(0)
