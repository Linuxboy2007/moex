# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 12:03:57 2022

@author: Юрий
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) 

from os.path import join, isdir
import pathlib
import pandas as pd
# import numpy as np
# from pandas_datareader.data import DataReader
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator
from pandas.core.common import SettingWithCopyWarning
import moexlib.mlib as moexl

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
# Период времени
start_date = '2022-08-01'
end_date = '2022-08-31'

path = r'c:\stock data' # корневой каталог для сохрания информации
moex_dest = join(path, start_date+ "_"+ end_date,'moexdata') # каталог для индексов МосБиржи
data_dest= join(path, start_date+ "_"+ end_date,'data') # каталог для хранения информации о инструментах
processed_dest = join(path, start_date+ "_"+ end_date,'processed') # каталог для хранения обработанных данных инструментов
ticks_path = join(path, 'SECID' + '.txt') # путь для файла со списком инструментов

moexl.dmei(moex_dest, start_date, end_date)

'''  Список secid инструментов '''
instrument_tickers=["ABRD","ACKO","AFKS","AFLT","AGRO","AKRN"] 
moexl.qoutes_download(instrument_tickers, data_dest, start_date, end_date)
# pathlib.Path(data_dest).mkdir(parents=True, exist_ok=True)
# arguments = ['SECID','SHORTNAME','OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME']

# for instrument_ticker in instrument_tickers:
#     data = DataReader(instrument_ticker,
#             'moex',
#             start=start_date,
#             end= end_date,
#         )
#     dest = join(data_dest, instrument_ticker + '.csv')
#     print("Writing %s -> %s" % (instrument_ticker, dest))
#     data.to_csv(dest, index_label='day',
#                 columns = arguments, encoding='utf-8-sig')
    
pathlib.Path(processed_dest).mkdir(parents=True, exist_ok=True)
'''
Для тестирования в переменную instrument_tickers вносим secid инструментов.
Для анализа большего числа инструментов, secid хранятся в файле secid.txt.
Пример получения secid
with open(ticks_path, "r") as instrument_tickers:
   instrument_tickers = [line.rstrip() for line in instrument_tickers]
'''
# instrument_tickers=["ABRD","ACKO","AFKS","AFLT","AGRO","AKRN"]
dft = pd.DataFrame()

for instrument_ticker in instrument_tickers:
    df = pd.read_csv (join(data_dest, instrument_ticker + '.csv'),sep=',')
    if df.isnull().values.any():
        print("Empty period")
    else:
        dft =  moexl.qoutes_descr(df, instrument_ticker, processed_dest, dft)
dest_all = join(processed_dest,'rpc_all' + '.csv')
dest_corr = join(processed_dest,'correlation' + '.csv')
dft['day'] = df['day']
dft.set_index("day", inplace=True)
dft.to_csv(dest_all, encoding='utf-8-sig')
dft.corr().to_csv(dest_corr, encoding='utf-8-sig')



