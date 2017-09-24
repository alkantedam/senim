#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler

import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# ------------Logger---------------------

import os
import requests
from pydub import AudioSegment
from ffmpy import FFmpeg
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import Bot, File, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from wit import Wit


client = Wit("3ZEVBYRASI3M467KEEXZMAI5UATB7N3A")
token = '435657974:AAH6rNnTGHCxvkxaofUfXUP9KRtOsNA6HuU'
updater = Updater(token)
bot = Bot(token)
dispatcher = updater.dispatcher


def start(bot, update):
    send_bot("Вы можете записать аудиосообщение для того, чтобы сделать заказ", update.message.chat_id)

def hello(bot, update):
	update.message.reply_text(
        'Здравсвуйте, {}. Я - бот, который поможет вам в использовании приложения Senim'.format(update.message.from_user.first_name))

def about(bot, update):

    kb = [
          [telegram.InlineKeyboardButton("Я - продавец",callback_data="seller")],
          [telegram.InlineKeyboardButton("Я - покупатель",callback_data="consumer")]
        ]
    markup = telegram.InlineKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите необходимую для вас информацию: ", reply_markup = markup)
    

def query(bot, update):
    chat_id = str(update.callback_query.message.chat_id)

    if update.callback_query.data == 'seller':
        send_bot("Каждый участник Senim дает 10% скидки на все свои товары и услуги. В обмен он получает 10% скидки на товары и услуги других участников. Бонусы, полученные при продаже товара, Вы можете использовать при покупке товаров и услуг у своих поставщиков, которые являются участниками Senim.",chat_id)
    if update.callback_query.data == 'consumer':
        send_bot("Вы регистрируетесь и становитесь участником программы лояльности. Пополняете баланс и получаете бонусы из расчета 100 бонусов на каждые 900 тенге. 1 бонус = 1 тенге. Бонусы используются для получения скидок.",chat_id)


def voice(bot, update):
    print(update.message)
    global send_idea_loc
    global send_anon_loc
    voice_file_id = update.message.voice.file_id #file_id
    voice_file = bot.getFile(voice_file_id) #File
    voice_file_path = voice_file.file_path
    voice_file.download()
    resp = None

    file_name = voice_file_path.split('/')[-1]
    final_name = file_name.replace('oga','wav')

    ff = FFmpeg (
        inputs={file_name : None},
        outputs={final_name: None})
    ff.run()

    with open(final_name, 'rb') as f:
      resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
    print(resp)
    message_text = str(resp['_text'].encode('utf-8'))
    print(message_text)

    os.remove(final_name)
    os.remove(file_name)

    if 'intent' in str(resp):
        intent = resp['entities']['intent']
        intent_confidence = float(str(intent[0]['confidence'])) #Уверенность
        intent_value = str(intent[0]['value']) #Намерение
        bot.send_message(chat_id = update.message.chat_id, text = intent_value+": "+str(intent_confidence))

        if intent_value == 'get_places':
            if 'japan' in str(resp):
                send_bot("Хер ты получишь свои суши",update.message.chat_id)
            if 'italian' in str(resp):
                send_bot("Обмажься своей пастой, усатый",update.message.chat_id)
            if 'type' in str(resp):
                send_bot("Купи донер, мажор",update.message.chat_id)


def voice_url(bot_says):
    url = "http://tts.voicetech.yandex.net/generate?key=6ffb35de-75b6-42e0-9baf-be1e401cd8f0&text=%s&format=mp3&lang=ru-RU&speaker=omazh"
    return url % bot_says.replace("%","%25").replace(" ","%20").replace(".","%2E").replace(":","%3A")

def download_file(url, name):
    local_filename = name+".mp3"
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename

def sendAudio(some_text, chat_id=""):
    url_down = voice_url(some_text)
    download_file(url_down, "oss")
    file1 = {'voice':open('oss.mp3','rb')}
    payload = {'chat_id':chat_id}
    r = requests.post("https://api.telegram.org/bot{}/sendVoice".format(token),params=payload, files = file1)
    os.remove("oss.mp3")

def send_bot(text, chat_id):
    sendAudio(text, chat_id)
    bot.send_message(chat_id = chat_id, text = text)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

hello_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hello_handler)

about_handler = CommandHandler('about', about)
dispatcher.add_handler(about_handler)

voice_handler = MessageHandler(Filters.voice, voice)
dispatcher.add_handler(voice_handler)

query_handler = CallbackQueryHandler(query)
dispatcher.add_handler(query_handler)

updater.start_polling()
