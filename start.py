import telebot
from secure import get_token

bot = telebot.TeleBot(get_token())

text_messages = {
    'hello':
        u'Привет, {name}!\n\n'
        u'Этот бот помогает пересылать сообщения между чатом и группой.\n'
        u'Он должен быть участником минимум одной группы и чата, чтобы все получилось. '
        u'Напишите /settings для того, чтобы настроить.',

    'choose_group':
        u'Выберите группу из списка:',

    'choose chat':
        u'Выберите группу из списка:'
}


@bot.message_handler(commands=['settings'])
def choose_chat(message):
    bot.reply_to(message, text_messages['choose_group'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['hello'])
def handle_start_help(message):
    name = 'имя'
    bot.reply_to(message, text_messages['hello'] + name)
    pass


# @bot.message_handler(commands=['pin'])
# def handle_start_help(message):
#     pinChatMessage
#     bot.reply_to(message, text_messages['hello'] + name)
#     pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
