#!/usr/bin/env python

from pyexcel_xls import get_data, save_data
from os import walk
import os
import yaml
import json
import numpy as np
import pandas as pd
import stocks
import click


class Fidelity(object):
    def __init__(self):
        pass

    def get_excel_file_names(self, files_dir):
        files_list = []
        for (dirpath, dirnames, filenames) in walk(files_dir):
            files_list.extend([os.path.join(dirpath, f) for f in filenames])
        return files_list

    def get_info(self, file_name):
        data = get_data(file_name)
        data = yaml.load(json.dumps(data))
        return data
    
def main():
    all_data = pd.DataFrame()
    excel_headers = []
    col_datas = []
    fidelity_client = Fidelity()
    file_names = fidelity_client.get_excel_file_names('fidelity/Data_Services/')
    
    for file_name in file_names:
        print file_name
        df = pd.read_excel(file_name)
        data = fidelity_client.get_info(file_name)
        for index, item in enumerate(data['Sheet1']):
            if index == 0:
                continue
            if not item:
                continue
            else:
                ticker = item[0]
                stocks.get_stock_info(ticker, days=30)
                click.pause(info="Press any key to continue...", err=False)

if __name__ == '__main__':
    main()
