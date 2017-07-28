from setuptools import setup, find_packages
setup(
    name = 'stock',
    description = 'Python script to get stock info',
    version = '1.0',
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
        ],
    entry_points = {
        'console_scripts': [
            'stock_info=stocks:stock_info',
            'my_stock_info=stocks:get_my_stocks_info',
            'get_info_yahoo=yahoo_finance:get_info_yahoo',
            'google_portfolio_info=google_finance:get_google_portfolio_info',
        ]
    },
)
