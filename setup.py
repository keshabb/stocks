from setuptools import setup, find_packages
setup(
    name = 'stock',
    description = 'Python script to get stock info',
    version = '1.1',
    py_modules = ['stock'],
    author = 'Keshab Budhathoky',
    author_email = 'kb4it.professional@hotmail.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = [
        'bs4',
        'click',
        'requests',
        'gdata',
        'pandas',
        'Quandl',
        'pyetrade',
        'jinja2',
        'pandas-finance',
        'Yahoo-ticker-downloader',
        'lxml',
        'MySQL-python',
        'pyexcel-xls',
        'prettytable'
        ],
    entry_points = {
        'console_scripts': [
            'stock_info=stocks:stock_info',
            'my_stock_info=stocks:get_my_stocks_info',
            'yahoo_info=get_yahoo_finance:get_info_yahoo',
            'google_portfolio_info=google_finance:get_google_portfolio_info',
            'vg_portfolio_holder_info=vg_port_holders:get_vg_portfolio_holder_info',
            'vg_ticker_info=vanguard:get_ticker_info',
            'etrade_watchlist_info=etrade_watchlist:etrade_watchlist_info',
        ]
    },
)
