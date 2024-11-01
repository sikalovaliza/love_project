import sqlite3
from pyrogram import Client, filters
from decouple import config
import time

# Соединение с базой данных
conn = sqlite3.connect('database.db', timeout=10)

# Функция для выполнения запросов к БД
def execute_query(query):
    while True:
        try:
            conn.execute(query)
            break
        except sqlite3.OperationalError:
            time.sleep(1)  # Ждём перед повторной попыткой

# Инициализация клиента
bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))

# Закрываем соединение перед началом работы с Pyrogram
conn.close()

bot.start()
bot.send_message(chat_id=config('LOGIN'), text='Тестируем отправку сообщения себе')
bot.stop()
