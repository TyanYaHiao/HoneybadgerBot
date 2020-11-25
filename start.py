import telebot
import emoji
from secure import get_token
from database import *
from finance import *

bot = telebot.TeleBot(get_token())
DB.stocks_init()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Type ticker, get price and change\n"
                                      "Try ticker + .me for moscow exhange\n"
                                      "Use ticker + number to get days change")


@bot.message_handler(commands=['stats'])
def handle_start_help(message):
    header_start = "*Start price: *"
    header_now = "*Now price: *"
    start_price = str(round(DB.start_price, 2))
    DB.calc_now_price()
    now_price = str(round(DB.now_price, 2))
    bot.send_message(message.chat.id,
                     header_start + start_price + " USD\n" + header_now + now_price + " USD", parse_mode="Markdown")

    pass

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        message_words = str.split(message.text)
        tick = yf.Ticker(message_words[0])
        name = str(tick.info['shortName'])
        price = str(tick.info['open'])
        currency = str(tick.info['currency'])
        if len(message_words) > 1 and message_words[1].isdigit:
            history = tick.history(period=str(message_words[1] + "d"))
            change = round(((tick.info['open'] / history['Close'][0] - 1) * 100), 1)
        else:
            history = tick.history(period="20d")
            change = round(((tick.info['open'] / history['Close'][0] - 1) * 100), 1)
        if change >= 10:
            change_sign = emoji.emojize("🚀")
        elif change > 0:
            change_sign = emoji.emojize("⬆")
        elif change < -10:
            change_sign = emoji.emojize("💩")
        elif change < 0:
            change_sign = emoji.emojize("⬇")
        else:
            change_sign = ""
        bot.send_message(message.chat.id, name + "\nPrice: " + price + " " + currency + ", " + str(change) + "% " + change_sign)
    except:
        bot.reply_to(message, "Error")


bot.polling()
