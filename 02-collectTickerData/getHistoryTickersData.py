
import pandas as pd
import ccxt
import time
import os
import datetime
import utils
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

exchange = ccxt.binance()
error_list = []
path = os.getcwd()

# 数据类型为 spot , 现货
trade_type = 'spot'
# 往前推进的时间周期，单位为天
timedelta = 30
# 获取一年前的时间 
start_time = str(pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) - datetime.timedelta(days=timedelta))

# 需要获取的交易对
symbol_list = ['ETH/USDT']

# 遍历交易对
for symbol in symbol_list:

    # 遍历时间周期
    for time_interval in ['5m', '15m']:
        print(exchange.id, symbol, time_interval)

        # 抓取数据并且保存
        try:
            utils.save_data(exchange, symbol, time_interval, start_time, path, trade_type, timedelta)
        except Exception as e:
            print(e)
            error_list.append('_'.join([exchange.id, symbol, time_interval]))

# 打印错误信息
print(error_list)
