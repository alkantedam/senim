#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# ------------Logger---------------------

import os
import json
import requests
from pydub import AudioSegment
from math import radians, cos, sin, asin, sqrt
from ffmpy import FFmpeg
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import Bot, File, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from wit import Wit

near_loc = False
near_cat_loc = False
food = False
hotels = False
sport = False
entertainment = False
beauty = False
market = False
medicine = False
other = False
def get_points():
    with open('points.json') as data_file:
        data = json.load(data_file)
    return data
    # {'id': 18394, 'name': 'Отель «ТАУ House»', 'category': 'Гостиница', 'longitude': 76.908764, 'latitude': 43.087581}


client = Wit("3ZEVBYRASI3M467KEEXZMAI5UATB7N3A")
token = '435657974:AAH6rNnTGHCxvkxaofUfXUP9KRtOsNA6HuU'
updater = Updater(token)
bot = Bot(token)
dispatcher = updater.dispatcher
points = get_points()

def start(bot, update):
    chat_id = update.message.chat_id
    username = update.message.chat.username

    telegram.ReplyKeyboardRemove(remove_keyboard = True)
    

    global points
    send_bot(
        'Здравствуйте, {}. Я - умный голосовой бот, который поможет вам в использовании приложения Senim. \n'.format(update.message.from_user.first_name), update.message.chat_id)
    bot.send_message(chat_id = update.message.chat_id, text = '/about - больше информации,\n/near - ближайшие точки')

    activate(bot, update.message.chat_id)
    
    url = "https://senimbot-1505821861966.firebaseio.com/telegram.json"

    payload = "{\n\t\"chat_id\":\"%s\",\n\t\"username\":\"%s\"\n}" % (chat_id,username)

    print(payload)
    headers = {
        'content-type': "application/json, charset=utf-8"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def loc_keyboard(bot, chat_id):
    kb = [
          [telegram.KeyboardButton("Отправить местоположение", request_location=True)]
    ]
    markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id = chat_id, text = 'Гды вы находитесь?', reply_markup = markup)

def activate(bot, chat_id):
    kb = [
        [telegram.KeyboardButton("/near")],
        [telegram.KeyboardButton("/near_cat")],
        [telegram.KeyboardButton("/ask")],
        [telegram.KeyboardButton("/help")],
        [telegram.KeyboardButton("/about")]

    ]
    markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(chat_id = chat_id, text = 'Выберите команду', reply_markup = markup)    

def about(bot, update):

    kb = [
          [telegram.InlineKeyboardButton("Я - продавец",callback_data="seller")],
          [telegram.InlineKeyboardButton("Я - покупатель",callback_data="consumer")]
        ]
    markup = telegram.InlineKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите необходимую для вас информацию: ", reply_markup = markup)

def ask(bot, update):

    send_bot(
        'Можете связаться с нашим доверенным оператором Senim и задать Ваш вопрос ', update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="Айгуль @username")

def help(bot, update):

    kb = [  
        [telegram.InlineKeyboardButton("/near",callback_data="near_loc")],
        [telegram.InlineKeyboardButton("/near_cat",callback_data="near_cat_loc")],
        [telegram.InlineKeyboardButton("/ask",callback_data="ask_option")],
        [telegram.InlineKeyboardButton("/help",callback_data="help_option")],
        [telegram.InlineKeyboardButton("/about",callback_data="about_option")],
         ]

    markup = telegram.InlineKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id, text="Команды для общения с ботом:", reply_markup = markup)

def near(bot, update):
    global near_loc
    global near_cat_loc
    near_cat_loc = False
    near_loc = True
    loc_keyboard(bot, update.message.chat_id)
def near_cat(bot, update):
    global near_cat_loc
    global near_loc
    near_loc = False
    near_cat_loc = True

    kb = [  
        [telegram.InlineKeyboardButton("Еда",callback_data="food")],
        [telegram.InlineKeyboardButton("Спорт",callback_data="sport")],
        [telegram.InlineKeyboardButton("Проживание",callback_data="hotels")],
        [telegram.InlineKeyboardButton("Развлечения",callback_data="entertainment")],
        [telegram.InlineKeyboardButton("Красота",callback_data="beauty")],
        [telegram.InlineKeyboardButton("Магазины",callback_data="market")],
        [telegram.InlineKeyboardButton("Медицина",callback_data="medicine")],
        [telegram.InlineKeyboardButton("Другое",callback_data="other")]
         ]
    markup = telegram.InlineKeyboardMarkup(kb)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите категорию: ", reply_markup = markup)

