from finance import *
from output import *

class DB:
    stocks = {}

    stocks_number = 0
    start_price = 0
    now_price = 0

    @classmethod
    def calc_now_price(cls):
        price = 0
        for index in range(cls.stocks_number):
            data = yf.Ticker(cls.stocks[index]["ticker"])
            history = data.history()
            cls.stocks[index]["now_price"] = get_tick_price(history)
            cls.stocks[index]["change"] = cls.stocks[index]["now_price"] - cls.stocks[index]["price"]
            cls.stocks[index]["change_percent"] = (cls.stocks[index]["now_price"] / cls.stocks[index]["price"] - 1) * 100
            cls.stocks[index]["change_sign"] = price_change_emoji(cls.stocks[index]["change_percent"])
            price += cls.stocks[index]["quantity"] * get_tick_price(history)
        cls.now_price = price

    @classmethod
    def stocks_init(cls):
        #               ticker, q-ty,   price
        cls.stock_init("AAPL",  1,      128.27)
        cls.stock_init("AMD",   1,      53.95)
        cls.stock_init("F",     15,     7.41)
        cls.stock_init("INTC",  4,      55.79)
        cls.stock_init("JPM",   1,      99.99)
        cls.stock_init("T",     6,      33.61)

    @classmethod
    def stock_init(cls, ticker, quantity, average_price):
        stock = {
            "ticker": ticker,
            "quantity": quantity,
            "price": average_price
        }
        cls.start_price += stock["quantity"] * stock["price"]
        cls.stocks[cls.stocks_number] = stock
        cls.stocks_number += 1
