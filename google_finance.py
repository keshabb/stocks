#!/usr/bin/env python

import csv
import subprocess
import click
import stocks
import sys


PORTFOLIOS = {'keshab': 'Keshab Portfolio', 'watching': 'watching portfolio',
             'david': 'David Gardner', 'iot': 'IOT', 'telecom': 'Telecom',
             'health': 'Health', 'entertainment': 'Entertainment', 'etf': 'ETF',
             'virtual-reality': 'Virtual Reality', 'airlines': 'Airlines',
             'smallcap': 'SMALL CAP', 'midcap':'MID CAP', 'game': 'GAME'}
@click.command()
@click.argument('portfolio', nargs=1)
@click.option('--days', type=int, default=None, help='No. of days to get stock info of')
def get_google_portfolio_info(portfolio, days):
    """ Loops through portfolio symbol and returns info on each symbol.
        portfolio= {keshab, watching, david, iot, health, entertainment,
        virtual-reality, airlines, etf, telecom, midcap, smallcap, game, solar}"""
    if not validate_portfolio(portfolio):
        click.echo("Portfolio {} doesn't exists".format(portfolio))
        sys.exit(0)
    get_name_and_symbol(portfolio, days)


def validate_portfolio(portfolio):
    if portfolio in PORTFOLIOS.keys():
        return True
    else:
        return False

def get_name_and_symbol(portfolio, days):
    port = "{}.csv".format(PORTFOLIOS[portfolio])
    with open(port, 'r') as csvfile:
        spread_reader = csv.DictReader(csvfile)
        portfolio_stocks = {}
        for item in spread_reader:
            #print("{}\t{}".format(item['\xef\xbb\xbfName'], item['Symbol']))
            portfolio_stocks.update({item['\xef\xbb\xbfName']: item['Symbol']})
        #print portfolio_stocks
    #for name, ticker in portfolio_stocks.iteritems():
    for name, ticker in portfolio_stocks.iteritems():
        click.echo("\n")
        click.echo("Name: {}".format(name))
        #click.echo("ticker: {}".format(ticker))
        stocks.get_stock_info(ticker, days)
        click.pause(info="Press any key to continue...", err=False)
