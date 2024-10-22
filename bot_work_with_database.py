from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
import os
from decouple import config

app = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))

@app.on_chat_member_updated(filters.chat('this_chat_love'))
async def handle_chat_member_update(client, chat_member_updated: ChatMemberUpdated):
    # Получение информации о событии
    user = chat_member_updated.new_chat_member.user
    if chat_member_updated.new_chat_member.status == "member":
        # Сообщение об добавлении участника
      print(f"👤 добавлен в чат.")
    elif chat_member_updated.new_chat_member.status == "left":
              # Сообщение об удалении участника
      print(f"👤 покинул чат.")
    elif chat_member_updated.new_chat_member.status == "administrator":
              # Сообщение о повышении участника до администратора
      print(f"👑 теперь администратор.")
    elif chat_member_updated.new_chat_member.status == "restricted":
              # Сообщение о понижении участника до ограниченного
      print(f"🔒 теперь ограничен в правах.")

app.start()




