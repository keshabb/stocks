#!/usr/bin/env python

import sys
import webbrowser

while True:
    ticker = raw_input("Enter the ticker:")
    if ticker.lower() == 'exit':
        sys.exit(0)

    etrade_research = 'https://www.etrade.wallst.com/v1/stocks/research/research.asp?symbol={}'.format(ticker)
#    etrade_snapshot = 'https://www.etrade.wallst.com/v1/stocks/snapshot/snapshot.asp?symbol={}'.format(ticker)
#    etrade_chart = 'https://www.etrade.wallst.com/v1/stocks/charts/charts.asp?symbol={}'.format(ticker)
#    etrade_news = 'https://www.etrade.wallst.com/v1/stocks/news/search_results.asp?symbol={}'.format(ticker)
#    etrade_fundamental = 'https://www.etrade.wallst.com/v1/stocks/fundamentals/fundamentals.asp?symbol={}'.format(ticker)
    vanguard_report = 'https://personal.vanguard.com/us/secfunds/stocks/reports?Ticker={}'.format(ticker)
#    vanguard_financial = 'https://personal.vanguard.com/us/secfunds/stocks/financials?Ticker={}'.format(ticker)
#    vanguard_earning = 'https://personal.vanguard.com/us/secfunds/stocks/earnings?Ticker={}'.format(ticker)
    morningstar_quote = 'http://library.morningstar.com/stock/quote?t={}&region=USA'.format(ticker)
#    morningstar_industry_peers = 'http://library.morningstar.com/stock/industry-peer?t={}&region=USA'.format(ticker)
#    morningstar_performance = 'http://library.morningstar.com/stock/Performance/total-returns?t={}&region=USA'.format(ticker)
#    morningstar_key_ratios = 'http://library.morningstar.com/stock/key-ratios?t={}&region=USA'.format(ticker)
#    morningstar_financial = 'http://library.morningstar.com/stock/financials/income-statement?t={}&region=USA'.format(ticker)
#    morningstar_valuation = 'http://library.morningstar.com/stock/valuation/price-ratio?t={}&region=USA'.format(ticker)
#    morningstar_shareholders = 'http://library.morningstar.com/stock/ownership/shareholders-overview?t={}&region=USA'.format(ticker)
    fidelity_snapshot = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}'.format(ticker)
#    fidelity_key_stats = 'https://eresearch.fidelity.com/eresearch/evaluate/fundamentals/keyStatistics.jhtml?stockspage=keyStatistics?symbol={}'.format(ticker)
#    fidelity_earning = 'https://eresearch.fidelity.com/eresearch/evaluate/fundamentals/earnings.jhtml?symbol={}'.format(ticker)
#    fidelity_financial = 'https://eresearch.fidelity.com/eresearch/evaluate/fundamentals/financials.jhtml?stockspage=financials?symbol={}'.format(ticker)
    yahoo_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(ticker, ticker)
    schwab_stats = 'https://client.schwab.com/secure/cc/research/stocks/stocks.html?path=/research/Client/Stocks/Earnings/Ratios&symbol={}'.format(ticker)

    urls = [etrade_research, vanguard_report, morningstar_quote, fidelity_snapshot, schwab_stats, yahoo_stats]

    for url in urls:
        webbrowser.open_new_tab(url)


