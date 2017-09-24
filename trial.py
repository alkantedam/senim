
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import telegram 
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


token ='384257512:AAGHyGMegHqiZBpvgILcuuUA616TU1Zu0Oc'
updater = Updater(token)
dispatcher = updater.dispatcher

def start(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text="Hello, I'm a bot. Please talk to me")


def key(bot, update):
	keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
				 InlineKeyboardButton("Option 2", callback_data='2'),
				 InlineKeyboardButton("Default Option", callback_data = '4')],

				[InlineKeyboardButton("Option 3", callback_data='3')]]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(bot,update):
	query = update.callback_query
	
	bot.send_message(text="Selected option: %s" % query.data,
						  chat_id=query.message.chat_id,
						  message_id=query.message.message_id)

start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)
key_handler = CommandHandler('key', key)
dispatcher.add_handler(key_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)

updater.start_polling()