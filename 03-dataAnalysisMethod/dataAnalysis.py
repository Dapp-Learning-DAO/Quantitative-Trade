import pandas as pd

# pd.set_option('display.max_columns', None)  #  print 时，显示所有列数据
pd.set_option('display.max_rows', None)  #  print 时，显示所有行数据

df = pd.read_csv(
    r'chaosData.csv',
    encoding='gbk',
    parse_dates=['candle_begin_time']
)

print("Original Data")
print(df)
print('\n')

# 对数据进行排序
df.sort_values(by=['candle_begin_time'], inplace=True)
print("After data sort")
print(df)
print('\n')

# 对数据进行去重
df = df.drop_duplicates(subset='candle_begin_time')
print("After drop duplicate")
print(df)
print('\n')

# 重置行索引
df = df.reset_index(drop=True)
print("After reset index")
print(df)
print('\n')



# 重新采样，变 1 分钟 K 线数据为 5 分钟
rule_type = '5T'
df_5T = df.resample(rule=rule_type, on='candle_begin_time').agg(
    {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
    }
)
df_5T = df_5T[['open', 'high', 'low', 'close', 'volume']]
print("After resample")
print(df_5T)
print('\n')


# 重新采样，变 1 分钟 K 线数据为 5 分钟
rule_type = '5T'
df_5T = df.resample(rule=rule_type, on='candle_begin_time').agg(
    {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
    }
)
df_5T = df_5T[['open', 'high', 'low', 'close', 'volume']]
print("After resample")
print(df_5T)
print('\n')


# 滚动计算平均值
df['mean'] = df['close'].rolling(3).mean()
print("After calculate mean")
print(df)
print('\n')

# 移除列数据
# 每一行 median 数据向下移动
df['mean_shift_down'] = df['mean'].shift()
print("After column mean shift down")
print(df)
print('\n')

# 每一行 median 数据向上移动
df['mean_shift_up'] = df['mean'].shift(-1)
print("After column mean shift up")
print(df)
print('\n')