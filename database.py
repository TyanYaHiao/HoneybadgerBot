from finance import *
from output import *


class Stock:
    def __init__(self, ticker, quantity, price_average):
        self.ticker = ticker
        self.quantity = quantity
        self.price_average = price_average
        self.cost_average = quantity * price_average

    def __repr__(self):
        return repr((self.ticker, self.quantity, self.price_average))

    def get_price(self):
        data = yf.Ticker(self.ticker)
        history = data.history()
        self.price = get_tick_price(history)
        self.cost = self.quantity * self.price
        self.change = self.cost - self.cost_average
        self.change_percent = (self.price / self.price_average - 1) * 100
        self.change_sign = price_change_emoji(self.change_percent)


class Portfolio:
    # def __init__(self):
    #     self.stocks = [
    #         Stock("AAPL", 1, 128.27),
    #         Stock("AMD", 1, 53.95),
    #         Stock("F", 15, 7.41),
    #         Stock("INTC", 4, 55.79),
    #         Stock("JPM", 1, 99.99),
    #         Stock("T", 6, 33.61),
    #     ]

    # @classmethod
    def update_cost(self):
        cost = 0
        average_cost = 0
        for index in range(len(self.stocks)):
            self.stocks[index].get_price()
            cost += self.stocks[index].cost
            average_cost += self.stocks[index].cost_average
            self.stocks[index].currency = self.currency
            self.stocks[index].currency_sign = self.currency_sign
        self.cost = cost
        self.cost_average = average_cost
        self.change = self.cost - self.cost_average
        self.change_percent = (self.cost / self.cost_average - 1) * 100
        self.change_sign = price_change_emoji(self.change_percent)

    def us_portfolio_init(self):
        self.stocks = [
            Stock("AAPL", 1, 128.27),
            Stock("AMD", 1, 53.95),
            Stock("F", 15, 7.41),
            Stock("INTC", 4, 55.79),
            Stock("JPM", 1, 99.99),
            Stock("T", 6, 33.61),
        ]
        for index in range(len(self.stocks)):
            self.stocks[index].ticker_short = self.stocks[index].ticker
            self.stocks[index].link = "https://finance.yahoo.com/quote/"\
                                      + self.stocks[index].ticker
        self.currency = "USD"
        self.currency_sign = "$"

    def ru_portfolio_init(self):
        self.stocks = [
            Stock("FXIT", 2, 7320.5),
            Stock("FXUS", 3, 4347.33),
            Stock("TATNP", 26, 577.62),
            Stock("YNDX", 2, 2795.0),
            Stock("SBERP", 40, 210.13),
            Stock("FXCN", 2, 3466.0),
            Stock("CHMF", 6, 932.1),
            Stock("AFKS", 200, 19.71),
            Stock("FEES", 30000, 0.21),
            Stock("GAZP", 30, 212.27),
            Stock("FXRB", 3, 1646.0),
            Stock("FXGD", 4, 955.0),
            Stock("FXRL", 1, 2819.0),
            Stock("DSKY", 20, 98.57),
            Stock("SBER", 10, 189.85),
            Stock("TCSG", 1, 1663.6),
            Stock("VTBEM", 2, 811.76),
            Stock("MOEX", 10, 136.6),
            Stock("TGKA", 100000, 0.01),
            Stock("ALRS", 10, 77.86),
            Stock("FXWO", 513, 1.32),
            Stock("OGKB", 1000, 0.58),
            Stock("FXRW", 506, 1.02),
        ]
        for index in range(len(self.stocks)):
            self.stocks[index].ticker_short = self.stocks[index].ticker
            self.stocks[index].ticker += ".ME"
            self.stocks[index].link = "https://finance.yahoo.com/quote/"\
                                      + self.stocks[index].ticker
        self.currency = "RUB"
        self.currency_sign = "₽"
