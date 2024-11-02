#выводить историю сообщений в чате

from pyrogram import Client, filters
from decouple import config

bot = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)

CHAT_NAME = 'mychat123445'

async def main():
    async with bot:
        async for message in bot.get_chat_history(CHAT_NAME):
            print(f"Сообщение: {message.text}")

if __name__ == "__main__":
    bot.run(main())
