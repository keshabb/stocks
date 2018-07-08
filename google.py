#!/usr/bin/python

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

url = "https://www.google.com/finance/portfolio?pid=3&output=csv&action=view&pview=sview&ei=XGBxWcivEoexjAHBw6XYDg";
values = {'Email': 'kb4it.professional@gmail.com', 'Passwd' : 'Anaconda420', 'signIn' : 'Sign in', 'PersistentCookie' : 'yes'} # The form data 'name' : 'value'

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
data = urllib.urlencode(values)
response = opener.open(url, data)
print response.content
