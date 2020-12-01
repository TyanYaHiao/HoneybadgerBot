import telebot
from secure.secure import get_token
from database import *
from finance import *
from output import *
from pycbrf import *

bot = telebot.TeleBot(get_token())
us_portfolio = Portfolio()
ru_portfolio = Portfolio()
us_portfolio.us_portfolio_init()
ru_portfolio.ru_portfolio_init()


@bot.message_handler(commands=['start'])
def explanation_list(message):
    bot.send_message(message.chat.id, "Type ticker to get price and change\n"
                                      "Try ticker + .me for moscow exhange price\n"
                                      "Use ticker + number to get price change over the last X days")


@bot.message_handler(commands=['rates'])
def portfolio_stats(message):
    rates = ExchangeRates()
    usd_rate = rates["USD"].rate
    eur_rate = rates["EUR"].rate
    usd_message = "*USD rate:* " + str(round(usd_rate, 2))
    eur_message = "\n*EUR rate:* " + str(round(eur_rate, 2))
    bot.send_message(message.chat.id, usd_message + eur_message,
                     parse_mode="Markdown")


@bot.message_handler(commands=['performance'])
def portfolio_stats(message):
    us_message = "*US portfolio analytics:*\n" + portfolio_performance_stats(us_portfolio, "SPY")
    ru_message = "*RU portfolio analytics:*\n" + portfolio_performance_stats(ru_portfolio, "ERUS")
    bot.send_message(message.chat.id, us_message + "\n\n" + ru_message,
                     parse_mode="Markdown")


@bot.message_handler(commands=['stats'])
def portfolio_stats(message):
    header = "*Portfolio:*\n"
    us_portfolio.update_cost()
    cost_us = str(round(us_portfolio.cost, 2))
    change_us = str(round((us_portfolio.change), 2))
    change_percent_us = round(us_portfolio.change_percent, 1)
    change_sign_us = us_portfolio.change_sign
    sign_us = us_portfolio.currency_sign
    ru_portfolio.update_cost()
    cost_ru = str(round(ru_portfolio.cost, 0))
    change_ru = str(round((ru_portfolio.change), 0))
    change_percent_ru = round(ru_portfolio.change_percent, 1)
    change_sign_ru = ru_portfolio.change_sign
    sign_ru = ru_portfolio.currency_sign
    stocks_info = ""
    sorted_portfolio = sorted(us_portfolio.stocks + ru_portfolio.stocks,
                              key=lambda portfolio: portfolio.change_percent,
                              reverse=True)
    for index in range(len(sorted_portfolio)):
        stocks_info += ticker_output(sorted_portfolio[index])
    bot.send_message(message.chat.id, header + "*US:* " + cost_us + " " + sign_us + ", "
                     + change_sign_us + " " + change_us + " " + sign_us + " ("
                     + str(change_percent_us) + " %)\n"
                     + "*RU:* " + cost_ru + " " + sign_ru + ", "
                     + change_sign_ru + " " + change_ru + " " + sign_ru + " ("
                     + str(change_percent_ru) + " %)"
                     + stocks_info, parse_mode="Markdown")
    pass


@bot.message_handler(func=lambda message: True)
def ticker_info(message):
    try:
        message_words = str.split(message.text)
        data = yf.Ticker(message_words[0])
        if len(message_words) > 1 and message_words[1].isdigit:
            days_change = message_words[1]
        else:
            days_change = "5"
        history = data.history()
        name = "*" + str(get_tick_name(data)) + ":*"
        price = get_tick_price(history)
        price_str = str(round(get_tick_price(history), 2))
        currency = get_tick_currency(data)
        prev_price = get_tick_price_hist(data, days_change)
        change = str(round((price - prev_price), 2))
        change_percent = round(((price / prev_price - 1) * 100), 1)
        change_sign = price_change_emoji(change_percent)
        bot.send_message(message.chat.id, name + "\nPrice: "
                         + price_str + currency + ", " + change_sign + " "
                         + change + currency
                         + " (" + str(change_percent) + " %) ",
                         parse_mode="Markdown")
    except:
        bot.reply_to(message, "Error")


bot.polling()
