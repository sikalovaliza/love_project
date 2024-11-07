import os
import re
from decouple import config
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv('.env.bot')

API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)
CHAT_NAME='this_chat_love'
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
    print("запустилось")
    async with app:
        print("запустилось1")
        await process_chat(CHAT_NAME)

if __name__ == "__main__":
    app.run(main())
