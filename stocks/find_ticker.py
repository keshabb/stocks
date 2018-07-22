#!/usr/bin/env python

import sys
import time
import requests
import click
import csv
from pandas_finance import api as yahoo_api

@click.command()
@click.argument('max-price', nargs=1)
@click.option('--min-price', default=None)
@click.option('--sector', default=None, help='Company sector. Valid values: "Healthcare", "Technology", "Consumer Goods", "Basic Materials", "Services", "Utilities", "Conglomerates", "Financial", "Industrial Goods"')
def get_stocks(max_price, min_price, sector):
    """ max_price: max price limit search for stock.
        min_price: min price limit for stock search.
        sector: Company sector.
    """

    with open('stocks.csv', 'rb') as csvfile:
        stock_reader = csv.reader(csvfile)
        next(stock_reader)
        for row in stock_reader:
            tick = yahoo_api.Equity(row[0])
            try:
                stock_price = tick.price
            except KeyError:
                continue
            if stock_price == 'N/A':
                continue
    #resp = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date=20170810&api_key=WjePZyesFpynS2nzq2so')
    #data = resp.json()
    #for d in data['datatable']['data']:
            if min_price is None:
                min_price = 0
            if float(stock_price) > float(min_price) and float(stock_price) < float(max_price):
                #tick = yahoo_api.Equity(d[0])
                profile = tick.profile
                if profile is None:
                    continue
                if sector:
                    company_sector = tick.sector
                    if sector != company_sector:
                        continue
                try:
                    market_cap = tick.mkt_cap
                except KeyError:
                    continue
                if market_cap is not None:
                    if market_cap.endswith('M'):
                        mkt_cap = market_cap.split('.')[0]
                        if int(mkt_cap) <= 200:
                            continue
                eps = tick.eps
                if float(eps) <= 0:
                    continue
                print "TICKER: {}, Industry: {}, Sector: {}, Market_Cap: {}, Price: {}, EPS: {}, PE-Ratio: {}".format(row[0], tick.industry, tick.sector, tick.mkt_cap, stock_price, eps, tick.PE_Ratio)
                #stock_row = '{},{},{},{},{},{},{}'.format(row[0], tick.industry, tick.sector, tick.mkt_cap, stock_price, eps, tick.PE_Ratio)
                #with open('technology_stocks.csv', 'wb') as tech_stocks:
                #    csv_writer = csv.writer(tech_stocks)
                #    csv_writer.writerow([stock_row])

def main():
    get_stocks()

if __name__ == '__main__':
    main()
