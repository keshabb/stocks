#!/usr/bin/env python

import sys
import webbrowser

etrade_news = 'https://www.etrade.wallst.com/v1/news/marketnews/marketnews.asp'
vanguard_news = 'https://investornews.vanguard/'
morningstar_news1 = 'http://library.morningstar.com/Markets/MarketsHome.aspx'
morningstar_news2 = 'http://library.morningstar.com/article/archive-articles.aspx'
morningstar_news3 = 'http://library.morningstar.com/Newsletters/Newsletters.aspx'
fidelity_news = 'https://www.fidelity.com/news/overview'
yahoo_news = 'https://finance.yahoo.com/'
google_news = 'https://finance.google.com/finance/market_news'
nasdaq_news = 'https://www.nasdaq.com/news/market-headlines.aspx'
investopedia_news = 'https://www.investopedia.com/news/'
zacks_news = 'https://www.zacks.com/'
barrons_news = 'https://www.barrons.com'
reuters_news = 'https://www.reuters.com/'
fool_news = 'https://www.fool.com/'
bogleheads_news = 'https://www.bogleheads.org/'
investorplace_news = 'https://investorplace.com/'
investor_news = 'https://www.investors.com/'
analystratings_news = 'http://www.analystratings.com/'
researchmarkets_news = 'https://www.researchandmarkets.com/'
businesswire_news = 'https://www.businesswire.com/portal/site/home/news/'


urls = [etrade_news, vanguard_news, morningstar_news1, morningstar_news2,
        morningstar_news3, fidelity_news, yahoo_news, google_news,
        nasdaq_news, investopedia_news, zacks_news, barrons_news,
        reuters_news, fool_news, bogleheads_news, investorplace_news,
        investor_news, analystratings_news, researchmarkets_news,
        businesswire_news]

for url in urls:
    webbrowser.open_new_tab(url)
