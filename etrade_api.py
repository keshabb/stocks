import os
import pyetrade
import click
import config

OAUTH_CONSUMER_KEY = config.OAUTH_CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET

class Account(object):
    def __init__(self):
        self.oauth = pyetrade.ETradeOAuth(OAUTH_CONSUMER_KEY, CONSUMER_SECRET)
        token_verification_url = self.oauth.get_request_token()
        click.echo(token_verification_url)
        verifier_code = click.prompt("Please enter a verfier code", type=str)
        self.tokens = self.oauth.get_access_token(verifier_code)
    
    def _get_ETradeAccessManager(self):
        self.access_mgr = pyetrade.ETradeAccessManager(
            self.oauth.consumer_key,
            self.oauth.consumer_secret, 
            self.tokens['oauth_token'],
            self.tokens['oauth_token_secret']
        )
        return self.access_mgr

    @property
    def renew_token(self):
        tok = self._get_ETradeAccessManager()
        tok.renew_access_token()

    @property
    def revoke_token(self):
        tok = self._get_ETradeAccessManager()
        tok.revoke_access_token()

class Equity(object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.oauth = pyetrade.ETradeOAuth(OAUTH_CONSUMER_KEY, CONSUMER_SECRET)
        token_verification_url = self.oauth.get_request_token()
        click.echo(token_verification_url)
        verifier_code = click.prompt("Please enter a verfier code", type=str)
        #Follow url and get verification code
        self.tokens = self.oauth.get_access_token(verifier_code)
    
#    def _get_ETradeAccessManager(self):
#        self.access_mgr = pyetrade.ETradeAccessManager(
#            self.oauth.consumer_key,
#            self.oauth.consumer_secret, 
#            self.tokens['oauth_token'],
#            self.tokens['oauth_token_secret']
#        )
#        return self.access_mgr
#
#    @property
#    def renew_token(self):
#        tok = self._get_ETradeAccessManager()
#        tok.renew_access_token()
#
#    @property
#    def revoke_token(self):
#        tok = self._get_ETradeAccessManager()
#        tok.revoke_access_token()
#

    def _get_ETradeMarket(self):
        self.market = pyetrade.ETradeMarket(
            self.oauth.consumer_key,
            self.oauth.consumer_secret,
            self.tokens['oauth_token'],
            self.tokens['oauth_token_secret']
        )
        return self.market

    @property
    def quote_all(self):
        quote = self._get_ETradeMarket()
        resp_data =  quote.get_quote(0,'json', 'ALL', self.ticker)
        quote_all = resp_data['quoteResponse']['quoteData']['all']
        print quote_all
        return quote_all
    
    @property
    def eps(self):
        return self.quote_all['eps']
