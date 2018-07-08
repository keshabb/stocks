#!/usr/bin/env python

import stocks
import click
import sys


def get_name_and_symbol(days):
    with open('analyst_pick.txt', 'r') as analysts_pick:
        for line in analysts_pick:
            if line.startswith('#'):
                continue
            ticker = line.split()[0]
            resp = stocks.get_stock_info(ticker, None, days)
            if resp is None:
                continue
            click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    get_name_and_symbol(35)
