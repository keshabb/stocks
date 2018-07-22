import os
import datetime
import pyetrade
import click
import config
import MySQLdb

OAUTH_CONSUMER_KEY = config.OAUTH_CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
DB_USERNAME = config.DB_USERNAME
DB_PASSWD = config.DB_PASSWD
epoch_time = datetime.datetime.now().strftime('%s')
now = datetime.datetime.now()


class Account(object):
    def __init__(self):
        #token_data = self.get_token()
        #if token_data:
        #    self.tokens = dict()
        #    self.oauth = pyetrade.ETradeOAuth(OAUTH_CONSUMER_KEY, CONSUMER_SECRET)
        #    self.tokens['oauth_token'] = token_data[0]
        #    self.tokens['oauth_token_secret'] = token_data[1]
        #    self.token_creation_time = token_data[2]
        #    print self.token_creation_time
        #else:
        #   self.oauth = pyetrade.ETradeOAuth(OAUTH_CONSUMER_KEY, CONSUMER_SECRET)
        #   token_verification_url = self.oauth.get_request_token()
        #   click.echo(token_verification_url)
        #   self.verifier_code = click.prompt("Please enter a verfier code", type=str)
        #   self.tokens = self.get_access_token()
        self.tokens = dict()
        self.oauth = pyetrade.ETradeOAuth(OAUTH_CONSUMER_KEY, CONSUMER_SECRET)
        token_data = self.get_token()
        if not token_data:
            token_verification_url = self.oauth.get_request_token()
            click.echo(token_verification_url)
            self.verifier_code = click.prompt("Please enter a verfier code", type=str)
            self.tokens = self.get_access_token()
            try:
                self.add_token(self.tokens['oauth_token'],
                               self.tokens['oauth_token_secret'])
            except Exception:
                raise Exception("Failed to add tokens")
        else:
            token_creation = token_data[2]
            diff_creation = now - token_creation
            token_access_time = token_data[3]
            diff_access_min = (now - token_access_time).total_seconds() / 60.0
            if  now.strftime("%Y-%m-%d") != token_creation.strftime("%Y-%m-%d"):
                token_verification_url = self.oauth.get_request_token()
                click.echo(token_verification_url)
                self.verifier_code = click.prompt("Please enter a verfier code", type=str)
                self.tokens = self.get_access_token()
                try:
                  self.update_token(self.tokens['oauth_token'], self.tokens['oauth_token_secret'])
                except Exception:
                    print("Failed to add tokens")
            elif now.strftime("%Y-%m-%d") == token_creation.strftime("%Y-%m-%d") and int(diff_access_min) > 120:
                self.tokens['oauth_token'] = token_data[0]
                self.tokens['oauth_token_secret'] = token_data[1]
                self.renew_token
                self.update_token(self.tokens['oauth_token'], self.tokens['oauth_token_secret'], last_access_time=now)
            else:
                self.tokens['oauth_token'] = token_data[0]
                self.tokens['oauth_token_secret'] = token_data[1]

    
    def get_access_token(self):
        return self.oauth.get_access_token(self.verifier_code)

    def connect_db(self):
        self.db = MySQLdb.connect(host="localhost",  # your host
                             user=DB_USERNAME,       # username
                             passwd=DB_PASSWD, # password
                             db="etrade_auth")   # name of the database
        self.cur = self.db.cursor()
        return self.db, self.cur

    def get_token(self):
        token_data = []
        self.connect_db()
        self.cur.execute("SELECT * FROM etrade_auth")
        row_count = self.cur.rowcount
        if row_count == 0:
            return token_data
        else:
            for row in self.cur.fetchall():
                token_data.extend((row[0], row[1], row[2], row[3]))
            return token_data

    def add_token(self, oauth_token, oauth_token_secret):
        self.connect_db()
        sql = ("INSERT INTO etrade_auth values ('{}', '{}', now(), now())".
                format(oauth_token, oauth_token_secret))
        self.cur.execute(sql)
        self.db.commit()

    def update_token(self, oauth_token, oauth_token_secret,
                     last_access_time=None):
        self.connect_db()
        if last_access_time is not None:
            sql = ("UPDATE etrade_auth set accessed_at=now()".
                    format(oauth_token, oauth_token_secret))
        else:
            sql = ("UPDATE etrade_auth set oauth_token='{}',"
                   "oauth_token_secret='{}',created_at=now(), accessed_at=now()".
                    format(oauth_token, oauth_token_secret))
        self.cur.execute(sql)
        self.db.commit()

    def _get_ETradeAccessManager(self):
        self.access_mgr = pyetrade.ETradeAccessManager(self.oauth.consumer_key,
                                                       self.oauth.consumer_secret,
                                                       self.tokens['oauth_token'],
                                                       self.tokens['oauth_token_secret'])
        return self.access_mgr

    @property
    def renew_token(self):
        tok = self._get_ETradeAccessManager()
        tok.renew_access_token()

    @property
    def revoke_token(self):
        tok = self._get_ETradeAccessManager()
        tok.revoke_access_token()

    def _get_EtradeAccount(self):
        self.acct = pyetrade.ETradeAccounts(self.oauth.consumer_key,
                                                 self.oauth.consumer_secret,
                                                 self.tokens['oauth_token'],
                                                 self.tokens['oauth_token_secret'])
        return self.acct

    @property
    def list_alerts(self):
        """ Returns alerts for an account """
        alert = self._get_EtradeAccount()
        return alert.list_alerts(0, 'json')


class Equity(object):
    def __init__(self, account, ticker):
        self.ticker = ticker
        self.oauth = account.oauth
        self.tokens = account.tokens
    
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
        self.market = pyetrade.ETradeMarket(self.oauth.consumer_key,
                                            self.oauth.consumer_secret,
                                            self.tokens['oauth_token'],
                                            #self.tokens.oauth_token,
                                            self.tokens['oauth_token_secret']
                                            #self.tokens.oauth_token_secret]
                                            )
        return self.market

    @property
    def quote_all(self):
        quote = self._get_ETradeMarket()
        resp_data =  quote.get_quote(0,'json', 'ALL', self.ticker)
        if 'Invalid Symbol' in resp_data['quoteResponse']['quoteData'].itervalues():
            return None
        quote_all = resp_data['quoteResponse']['quoteData']['all']
        return quote_all
    
    @property
    def eps(self):
        return self.quote_all['eps']

    @property
    def highprice(self):
        return self.quote_all['high']
    
    @property
    def openprice(self):
        return self.quote_all['open']
    
    @property
    def lowprice(self):
        return self.quote_all['low']
    
    @property
    def totalVol(self):
        return self.quote_all['totalVolume']
    
    @property
    def dividend(self):
        return self.quote_all['dividend']
    
    @property
    def annualDividend(self):
        return self.quote_all['annualDividend']
    
    @property
    def todayClose(self):
        return self.quote_all['todayClose']
    
    @property
    def numTrades(self):
        return self.quote_all['numTrades']
    
    @property
    def estEarnings(self):
        return self.quote_all['estEarnings']
    
    @property
    def companyName(self):
        return self.quote_all['companyName']
    
    @property
    def ask(self):
        return self.quote_all['ask']
    
    @property
    def askSize(self):
        return self.quote_all['askSize']
    
    @property
    def askTime(self):
        return self.quote_all['askTime']
    
    @property
    def highAsk(self):
        return self.quote_all['highAsk']

    @property
    def lowAsk(self):
        return self.quote_all['lowAsk']

    @property
    def numTrades(self):
        return self.quote_all['numTrades']

    @property
    def beta(self):
        return self.quote_all['beta']
