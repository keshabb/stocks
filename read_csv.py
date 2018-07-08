#!/usr/bin/env python

import requests


with open('ticker_list.csv', 'r') as f:
    for line in f:
        print line.split(',')[0]
