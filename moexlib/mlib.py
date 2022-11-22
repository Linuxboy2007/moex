# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:55:05 2022

@author: Юрий
"""
from os.path import join
import pathlib
import pandas as pd
import numpy as np
from pandas_datareader.data import DataReader

def dmei(moex_dest, start_date, end_date):
    '''
Downloading Moscow Exchange indices
moex_dest - catalog for Moscow Exchange indices
start_date - period start date
end_date - period end date
    '''
    pathlib.Path(moex_dest).mkdir(parents=True, exist_ok=True)
    tickers=["IMOEX","MOEX10"]
    arguments = ['SECID','SHORTNAME','OPEN', 'CLOSE', 
                 'HIGH', 'LOW','MEAN','RPC']
    for ticker in tickers:
        data = DataReader(
            ticker,
            'moex',
            start=start_date,
            end=end_date,
        )
    data = data[['SECID','SHORTNAME','OPEN', 'CLOSE', 'HIGH', 'LOW']]
    data['MEAN'] = np.array(data.iloc[:,2:5].mean(1))
    data['RPC'] = 0
    data.iloc[1:,7] = [ (data.iloc[i,6]-data.iloc[i-1,6])/data.iloc[i-1,6] 
                for i in range(1,data.shape[0]) ]
    dest = join(moex_dest, ticker + '.csv')
    print("Writing %s -> %s" % (ticker, moex_dest))
    data.to_csv(dest, index_label='day', 
                columns = arguments, encoding='utf-8-sig') 

def qoutes_download(instrument_tickers, data_dest, start_date, end_date):
    '''
    Dowload and processing of instrument data
    '''
    pathlib.Path(data_dest).mkdir(parents=True, exist_ok=True)
    arguments = ['SECID','SHORTNAME','OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME']

    for instrument_ticker in instrument_tickers:
        data = DataReader(instrument_ticker,
            'moex',
            start=start_date,
            end= end_date,
        )
        dest = join(data_dest, instrument_ticker + '.csv')
        print("Writing %s -> %s" % (instrument_ticker, dest))
        data.to_csv(dest, index_label='day', columns = arguments, encoding='utf-8-sig')
    

def qoutes_descr(data, ticker, path, data_all):
    '''
    путь для сохранения фалов
    '''
    dest = join(path, ticker +'_processed' + '.csv')
    dest1 = join(path,'descr_all' + '.csv')
    '''
    Средняя цена за день (MEAN)и 
    относительное изменением цены дня по отношению к предыдущему дню (RPC)
    '''
    data['MEAN'] = np.array(data.iloc[:,3:6].mean(1))
    data['RPC'] = 0
    data.iloc[1:,9] = [(data.iloc[i,8]-data.iloc[i-1,8])/data.iloc[i-1,8] 
                for i in range(1,data.shape[0]) ]
    print("Writing %s -> %s" % (ticker, dest))
    data.to_csv(dest, index = False, encoding='utf-8-sig')
    '''
    Среднее значение (Mean), с.к.о. (Std), несимметричность (Skew),
    коэффициент эксцесса (островершинность) (kurtosis),
    относительное изменение за весь период (Rpc_all).   
    '''
    df1 = pd.DataFrame(data={'Secid':[data.iloc[0,1]],
         'Mean': [data['MEAN'].mean()], 
         'Std':[data['MEAN'].std()],
         'Skew': [data['MEAN'].skew()], 
         'kurtosis': [data['MEAN'].kurtosis()],
         'Rpc_all': [(data.iloc[-1,8]-data.iloc[0,8])/data.iloc[0,8]]})

    print("Writing descr%s -> %s" % (ticker, dest))
    if pathlib.Path(dest1).is_file():
        df1.to_csv(dest1, mode='a', header=False, index = False,
                   encoding='utf-8-sig')
    else:
        df1.to_csv(dest1, index = False, encoding='utf-8-sig')
    data_all[data['SHORTNAME'][0]]=data.iloc[:,9]
    return data_all



    