def query(bot, update):
    global near_cat_loc
    chat_id = str(update.callback_query.message.chat_id)
    global sport
    global food
    global hotels
    global entertainment
    global beauty
    global market
    global medicine
    global other
    near_cat_loc = True
    if update.callback_query.data == 'seller':
        send_bot("Каждый участник Senim дает 10% скидки на все свои товары и услуги. В обмен он получает 10% скидки на товары и услуги других участников. Бонусы, полученные при продаже товара, Вы можете использовать при покупке товаров и услуг у своих поставщиков, которые являются участниками Senim.",chat_id)
    if update.callback_query.data == 'consumer':
        send_bot("Вы регистрируетесь и становитесь участником программы лояльности. Пополняете баланс и получаете бонусы из расчета 100 бонусов на каждые 900 тенге. 1 бонус = 1 тенге. Бонусы используются для получения скидок.",chat_id)
    if update.callback_query.data == 'ask_option':
        send_bot("Вас напрямую свяжут с оператором",chat_id)
    if update.callback_query.data == 'near_loc':
        send_bot("Присылает ближайшие точки-партнеры Senim ",chat_id)
    if update.callback_query.data == 'near_cat_loc':
        send_bot("Присылает ближайшие к вам точки по заданной категории",chat_id)
    if update.callback_query.data == 'help_option':
        send_bot("Выводит список команд бота и их описание",chat_id)
    if update.callback_query.data == 'about_option':
        send_bot("Предоставляет информацию по сервису",chat_id)
    if update.callback_query.data == 'food':
        food = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'sport':
        sport = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'hotels':
        hotels = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'entertainment':
        entertainment = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'beauty':
        beauty = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'market':
        market = True
        loc_keyboard(bot, chat_id)    
    if update.callback_query.data == 'medicine':
        medicine = True
        loc_keyboard(bot, chat_id)
    if update.callback_query.data == 'other':
        other = True
        loc_keyboard(bot, chat_id)    
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def location(bot, update):
    global near_loc
    global near_cat_loc
    global points
    global sport
    global food
    global hotels
    global entertainment
    global beauty
    global market
    global medicine
    global other
    l = []
    if near_loc:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    # for point in points:
        telegram.ReplyKeyboardRemove(remove_keyboard = True)
        longitude = update.message.location['longitude']
        latitude = update.message.location['latitude']
        near_loc = False
        for point in points:
            distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
            if distance < 2:
                bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")

    
    elif near_cat_loc: 
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        near_cat_loc = False
        longitude = update.message.location['longitude']
        latitude = update.message.location['latitude']
        for point in points:
            if food:    
                if point['category'] == 'Рестораны' or  point['category'] == 'Бары' or point['category'] == 'Фастфуд' or point['category'] == 'Кафе':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 4:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        food = False      
            elif sport:
                if point['category'] == 'Фитнес центры' or  point['category'] == 'Спорт':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 4:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        sport = False
            elif hotels:
                if point['category'] == 'Отель' or  point['category'] == 'Гостиница' or point['category'] == 'Хостелы':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 9:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        hotels = False
            elif entertainment:
                if point['category'] == 'Интернет и компьютерные клубы' or  point['category'] == 'Кинотеатры'  or point['category'] == 'Ночные клубы и караоке' or point['category'] == 'Активный отдых':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 9:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        entertainment = False
            elif beauty:
                if point['category'] == 'Салоны красоты':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 9:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        beauty = False                        
                         
            elif market:                
                if point['category'] == 'Супермаркеты' or  point['category'] == 'Прочие магазины'  or point['category'] == 'Продуктовые магазины' or point['category'] == 'Минимаркеты':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 9:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        market = False
            elif medicine:                
                if point['category'] == 'Медицинские центры' or  point['category'] == 'Стоматологические центры':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 9:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        medicine = False
            elif other:                
                if point['category'] == 'Магазин Цветов' or  point['category'] == 'Строительные материалы' or point['category'] == 'Авто магазины' or point['category'] == 'Рекламные услуги' or point['category'] == 'Полиграфия и дизайн' or point['category'] == 'Одежда' or point['category'] == 'Подарки и сувениры' or point['category'] == 'Текстиль и кожа' or point['category'] == 'Организация и проведение праздников' or point['category'] == 'Автомойки':
                    distance = haversine(longitude, latitude, float(point['longitude']),float(point['latitude']))
                    if distance < 4:
                        bot.send_message(chat_id=update.message.chat_id, text="В радиусе 4 км:\n"+point['name']+"\n"+point['category']+"\n"+str(distance*1000)[:5]+"м")    
                        other = False   
                else:
                    send_bot("В радиусе 4 км ничего не обнаружено", update.message.chat_id) 
                    other = False                           
def voice(bot, update):
    global near_cat_loc
    global points
    global sport
    global food
    global hotels
    global entertainment
    global beauty
    global market
    global medicine
    global other
    print(update.message)

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
        #bot.send_message(chat_id = update.message.chat_id, text = resp['entities'])

        if intent_value == 'get_places':
            near_cat_loc = True    
            if 'sport' in str(resp):
                sport = True
                loc_keyboard(bot, update.message.chat_id)
            if 'food' in str(resp):
                food = True
                loc_keyboard(bot, update.message.chat_id)
            if 'hotels' in str(resp):
                hotels = True
                loc_keyboard(bot, update.message.chat_id)
            if 'entertainment' in str(resp):
                entertainment = True
                loc_keyboard(bot, update.message.chat_id)
            if 'beauty' in str(resp):
                beauty = True
                loc_keyboard(bot, update.message.chat_id)
            if 'market' in str(resp):
                market = True
                loc_keyboard(bot, update.message.chat_id)
            if 'medicine' in str(resp):
                medicine = True
                loc_keyboard(bot, update.message.chat_id)
            if 'other' in str(resp):
                other = True
                loc_keyboard(bot, update.message.chat_id)
            


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

near_handler = CommandHandler('near', near)
dispatcher.add_handler(near_handler)

near_cat_handler = CommandHandler('near_cat', near_cat)
dispatcher.add_handler(near_cat_handler)

about_handler = CommandHandler('about', about)
dispatcher.add_handler(about_handler)

ask_handler = CommandHandler('ask', ask)
dispatcher.add_handler(ask_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

voice_handler = MessageHandler(Filters.voice, voice)
dispatcher.add_handler(voice_handler)

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

query_handler = CallbackQueryHandler(query)
dispatcher.add_handler(query_handler)

updater.start_polling()