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
mention_pattern = re.compile(r'@(w+)')


async def main():
  async with app:
    for CHAT_NAME in chats:
      try:
        chat = await app.get_chat(CHAT_NAME)
        print(f"Работа с чатом: {CHAT_NAME}")
        participants = await app.get_chat_members_count(chat.id)
        print(f"Количество участников: {participants}")
        new_chat = [{'chat_id':str(chat.id), 'chat_name': f"{CHAT_NAME}", 'users_count' : participants}]
        '''try:
          await add_many_users_tg_chat(users_data=new_chat) 
        except Exception as e:
           print(f"Ошибка при обработке чата '{CHAT_NAME}': {str(e)}")'''

        async for member in app.get_chat_members(chat.id):
          username = f"@{member.user.username}" if member.user.username else "Без имени"
          print(f"- {username}")
          user={'tg_id': str(member.user.id), 'user_name': f'{username}'}
          '''try:
            await add_one_user_tg(user)
          except Exception as e:
            print(f"Ошибка при обработке юзера '{username}': {str(e)}")'''

        async for action in app.get_chat_history(chat.id, limit=100):
          print(action)
          if action.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            #print(action)
            if action.new_chat_members:
              for member in action.new_chat_members:
                  new_from = action.from_user.first_name if action.from_user else "Неизвестный"
                  print(f"{member.first_name} был добавлен в чат '{chat.title}', его добавил '{new_from}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
                  new_action={'chat_id': str(chat.id), 'action': TgActionEnum.add_user, 'action_from': str(action.from_user.id), 'action_to': str(member.id), 'time': action.date}
                  '''try:
                    await add_one_action_tg_inter(new_action)
                  except Exception as e:
                    print(f"Ошибка при обработке действия: {str(e)}")'''

            if action.left_chat_member:
              for member in action.left_chat_members:
                print(f"{action.left_chat_member.first_name} был удален из чата '{chat.title}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
                new_action={'chat_id': str(chat.id), 'action': TgActionEnum.left_user, 'action_from': str(action.from_user.id), 'action_to': str(member.id), 'time': action.date}
                '''try:
                    await add_one_action_tg_inter(new_action)
                except Exception as e:
                    print(f"Ошибка при обработке действия: {str(e)}")'''
            
            if action.text:
              sender_username = f"@{action.from_user.username}" if action.from_user.username else "Без имени"
              print(f"Сообщение от {sender_username}: '{action.text}' {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
              new_action={'chat_id': str(chat.id), 'action': TgActionEnum.message, 'action_from': str(action.from_user.id), 'time': action.date}
              new_tg_stat={'reaction':'none', 'count': 0}
              new_tg_message={'id': action.id, 'text': f"{action.text}", 'statistics': action.id}
              '''try:
                await add_one_action_tg_inter(new_action)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")
              
              try:
                await add_one_tg_mess(new_tg_message)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")

              try:
                await add_one_tg_stat(new_tg_stat)
              except Exception as e:
                 print(f"Ошибка при обработке действия: {str(e)}")'''

            # Проверка на ответ на сообщение
            '''if action.reply_to_message_id:
                print(f"{sender_username} ответил на сообщение от {action.reply_to_message_id}'")

            # Получаем имя пользователя, отправившего сообщение
            mentions = mention_pattern.findall(action.text)

            if mentions:
                # Создаем строку с упоминаниями
                mentioned_users = ', '.join(mentions)
                print(f"{action.from_user.username} упомянул(а): {mentioned_users}")'''

            # Проверка на пересылку сообщения
            if action.forward_from:
              forward_sender_username = f"@{action.forward_from.username}" if action.forward_from.username else "Без имени"
              print(f"Сообщение переслано от {forward_sender_username}")

            

      except Exception as e:
        print(f"Ошибка при обработке чата '{CHAT_NAME}': {str(e)}")

if __name__ == "__main__":
    app.run(main())