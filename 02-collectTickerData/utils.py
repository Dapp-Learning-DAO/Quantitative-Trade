
import os
import datetime
import pandas as pd
import time
pd.set_option('expand_frame_repr', False) 

"""
检查文件夹
:param exchange: 目标交易所
:param symbol: 目标交易对，如 BTC/USD
:param time_interval: K线的时间周期，如 5m, 10m
:param path: 文件保存根目录
:param trade_type: 交易类型，如 spot ( 现货 ), margin ( 杠杆 )
"""
def check_folder(exchange, symbol, time_interval, start_time, path, trade_type):
    # 创建交易所文件夹
    path = os.path.join(path, exchange.id)
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建交易类型文件夹
    path = os.path.join(path, trade_type)
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建日期文件夹
    path = os.path.join(path, str(pd.to_datetime(start_time).date()))
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 拼接文件目录
    file_name = '_'.join([symbol.replace('/', '-'), time_interval]) + '.csv'
    path = os.path.join(path, file_name)

    # 返回数据文件路径
    return path


"""
将某个交易所在指定日期指定交易对的K线数据，保存到指定文件夹
:param exchange: 交易所, 如 币安, 火币, okey
:param symbol: 指定交易对，例如'BTC/USDT'
:param time_interval: K线的时间周期，如 '5m'
:param start_time: 指定日期，格式为'2020-03-16 00:00:00'
:param path: 文件保存根目录, 如 '/usr/location/'
:param timedelta: 抓取的数据时长，以天为单位，默认为 1
:return:
"""
def feth_and_sort_data(exchange,symbol,time_interval,start_time,timedelta):
    df_list = []
    start_time_since = exchange.parse8601(start_time)
    end_time = pd.to_datetime(start_time) + datetime.timedelta(days=timedelta) #默认获取 1 天的交易数据
    
    while True:
        # 获取数据
        df = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, since=start_time_since)
        # 整理数据
        df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
        # 合并数据
        df_list.append(df)
        # 新的since
        t = pd.to_datetime(df.iloc[-1][0], unit='ms')
        start_time_since = exchange.parse8601(str(t))
        # 判断是否挑出循环
        if t >= end_time or df.shape[0] <= 1:
            break
        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(1)
    
    # ===合并整理数据
    df = pd.concat(df_list, ignore_index=True)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                       3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')  # 整理时间
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序

    # 去重、排序
    df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
    df.sort_values('candle_begin_time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

"""
将某个交易所在指定日期指定交易对的K线数据，保存到指定文件夹
:param exchange: 交易所, 如 币安, 火币, okey
:param symbol: 指定交易对，例如'BTC/USDT'
:param time_interval: K线的时间周期，如 '5m'
:param start_time: 指定日期，格式为'2020-03-16 00:00:00'
:param path: 文件保存根目录, 如 '/usr/location/'
:param timedelta: 抓取的数据时长，以天为单位，默认为 1
:return:
"""
def save_data(exchange, symbol, time_interval, start_time, path,trade_type,timedelta=1):
    # ===开始抓取数据，并返回整理后的数据
    df = feth_and_sort_data(exchange, symbol, time_interval, start_time, timedelta)

    # 创建数据文件， 同时返回数据文件路径
    file_path = check_folder(exchange, symbol, time_interval, start_time, path,trade_type)

    # 保存数据
    df.to_csv(file_path, index=False)