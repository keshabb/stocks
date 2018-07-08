#!/usr/bin/env python

import subprocess
import click
import stocks
import sys


WATCHLISTS = {'watchlist': 'watching portfolio', 'canopy': 'canopy', 'chinese': 'Chinese', 'largecap': 'largecap', 'vgvcr': 'vgvcr', 'vgvdc': 'vgvdc', 'vgvgt': 'vgvgt', 'midcap': 'midcap', 'smallcap': 'smallcap', 'cyber': 'cyber', 'david': 'david', 'entertainment': 'entertainment', 'solar': 'solar', 'virtualreality': 'virtualreality', 'health': 'health', 'telecom': 'telecom', 'iot': 'iot', 'transport': 'transport', 'ipo': 'ipo', 'vgsmallcapgrowth': 'vgsmallcapgrowth', 'watchlist2018': 'watchlist2018', 'ibdgrowth': 'ibdgrowth', 'etradegrwoth': 'etradegrwoth'}
@click.command()
@click.argument('watchlist', nargs=1)
@click.option('--days', type=int, default=None, help='No. of days to get stock info of')
def etrade_watchlist_info(watchlist, days):
    """ Loops through portfolio symbol and returns info on each symbol.
        portfolio= {watchlist, chinese, largecap, vgvcr, vgvdc, vgvgt, mipcap, smallcap, cyber, david, entertainment, solar, virtualreality, health, telecom, iot, transport, ipo, vgsmallcapgrowth, vgsmallcapgrowth, watchlist2018, ibdgrowth, etradegrwoth}"""
    if not validate_watchlist(watchlist):
        click.echo("Watchlist {} doesn't exists".format(watchlist))
        sys.exit(0)
    get_name_and_symbol(watchlist, days)


def validate_watchlist(watchlist):
    if watchlist in WATCHLISTS.keys():
        return True
    else:
        return False

def get_name_and_symbol(watchlist, days):
    watch = "etrade/{}.csv".format(WATCHLISTS[watchlist])
    with open(watch, 'r') as watchlist_file:
        for line in watchlist_file:
            ticker = line.split(',')[0]
            resp = stocks.get_stock_info(ticker, None, days)
            if resp is None:
                continue
            click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    sys.exit(0)
