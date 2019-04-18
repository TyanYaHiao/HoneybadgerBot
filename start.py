import telebot
from secure import get_token

bot = telebot.TeleBot(get_token())


@bot.message_handler(commands=['settings'])
def choose_chat(message):
    bot.reply_to(message, "Выберите чат, в который будут пересылаться сообщения")
    bot.cha


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['hello'])
def handle_start_help(message):
    bot.reply_to(message, "Privet")
    pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
