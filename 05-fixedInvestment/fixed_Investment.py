from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import ccxt
import json
from env import OKEX_ACCOUNT
from OKEX_BROKER import OKEXBroker


# =====创建ccxt交易所
OKEX_CONFIG = {
    'apiKey': OKEX_ACCOUNT['apiKey'],
    'secret': OKEX_ACCOUNT['secret'],
    'password': OKEX_ACCOUNT['password'],
    #'timeout': exchange_timeout,
    'rateLimit': 10,
    'enableRateLimit': False}
exchange = ccxt.okex5(OKEX_CONFIG)

# 交易的 symbol 
symbol = 'CRV-USDT'

# 投入资金
fixed_invest_money = 4

# 最小买入数量
min_amount = 1

# 定投时间,
fixedDay = 4  # 默认为每周 4 进行定投
 
# OKEX 经纪人
okex_broker = OKEXBroker(exchange, symbol, fixed_invest_money,min_amount, fixedDay)

scheduler = BlockingScheduler()   # 主线程里面执行.
scheduler.add_job(okex_broker.fixed_invest_trading, trigger='cron', minute='*/1')  # 每小时运行一次.
scheduler.add_job(okex_broker.check_order_status, trigger='cron', minute='*/1')  # 每五分钟检查下仓位.
# scheduler.add_job(okex_broker.send_notify_msg, trigger='cron', hour='*/8')  # 每八个小时通知一次。
# 启动定时任务
scheduler.start()