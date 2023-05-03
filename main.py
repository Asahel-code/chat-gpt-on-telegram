import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

bot_token = os.environ.get('TELEGRAM_KEY')
bot = telegram.Bot(token=bot_token)

openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.ChatCompletion()


def on_finish(error, response):
    if error is not None:
        raise error
    print(response)


def handle_start(update, context):
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id, text='Hello and welcome to Mkuu bot, what information would like me to offer you?')


def handle_message(update, context):
    message = update.message
    chat_id = message.chat_id

    user_message = message.text

    chat_log = [{
        'role': 'user',
        'content': user_message,
    }]
    
    response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
    answer = response.choices[0]['message']['content']
    bot.send_message(chat_id=chat_id, text=answer)


updater = Updater(token=bot_token, use_context=True)

start_handler = CommandHandler('start', handle_start)
updater.dispatcher.add_handler(start_handler)

message_handler = MessageHandler(Filters.text, handle_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling()
