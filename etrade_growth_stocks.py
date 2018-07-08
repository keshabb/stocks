#!/usr/bin/env python

import subprocess
import click
import stocks
import sys


def etrade_growth_stock_info(days=30):
    get_name_and_symbol(days)


def get_name_and_symbol(days):
    growth_stock_file = "etrade_growth_list.txt"
    with open(growth_stock_file, 'r') as f:
        for line in f:
            ticker = line.split('\t')[2]
            resp = stocks.get_stock_info(ticker, None, days)
            if resp is None:
                continue
            click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    etrade_growth_stock_info()
