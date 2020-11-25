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
    delta = round(((DB.now_price / DB.start_price - 1) * 100), 2)
    change_sign = price_change_emoji(delta)
    bot.send_message(message.chat.id, header + now_price + " USD, " + str(delta) + "% " + change_sign, parse_mode="Markdown")

    pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        message_words = str.split(message.text)
        tick = yf.Ticker(message_words[0])
        name = "*" + str(tick.info['shortName']) + "*"
        price = str(get_tick_price(message_words[0]))
        currency = str(tick.info['currency'])
        if len(message_words) > 1 and message_words[1].isdigit:
            history = tick.history(period=str(message_words[1] + "d"))
            change = round(((tick.info['open'] / history['Close'][0] - 1) * 100), 1)
        else:
            history = tick.history(period="20d")
            change = round(((tick.info['open'] / history['Close'][0] - 1) * 100), 1)
        change_sign = price_change_emoji(change)
        bot.send_message(message.chat.id, name + "\nPrice: " + price + " " + currency + ", " + str(change) + "% " + change_sign, parse_mode="Markdown")
    except:
        bot.reply_to(message, "Error")


bot.polling()
