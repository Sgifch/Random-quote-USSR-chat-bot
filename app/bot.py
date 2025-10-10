import telebot
from telebot import types
import sqlite3
import random

def RandomQuotes():
    connection = sqlite3.connect('QuotesUSSR.db')

    #Получение последней записи
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Quotes ORDER BY ID DESC LIMIT 1')
    n = cursor.fetchall()
    rnd = random.randint(1, n[0][0])
    
    #Получение случайной записи
    s = 'SELECT * FROM Quotes WHERE ID = ' + str(rnd)
    cursor.execute(s)
    l = cursor.fetchall()
    connection.close()

    return l

BOT_TOKEN = 'ВАШ_ТОКЕН'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    #RandomQuotes()
    bot.send_message(message.from_user.id, "Приветствую! Я говорю случайными цитатами из фильмов!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if (message.text == "Начать"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Случайная цитата")
        markup.add(btn2)
        bot.send_message(message.from_user.id, "Ну что ж, приступим 🎉!", reply_markup=markup)
    
    elif (message.text == "Случайная цитата"):
        l=RandomQuotes()
        text = l[0][1]
        img = l[0][2]
        bot.send_photo(message.from_user.id, img, text)

bot.polling(none_stop=True, interval=0)