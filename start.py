import telebot
import emoji
import yfinance as yf
from secure import get_token

bot = telebot.TeleBot(get_token())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Type ticker, get price and change\n"
                                      "Try ticker + .me for moscow exhange\n"
                                      "Use ticker + number to get days change")


@bot.message_handler(commands=['hello'])
def handle_start_help(message):
    bot.reply_to(message, "Privet")
    pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        message_words = str.split(message.text)
        tick = yf.Ticker(message_words[0])
        # bot.send_message(message.chat.id, "*bold *text*", parse_mode="Markdown")
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
        elif change < 0:
            change_sign = emoji.emojize("⬇")
        else:
            change_sign = ""
        bot.send_message(message.chat.id, name + "\nPrice: " + price + " " + currency + ", " + str(change) + "% " + change_sign)
    except:
        bot.reply_to(message, "Error")


bot.polling()
