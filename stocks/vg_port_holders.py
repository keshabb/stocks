#!/usr/bin/env python

import subprocess
import click
import stocks
import sys


PORTFOLIOS = {'vgt': 'VGT', 'vcr': 'VCR', 'vdc': 'VDC', 'vbk': 'VBK'}
@click.command()
@click.argument('portfolio', nargs=1)
@click.option('--days', type=int, default=None, help='No. of days to get stock info of')
def get_vg_portfolio_holder_info(portfolio, days):
    """ Loops through portfolio symbol and returns info on each symbol.
        portfolio= {vgt, vcr}"""
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
    port = "vanguard/{}.txt".format(PORTFOLIOS[portfolio])
    with open(port, 'r') as port_file:
        for line in port_file:
            ticker, name = line.split()[0], line.split()[1]
            resp = stocks.get_stock_info(ticker,name, days)
            if resp is None:
                continue
            click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    sys.exit(0)
