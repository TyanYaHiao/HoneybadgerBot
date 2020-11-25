import yfinance as yf


def get_tick_price(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['open']


def get_tick_price_hist(ticker, days_ago):
    tick = yf.Ticker(ticker)
    return tick.history(period=str(days_ago + "d"))['Close'][0]


def get_tick_name(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['shortName']


def get_tick_currency(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['currency']

