from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.handlers import ChatMemberUpdatedHandler, MessageHandler
import sqlite3
from pyrogram import Client, filters
from decouple import config
import time

# Установка базы данных
Base = declarative_base()
TARGET_CHAT_ID = 374150300

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///chat_activity.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))


def save_activity(chat_id, user_id, action):
    session = Session()
    activity = Activity(chat_id=chat_id, user_id=user_id, action=action)
    session.add(activity)
    session.commit()
    session.close()

@bot.on_chat_member_updated(filters.chat(TARGET_CHAT_ID))
def chat_member_update_handler(client, update):
    chat_id = update.chat.id
    user_id = update.new_chat_member.user.id
    action = ""

    if update.new_chat_member.status == "member":
        action = f"{update.new_chat_member.user.first_name} присоединился к чату"
    elif update.new_chat_member.status == "kicked":
        action = f"{update.new_chat_member.user.first_name} был исключён из чата"
    elif update.new_chat_member.status == "administrator":
        action = f"{update.new_chat_member.user.first_name} стал администратором чата"
    elif update.new_chat_member.status == "restricted":
        action = f"{update.new_chat_member.user.first_name} был ограничен в правах."

    if action:
        print(action)
        save_activity(chat_id, user_id, action)

def message_forwarded_handler(client, message):
    if message.forward_from:
        action = f"{message.from_user.first_name} переслал сообщение от {message.forward_from.first_name}"
        save_activity(message.chat.id, message.from_user.id, action)

def message_mentioned_handler(client, message):
    if message.mentioned_users:
        for user in message.mentioned_users:
            action = f"{message.from_user.first_name} отметил {user.first_name} в сообщении"
            save_activity(message.chat.id, message.from_user.id, action)

bot.add_handler(ChatMemberUpdatedHandler(chat_member_update_handler))
bot.add_handler(MessageHandler(message_forwarded_handler, filters.forwarded))
bot.add_handler(MessageHandler(message_mentioned_handler, filters.text & filters.mentioned))


bot.run()
