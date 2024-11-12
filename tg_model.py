from pyrogram import Client, enums
from decouple import config
import random
import asyncio
import re
import datetime
from dotenv import load_dotenv
import os

from add_methods_dao import add_many_users_tg_chat, add_one_action_tg_inter, add_one_tg_mess, add_one_tg_stat, add_one_user_tg
from sql_enums import TgActionEnum

load_dotenv('.env.bot')

API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')

chats = [
    'new_love_chat',
    'this_chat_love'
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
      try:
        chat = await app.get_chat(CHAT_NAME)
        print(f"Работа с чатом: {CHAT_NAME}")
        participants = await app.get_chat_members_count(chat.id)
        print(f"Количество участников: {participants}")
        new_chat = [
          {
            'chat_id':str(chat.id), 
            'chat_name': f"{CHAT_NAME}", 
            'users_count' : participants
          }]
        try:
          await add_many_users_tg_chat(users_data=new_chat) 
        except Exception as e:
           print(f"Ошибка при обработке чата '{CHAT_NAME}': {str(e)}")

        async for member in app.get_chat_members(chat.id):
          username = f"@{member.user.username}" if member.user.username else "Без имени"
          print(f"- {username}")
          user={
            'tg_id': str(member.user.id), 
            'user_name': f'{username}',
            'first_name': f'{member.user.first_name}',
            'last_name': f'{member.user.last_name}',
            'last_online': member.user.last_online_date
          }
          try:
            await add_one_user_tg(user)
          except Exception as e:
            print(f"Ошибка при обработке юзера '{username}': {str(e)}")

        async for action in app.get_chat_history(chat.id):
          print(action)
          if action.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            print(action)
            if action.new_chat_members:
              for member in action.new_chat_members:
                  new_from = action.from_user.first_name if action.from_user else "Неизвестный"
                  print(f"{member.first_name} был добавлен в чат '{chat.title}', его добавил '{new_from}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
                  new_action={
                    'chat_id': str(chat.id), 
                    'action': TgActionEnum.add_user, 
                    'action_from': str(action.from_user.id), 
                    'action_to': str(member.id), 
                    'reply_on_chat_id': '0',
                    'reply_on_id': '0',
                    'message_chat_id': '0',
                    'message_id': str(action.id),
                    'time': action.date
                  }
                  '''try:
                    await add_one_action_tg_inter(new_action)
                  except Exception as e:
                    print(f"Ошибка при обработке действия: {str(e)}")'''

            if action.left_chat_member:
              for member in action.left_chat_members:
                print(f"{action.left_chat_member.first_name} был удален из чата '{chat.title}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
                new_action={
                  'chat_id': str(chat.id), 
                  'action': TgActionEnum.delete, 
                  'action_from': str(action.from_user.id), 
                  'action_to': str(member.id), 
                  'reply_on_chat_id': '0',
                  'reply_on_id': '0',
                  'message_chat_id': '0',
                  'message_id': str(action.id),
                  'time': action.date
                }
                try:
                    await add_one_action_tg_inter(new_action)
                except Exception as e:
                    print(f"Ошибка при обработке действия: {str(e)}")
            
            if action.text:
              sender_username = f"@{action.from_user.username}" if action.from_user.username else "Без имени"
              print(f"Сообщение от {sender_username}: '{action.text}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
              new_action={'chat_id': str(chat.id), 'action': TgActionEnum.message, 'action_from': str(action.from_user.id), 'time': action.date}
              new_tg_stat={'reaction':'none', 'count': 0}
              new_tg_message={'id': action.id, 'text': f"{action.text}", 'statistics': action.id}
              try:
                await add_one_action_tg_inter(new_action)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")
              
              '''try:
                await add_one_tg_mess(new_tg_message)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")

              try:
                await add_one_tg_stat(new_tg_stat)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")'''

            if action.reply_to_message_id:
                print(f"{sender_username} ответил на сообщение от {action.reply_to_message_id}'")
                new_action={
                  'chat_id': str(chat.id), 
                  'action': TgActionEnum.reply, 
                  'action_from': str(action.from_user.id), 
                  'reply_on_chat_id': (str(action.reply_to_message_id) + ' ' +str(chat.id)),
                  'reply_on_id': str(action.reply_to_message_id),
                  'message_chat_id': str(str(action.id) + ' ' + str(chat.id)),
                  'message_id': str(action.id),
                  'time': action.date
                }
                try:
                  await add_one_action_tg_inter(new_action)
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
                    'reply_on_chat_id': '',
                    'reply_on_id': '',
                    'message_chat_id': '',
                    'message_id': str(action.id),
                    'time': action.date
                  }
                  try:
                    await add_one_action_tg_inter(new_action)
                  except Exception as e:
                    print(f"Ошибка при обработке действия: {str(e)}")

            if action.reactions:
              new_reaction={
                'chat_id': str(chat.id), 
                'action': TgActionEnum.react, 
                'action_from': str(action.from_user.id), 
                'reply_on_chat_id': '0',
                'reply_on_id': '0',
                'message_chat_id': '0',
                'message_id': str(action.id),
                'time': action.date
              }
              try:
                await add_one_action_tg_inter(new_reaction)
              except Exception as e:
                print(f"Ошибка при обработке действия: {str(e)}")

            await process_chat(CHAT_NAME)

      except Exception as e:
        print(f"Ошибка при обработке чата '{CHAT_NAME}': {str(e)}")


if __name__ == "__main__":
    app.run(main())