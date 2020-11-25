import yfinance as yf


def get_tick_price(history):
    return history.tail(1)['Close'].iloc[0]


def get_tick_price_hist(data, days_change):
    days_history = data.history(period=str(days_change + "d"))
    return days_history['Close'][0]


def get_tick_name(data):
    return data.info['shortName']


def get_tick_currency(data):
    currency = data.info['currency']
    if currency == "USD":
        return " $"
    elif currency == "EUR":
        return " €"
    elif currency == "RUB":
        return " ₽"
    return currency

# for ticker in tickers:
#     ticker_yahoo = yf.Ticker(ticker+'.SA')
#     data = ticker_yahoo.history()
#     last_quote = (data.tail(1)['Close'].iloc[0])
#     print(ticker,last_quote)