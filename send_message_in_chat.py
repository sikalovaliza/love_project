#отправляет сообщение в чат

from pyrogram import Client
import os
from decouple import config

bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))

CHAT_NAME = 'this_chat_love'

MESSAGE = "Привет, это тестовое сообщение!"

def send_message():
    with bot:
        bot.send_message(CHAT_NAME, MESSAGE)
        print("Сообщение отправлено!")

if __name__ == "__main__":
    send_message()
