# 交易数据收集   
制定好我们自己的量化策略后，我们需要验证我们的策略效果如何，这个时候就需要使用历史交易数据进行回测验证。历史交易数据不容易获取，特别是需要各大交易所的历史数据时，即使付费，获取的数据也不是全量的。   
所以我们可以自己进行数据的收集，为了后续进行交易策略验证时使用。 这里收集 实时/历史 数据并保存为 csv 文件，也可以选择保存数据到其他的数据仓库，如 mysql。 


## 执行收集程序  
- 执行实时 Ticker 数据收集  
修改 getRealTimeTickersData.py 中 "timedelta" 数据，默认收集 30s 的数据
```shell
python getRealTimeTickersData.py
```

- 执行历史 Ticker 数据收集  
修改 getRealTimeTickersData.py 中 "timedelta" 数据，默认收集前一天到当前时刻的数据
```shell
python getHistoryTickersData.py
```

## 参考文档  
python _thread 模块： https://www.runoob.com/python3/python3-multithreading.html  
python 多进程模式:  https://www.liujiangblog.com/course/python/82  
