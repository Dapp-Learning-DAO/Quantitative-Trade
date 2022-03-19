
import pandas as pd
import ccxt
import time
import datetime
import utils
import os
pd.set_option('display.max_columns', None)  # print 时，显示所有列数据
pd.set_option('display.max_rows', None)  # print 时，显示所有行数据


# 数据收集持续的时间, 这里单位是 秒
timedelta = 30
# 需要获取的交易对
swap_list = ['BTC-USD-SWAP','BTC-USDT-SWAP']

# 获取结束时间
start_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
end_time = start_time + datetime.timedelta(seconds=timedelta)

exchange = ccxt.okex5()

# 定义永续合约数据变量
swap_coin_based_data = []
swap_u_based_data = []

# 获取永续合约数据
while True:
    # 循环遍历 swap_list, 获取永续合约数据
    for swap in swap_list:
        params = {
            'instId': swap,  ## 永续合约
        }
        temp_swap_data = pd.DataFrame(exchange.publicGetMarketTicker(params)['data'])
        if swap.startswith('BTC-USDT'):
            swap_u_based_data.append(temp_swap_data)
        else:
            swap_coin_based_data.append(temp_swap_data)


    # 判断当前时间是否已经超过 end_time
    current_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if current_time > end_time:
        break


# 保存 swap 数据
# 获取当前路径
path = os.getcwd()
# 保存数据
for swap in swap_list:
    # 创建数据文件， 同时返回数据文件路径
    file_path = utils.check_folder(exchange, swap, '1', start_time, path, 'swap')
    if swap.startswith('BTC-USDT'):
        swap_u_based_data = pd.concat(swap_u_based_data, ignore_index=True)
        swap_u_based_data.to_csv(file_path, index=False)
    else:
        swap_coin_based_data = pd.concat(swap_coin_based_data, ignore_index=True)
        swap_coin_based_data.to_csv(file_path, index=False)
