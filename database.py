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

    # @classmethod
    def update_history_cost(self, days_change):
        cost_history = 0
        for index in range(len(self.stocks)):
            data = yf.Ticker(self.stocks[index].ticker)
            self.stocks[index].price_history =\
                get_tick_price_hist(data, days_change)
            self.stocks[index].cost_history =\
                self.stocks[index].price_history * self.stocks[index].quantity
            cost_history += self.stocks[index].cost_history
        self.cost_history = cost_history
        self.change_history = self.cost - self.cost_history
        self.change_history_percent = (self.cost / self.cost_history - 1) * 100
        self.change_history_sign = price_change_emoji(self.change_history_percent)

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


def portfolio_performance_stats(portfolio, market_ticker):
    days_change = "5"
    portfolio.update_cost()
    portfolio.update_history_cost(days_change)
    portfolio_cost = portfolio.cost
    portfolio_prev_cost = portfolio.cost_history
    portfolio_change_percent =\
        round(((portfolio_cost / portfolio_prev_cost - 1) * 100), 1)
    portfolio_change_sign = price_change_emoji(portfolio_change_percent)
    market_data = yf.Ticker(market_ticker)
    market_history = market_data.history()
    market_cost = get_tick_price(market_history)
    market_prev_cost = get_tick_price_hist(market_data, days_change)
    market_change_percent =\
        round(((market_cost / market_prev_cost - 1) * 100), 1)
    market_change_sign = price_change_emoji(market_change_percent)
    portfolio_performance = portfolio_change_percent - market_change_percent
    if portfolio_performance > 0:
        portfolio_performance_word = "overperformed"
    else:
        portfolio_performance_word = "underperformed"
    message = "Market change: " + market_change_sign + " "\
              + str(market_change_percent) + " %\n" \
              + "Portfolio price change: " + portfolio_change_sign + " "\
              + str(portfolio_change_percent) + " %\n" + "You "\
              + portfolio_performance_word + " the market for "\
              + str(portfolio_performance) + " %"
    return message
