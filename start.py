import telebot
from secure import get_token
from database import *
from finance import *
from output import *

bot = telebot.TeleBot(get_token())
DB.stocks_init()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Type ticker, get price and change\n"
                                      "Try ticker + .me for moscow exhange\n"
                                      "Use ticker + number to get days change")


@bot.message_handler(commands=['stats'])
def handle_start_help(message):
    header = "*Portfolio price:*\n"
    DB.calc_now_price()
    now_price = str(round(DB.now_price, 2))
    change = str(round((DB.now_price - DB.start_price), 2))
    change_percent = round(((DB.now_price / DB.start_price - 1) * 100), 2)
    change_sign = price_change_emoji(change_percent)
    stocks_info = ""
    for index in range(DB.stocks_number):
        stocks_info += "\n*"
        stocks_info += DB.stocks[index]["ticker"]
        stocks_info += ":* "
        stocks_info += str(round(DB.stocks[index]["now_price"] * DB.stocks[index]["quantity"], 1))
        stocks_info += " $, "
        stocks_info += DB.stocks[index]["change_sign"]
        stocks_info += " "
        stocks_info += str(round(DB.stocks[index]["change"] * DB.stocks[index]["quantity"], 1))
        stocks_info += " $ ("
        stocks_info += str(round(DB.stocks[index]["change_percent"], 2))
        stocks_info += ")"
    bot.send_message(message.chat.id, header + now_price + " $, " + change_sign + " " + change + " $ ("+ str(change_percent) + " %)" + stocks_info, parse_mode="Markdown")
    pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        message_words = str.split(message.text)
        data = yf.Ticker(message_words[0])
        history = data.history()
        if len(message_words) > 1 and message_words[1].isdigit:
            days_change = message_words[1]
        else:
            days_change = "5"
        name = "*" + str(get_tick_name(data)) + ":*"
        price = get_tick_price(history)
        price_str = str(round(get_tick_price(history), 2))
        currency = get_tick_currency(data)
        prev_price = get_tick_price_hist(data, days_change)
        change = str(round((price - prev_price), 2))
        change_percent = round(((price / prev_price - 1) * 100), 1)
        change_sign = price_change_emoji(change_percent)
        bot.send_message(message.chat.id, name + "\nPrice: " + price_str + currency + ", " + change_sign + " " + change + currency + " (" + str(change_percent) + " %) ", parse_mode="Markdown")
    except:
        bot.reply_to(message, "Error")


bot.polling()
