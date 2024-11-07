from decouple import config
import os
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv('.env.bot')

API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')

CHAT_NAME = 'this_chat_love'

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)

async def check_bio_links(chat_id):
    chat = await app.get_chat(chat_id)
    async for member in app.get_chat_members(chat.id):
       print(member.GetFullUser())
       '''bio = member.user.bio if member.user.bio else ""
        if "t.me/" in bio:
            link = bio.split("t.me/")[-1].split()[0]
            try:
                new_chat = await app.get_chat(link)
                print(f"Получилось зайти в {link}")
                # Рекурсивный вызов для нового чата
                await check_bio_links(new_chat.id)
            except Exception as e:
                print(f"Не удалось получить чат {link}: {e}")'''

async def main():
    print("запустилось")
    async with app:
        print("запустилось1")
        await check_bio_links(CHAT_NAME)

if __name__ == "__main__":
    app.run(main())
