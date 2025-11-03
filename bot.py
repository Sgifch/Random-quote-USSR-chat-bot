import telebot
from telebot import types
import sqlite3
import random

#Функции БД---------------------------------------------------------------------------------------------
def RandomQuotes(id):
    connection = sqlite3.connect('QuotesUSSR.db')

    #Получение последней записи
    cursor = connection.cursor()

    isCheck = CheckTable(id)
    if isCheck:
        tableName = str(id)
        print("Использую таблицу пользователя")
    else:
        tableName = "Quotes"
        print("Использую основную таблицу")

    cursor.execute("SELECT * FROM '" + tableName + "'")
    n = cursor.fetchall()
    rnd = random.randint(1, len(n))
    
    #Получение случайной записи
    s = 'SELECT * FROM Quotes WHERE ID = ' + str(rnd)
    cursor.execute(s)
    l = cursor.fetchall()
    connection.close()

    return l

#Вставка новой записи
def InsertQuotes(id, quotes, picter):
    connection = sqlite3.connect('QuotesUSSR.db')
    cursor = connection.cursor()
    isCheck = CheckTable(id)

    if isCheck: #Если таблица существует
        print("Добавляю запись в существующую таблицу")
    else: #Если таблица не существует
        print ("Добавляю нового пользователя")
        s="CREATE TABLE '"+ str(id)+"' AS SELECT * FROM 'Quotes'"
        cursor.execute(s)
        cursor.fetchall()
    
    cursor.execute("SELECT * FROM '" + str(id) + "' ORDER BY ID DESC LIMIT 1")
    n = cursor.fetchall()

    s = "INSERT INTO '" + str(id) + "' (ID, quotes, picters) VALUES ('"+ str(n[0][0]+1) +"','"+ quotes +"', '"+ picter +"')"
    cursor.execute(s)
    cursor.fetchall()
    connection.commit()

    connection.close()

#Проверка наличия таблицы с именем id пользователя
def CheckTable(id):
    connection = sqlite3.connect('QuotesUSSR.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=" + str(id))
    i = cursor.fetchall() 

    if len(i) == 0:
        isCheck = False
    else:
        isCheck = True

    connection.close()
    return isCheck

#Просмотр всех записей
def ViewQuotes(id):
    connection = sqlite3.connect('QuotesUSSR.db')
    cursor = connection.cursor()

    isCheck = CheckTable(id)
    if isCheck:
        tableName = str(id)
        print("Использую таблицу пользователя")
    else:
        tableName = "Quotes"
        print("Использую основную таблицу")

    cursor.execute("SELECT * FROM '" + tableName + "'")
    l = cursor.fetchall()
    connection.close()

    return l

#Удаление записи
def DeleteQuotes(id):
    connection = sqlite3.connect('QuotesUSSR.db')
    cursor = connection.cursor()

    isCheck = CheckTable(id)
    if isCheck:
        msg = bot.send_message(id, "Введите номер записи для удаления (/cancel для отмены):")
        bot.register_next_step_handler(msg, InputDeleteMessage)
    else:
        bot.send_message(id, "Пока я не могу удалять записи :(. Попробуйте создать новую запись")
        return
    
    


#Обработка сообщений-------------------------------------------------------------------------------------------
#Чтение первого сообщения
def InputFirstMessage(message):
    quotes = message.text
    if quotes == '/cancel':
        bot.send_message(message.from_user.id, "Добавление новой цитаты отменено")
        return
    msg = bot.send_message(message.from_user.id,"Введите ссылку на картинку (/cancel для отмены):")
    bot.register_next_step_handler(msg, InputSecondMessage, quotes)

#Чтение второго сообщения
def InputSecondMessage(message, quotes):
    picter = message.text
    if picter == '/cancel':
        bot.send_message(message.from_user.id, "Добавление новой цитаты отменено")
        return
    
    try:
        InsertQuotes(message.from_user.id, quotes, picter)
        bot.send_message(message.from_user.id, "Новая цитата была добавлена ;)")
    except Exception as e:
        print (e)
        bot.send_message(message.from_user.id, "Произошла ошибка :(")

#Чтение id для удаления
def InputDeleteMessage(message):
    id = message.text
    connection = sqlite3.connect('QuotesUSSR.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM '" + str(message.from_user.id) + "' WHERE ID='" + str(id) + "'")
    cursor.fetchall()

    l = ViewQuotes(message.from_user.id)

    if int(id) != len(l):
        for i in range (int(id), len(l)):
            cursor.execute("UPDATE '" + str(message.from_user.id) + "' SET ID = '" + str(l[i][0] - 1) + "' WHERE ID = '" + str(l[i][0]) + "'")
            cursor.fetchall()
    
    connection.commit()
    connection.close()
    bot.send_message(message.from_user.id, "Цитата была удалена")

#----------------------------------------------------------------------------------------------------------------
BOT_TOKEN = '8037922129:AAGaXHrOllzBxEyZyxFa02FedQbgBk1cU8Y'
bot = telebot.TeleBot(BOT_TOKEN)
web_app = types.WebAppInfo(url="https://sgifch.github.io/Random-quote-USSR-chat-bot/")

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Приветствую! Я говорю случайными цитатами из фильмов!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if (message.text == "Начать"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Случайная цитата")
        btn3 = types.KeyboardButton("Добавить свою цитату")
        btn4 = types.KeyboardButton("Просмотреть все цитаты")
        btn5 = types.KeyboardButton("Удалить цитату")
        markup.add(btn2, btn3)
        markup.add(btn4)
        markup.add(btn5)
        bot.send_message(message.from_user.id, "Ну что ж, приступим 🎉!", reply_markup=markup)
    
    elif (message.text == "Случайная цитата"):
        l=RandomQuotes(message.from_user.id)
        text = l[0][1]
        img = l[0][2]
        try:
            bot.send_photo(message.from_user.id, img, text)
        except:
            bot.send_message(message.from_user.id, "Ошибка. Не удалось вывести цитату:(")

    elif (message.text == "Добавить свою цитату"):
        msg = bot.send_message(message.from_user.id, "Введите цитату (/cancel для отмены):")
        bot.register_next_step_handler(msg, InputFirstMessage)
    
    elif (message.text == "Просмотреть все цитаты"):
        l = ViewQuotes(message.from_user.id)

        msg = ""
        for i in range (len(l)):
            msg += str(l[i][0]) + ". " + l[i][1] + "\n"

        bot.send_message(message.from_user.id, msg)
    
    elif (message.text == "Удалить цитату"):
        DeleteQuotes(message.from_user.id)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(web_app_message):
    try:

        if web_app_message == "1":
            bot.send_message(web_app_message.chat.id, "hi")
        else:
            bot.send_message(web_app_message.chat.id, "❌ Жанр не найден. Попробуйте еще раз.")

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(web_app_message.chat.id, "❌ Произошла ошибка. Попробуйте еще раз.")

bot.polling(none_stop=True, interval=0)