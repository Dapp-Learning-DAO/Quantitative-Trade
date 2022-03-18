
import pandas as pd
import ccxt
import time
import datetime
import utils
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 数据收集持续的时间, 这里单位是 秒
timedelta = 300
# 需要获取的交易对
swap_list = ['BTC-USD-SWAP','BTC-USDT-SWAP']
futures_list = ['BTC-USD-220325','BTC-USDT-220325']

# 获取结束时间
start_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
end_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + datetime.timedelta(seconds=timedelta)

exchange = ccxt.okex5()

# 定义永续合约数据，交割合约数据保存变量
swap_coin_based_data = []
swap_u_based_data = []
future_coin_based_data = []
future_u_based_data = []
# 获取永续合约, 交易合约数据
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

    # 循环遍历 swap_list, 获取永续合约数据
    for future in futures_list:
        params = {
            'instId': future,  ## 永续合约
        }
        temp_future_data = pd.DataFrame(exchange.publicGetMarketTicker(params)['data'])
        if future.startswith('BTC-USDT'):
            future_u_based_data.append(temp_swap_data)
        else:
            future_coin_based_data.append(temp_swap_data)


    # 判断当前时间是否已经超过 end_time
    current_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if current_time > end_time:
        break


# 保存 swap 和 future 数据
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

for future in futures_list:
     # 创建数据文件， 同时返回数据文件路径
    file_path = utils.check_folder(exchange, future, '1', start_time, path, 'future')
    if future.startswith('BTC-USDT'):
        future_u_based_data = pd.concat(future_u_based_data, ignore_index=True)
        future_u_based_data.to_csv(file_path, index=False)
    else:
        future_coin_based_data = pd.concat(future_coin_based_data, ignore_index=True)
        future_coin_based_data.to_csv(file_path, index=False)
