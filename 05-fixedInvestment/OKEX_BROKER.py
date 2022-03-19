from datetime import datetime
import ccxt
from ccxt import Exchange
import time

class OKEXBroker(object):
    def __init__(self, exchange: Exchange, symbol: str, fixed_invest_money: float, min_amount: float, fixedDay: int):
        super(OKEXBroker, self).__init__()
        self.exchange = exchange
        self.symbol = symbol
        self.fixed_invest_money = fixed_invest_money
        self.order_id = None  # 记录最近一次下单的订单ID.
        self.bid_price = 0
        self.ask_price = 0
        self.min_amount = min_amount
        self.orderChecked = False
        self.fixedDay = fixedDay
        

    def fixed_invest_trading(self, fixedDay):
        now = datetime.now()
        weekday = now.isoweekday()
        if weekday == self.fixedDay and not self.order_id:  # 每周四周五的时候定投.
            for i in range(5):
                try:
                    self.get_ask_bid_price()
                    amount = self.fixed_invest_money/self.ask_price
                    min_amount = self.min_amount
                    amount = amount // min_amount * min_amount  # 取整数.
                    print(f"symbol: {self.symbol}, amount:{amount} ask_price:{self.ask_price}")
                    order = self.exchange.create_limit_buy_order(self.symbol, amount, self.ask_price)
                    print(order)
                    if order:
                        self.order_id = order['info']['ordId']
                        self.orderChecked = False
                        break
                    else:
                        continue
                except Exception as error:
                    print(f"下单发生错误：{error}")
                    time.sleep(10)  # 休息10秒钟


    def check_order_status(self):
        """
        定时检查仓位信息等,检查当前的订单有没有成交等.
        如果order 没有成交的情况下，重新撤单. 然后在下单.
        :return:
        """
        now = datetime.now()
        weekday = now.isoweekday()
        if self.order_id and not self.orderChecked:
            order = self.exchange.fetch_order(self.order_id, self.symbol)
            if order['info']['state'] == 'live' or order['info']['state'] == 'partially_filled': # 部分成交或没有成交时，取消订单
                try:
                    self.exchange.cancel_order(self.order_id, self.symbol)
                    order_id = None
                except Exception as error:
                    print(f"取消订单发生错误：{error}")
            else:
                self.orderChecked = True
        
        if weekday != self.fixedDay and self.order_id:
            self.order_id = None

    def get_ask_bid_price(self):
        ticker = self.exchange.fetch_ticker(self.symbol)
        if ticker:
            self.bid_price = ticker['bid']
            self.ask_price = ticker['ask']
        print(f"bid_price: {self.bid_price}, ask_price:{self.ask_price}")

    def send_notify_msg(self):
        """
        发送通知或者提醒功能.
        :return:
        """