import webbrowser
import sqlite3
import requests
import datetime

import telebot
from telebot import types
import telegram
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot('qwe')
WEATHER_API = '99f30b3d30059ebfe3fdf6f91697593c'


@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect('kiri4.sql')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE)''')
    conn.commit()
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, add_users)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('View website')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Exchange rate')
    btn3 = types.KeyboardButton('Weather')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}.', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'View website':
        site(message)
    elif message.text == 'Exchange rate':
        exchange_rate(message)
    elif message.text == 'Weather':
        ask_city(message, get_weather)


def add_users(message):
    conn = sqlite3.connect('kiri4.sql')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (message.from_user.username,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO users (username) VALUES (?)", (message.from_user.username,))
        conn.commit()
    cur.close()
    conn.close()


def ask_city(message, chapter):
    bot.send_message(message.chat.id, 'Enter the name of the city:')
    bot.register_next_step_handler(message, chapter)


def exchange_rate(message):
    city = 'Брест'
    res = requests.get(f'https://belarusbank.by/api/kursExchange?city={city}')
    data = res.json()

    if res.status_code == 200 and data:
        exchange_info = f"Курс на {datetime.date.today()} в отделах Беларусбанк в городе {city}:\n"
        for currency, buy_rate in [('USD', 'USD_in'), ('USD', 'USD_out'),
                                  ('EUR', 'EUR_in'), ('EUR', 'EUR_out'),
                                  ('RUB', 'RUB_in'), ('RUB', 'RUB_out')]:
            sell_rate_key = f"{currency}_out"
            if buy_rate in data[0] and sell_rate_key in data[0]:
                exchange_info += f"покупка {currency} {data[0][buy_rate]}, " \
                                f"продажа {currency} {data[0][sell_rate_key]}\n"
        bot.reply_to(message, exchange_info)
        main(message)
    else:
        bot.reply_to(message, f"Не удалось получить информацию о курсе валюты на {datetime.date.today()} для города {city}.")
        main(message)


def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric')
    data = res.json()
    if data['cod'] == 200:
        weather_info = f"Сейчас в городе {city} {data['weather'][0]['description']}, " \
                       f"температура {data['main']['temp']}°C."
        bot.reply_to(message, weather_info)
        main(message)
    else:
        bot.reply_to(message, f"Не удалось получить информацию о погоде для города {city}.")
        main(message)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    keyboard = [[InlineKeyboardButton('Открыть сайт', url='https://www.youtube.com/watch?v=7MdDtczKBsY')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, 'Нажмите кнопку, чтобы открыть сайт', reply_markup=reply_markup)
    main(message)


@bot.message_handler(commands=['info'])
def userInfo(message):
    bot.send_message(message.chat.id, message.from_user.username)


@bot.message_handler(commands=['users'])
def showUsers(message):
    conn = sqlite3.connect('kiri4.sql')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        if not users:
            mes = "Пока нет зарегистрированных пользователей."
        else:
            num_users = len(users)
            mes = f"Количество пользователей: {num_users}\n\n```\n"
            for user in users:
                mes += f"Username: {user[1]}\n"
            mes += "```"

        bot.send_message(message.chat.id, mes, parse_mode="Markdown")

    except sqlite3.Error as e:
        bot.send_message(message.chat.id, f"Ошибка при работе с базой данных: {e}")

    finally:
        cur.close()
        conn.close()
        main(message)


bot.polling(none_stop=True)
