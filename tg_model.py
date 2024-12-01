from pyrogram import Client, enums
from decouple import config
import random
import asyncio
import re
from datetime import datetime
from dotenv import load_dotenv
import os

from add_methods_dao import add_many_users_tg_chat, add_one_action_tg_interaction, add_one_tg_group, add_one_tg_message, add_one_tg_stats, add_one_user_tg
from sql_enums import TgActionEnum

load_dotenv('.env.bot')

API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')

chats = [
  'chatindustrialbioinformatics'
]

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)

# Регулярное выражение для поиска упоминаний
mention_pattern = re.compile(r'@(w+)')\

link_pattern = re.compile(r'https?://t\.me/([a-zA-Z0-9_]+)')

async def process_chat(chat_name):
  try:
      chat = await app.get_chat(chat_name)
      print(chat)
      async for message in app.get_chat_history(chat.id):
          if message.text:
              links = link_pattern.findall(message.text)
              print(links)
              for link in links:
                  try:
                      new_chat = await app.get_chat(link)
                      print(f"Зашел в чат: {link}")
                      await process_chat(new_chat.username)
                  except Exception as e:
                      print(f"Ошибка при попытке зайти в чат {link}: {e}")
  except Exception as e:
      print(f"Не удалось получить чат {chat_name}: {e}")


async def main():
  async with app:
    for CHAT_NAME in chats:
      #try:
        chat = await app.get_chat(CHAT_NAME)
        #print(f"Работа с чатом: {CHAT_NAME}")
        participants = await app.get_chat_members_count(chat.id)
        #print(f"Количество участников: {participants}")
        group = {
            'chat_id':str(chat.id), 
            'chat_name': f"{CHAT_NAME}", 
            'users_count' : participants
          }
        try:
          new_group_id = await add_one_tg_group(group_data=group)
        except Exception as e:
           print(f"Ошибка при обработке чата '{CHAT_NAME}': {str(e)}")

        dt = datetime.fromisoformat('2023-10-25T15:30:00')

        async for member in app.get_chat_members(chat.id):
          username = f"@{member.user.username}" if member.user.username else "Без имени"
          #print(f"- {username}")
          #print(member)
          tg_user={
            'tg_id': str(member.user.id), 
            'user_name': f'{username}',
            'first_name': f'{member.user.first_name}',
            'last_name': f'{member.user.last_name}',
            #'last_online':member.user.last_online_date 
            'last_online': dt
          }
          try:
            new_tg_user_id = await add_one_user_tg(user_data=tg_user)
          except Exception as e:
            print(f"Ошибка при обработке юзера '{username}': {str(e)}")

        async for action in app.get_chat_history(chat.id):
          #print(action)
          if action.text:
            statistics={'reaction_count': {'heart': '0'}}
            if action.reactions:
              for reaction in action.reactions.reactions:
                emoji = str(reaction.emoji) 
                count = str(reaction.count)
                statistics={'reaction_count': {emoji: count}}
            try:
                new_stat_id = await add_one_tg_stats(stats_data=statistics)
            except Exception as e:
              print(f"Ошибка при обработке действия: {str(e)}")
            message={
                'chat_id': str(chat.id),
                'id': str(action.id), 
                'text': f"{action.text}", 
                'statistics':new_stat_id
              }
            try:
              new_message = await add_one_tg_message(message_data=message)
              #print('cooбщение положено')
            except Exception as e:
                print(f"Ошибка при закладке сообщения: {str(e)}")

            sender_username = f"@{action.from_user.username}" if action.from_user.username else "Без имени"
            #print(f"Сообщение от {sender_username}: '{action.text}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
            new_action={
                'chat_id': str(chat.id), 
                'action': TgActionEnum.message, 
                'action_from': str(action.from_user.id), 
                'message_id': str(action.id),
                'message_chat_id': str(chat.id),
                'time': action.date
            }

            try:
              new_tg_action = await add_one_action_tg_interaction(interaction_data=new_action)
            except Exception as e:
                print(f"Ошибка при закладке события: {str(e)}")

            
          if action.new_chat_members:
            print(action)
            for member in action.new_chat_members:
              new_from = action.from_user.first_name if action.from_user else "Неизвестный"
              #print(f"{member.first_name} был добавлен в чат '{chat.title}', его добавил '{new_from}'")
              new_action={
                'chat_id': str(chat.id), 
                'action': TgActionEnum.add_user, 
                'action_from': str(action.from_user.id), 
                'action_to': str(member.id), 
                'message_id': str(action.id),
                'message_chat_id': str(chat.id),
                'time': action.date
              }
              try:
                new_tg_action = await add_one_action_tg_interaction(interaction_data=new_action)
              except Exception as e:
                print(f"Ошибка при добавлении участника: {str(e)}")

          if action.left_chat_member:
            for member in action.left_chat_member:
              print(f"{action.left_chat_member.first_name} был удален из чата '{chat.title}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
              new_action={
                'chat_id': str(chat.id), 
                'action': TgActionEnum.delete, 
                'action_from': str(action.from_user.id), 
                'action_to': str(member.user.id), 
                'message_id': str(action.id),
                'message_chat_id': str(chat.id),
                'time': action.date
              }
              try:
                  new_tg_action = await add_one_action_tg_interaction(interaction_data=new_action)
              except Exception as e:
                  print(f"Ошибка при обработке действия: {str(e)}")

          if action.reply_to_message_id:
            print(f"{sender_username} ответил на сообщение от {action.reply_to_message_id}'")
            new_action={
              'chat_id': str(chat.id), 
              'action': TgActionEnum.reply, 
              'action_from': str(action.from_user.id), 
              'reply_on_id': str(action.reply_to_message_id),
              'message_id': str(action.id),
              'message_chat_id': str(chat.id),
              'time': action.date
            }
            try:
              await add_one_action_tg_interaction(new_action)
            except Exception as e:
              print(f"Ошибка при обработке действия: {str(e)}")

          if action.text:
              mentions = mention_pattern.findall(action.text)
              if mentions:
                mentioned_users = ', '.join(mentions)
                print(f"{action.from_user.username} упомянул(а): {mentioned_users}")
                new_action={
                  'chat_id': str(chat.id), 
                  'action': TgActionEnum.reply, 
                  'action_from': str(action.from_user.id), 
                  'message_id': str(action.id),
                  'message_chat_id': str(chat.id),
                  'time': action.date
                }
                try:
                  new_tg_action = await add_one_action_tg_interaction(interaction_data=new_action)
                except Exception as e:
                  print(f"Ошибка при обработке действия: {str(e)}")

            

            #await process_chat(CHAT_NAME)



if __name__ == "__main__":
    app.run(main())