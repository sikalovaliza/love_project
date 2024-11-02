from pyrogram import Client
from decouple import config

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)

CHAT_NAME = 'this_chat_love'

async def main():
    async with app:
        chat = await app.get_chat(CHAT_NAME)

        # Получаем историю чата
        async for message in app.get_chat_history(chat.id, limit=100):  # Укажите нужное количество сообщений
            if message.reply_markup:
                # Проверяем наличие реакций
                for reaction in message.reply_markup.inline_keyboard:
                    for r in reaction:
                        if r.callback_data:
                          print(f"Сообщение: | Реакция: {r.text}")

            # Если имеется поле для reactions
            if message.reactions:
                for reaction in message.reactions:
                    for user_id in message.reactions.users.get(reaction, []):
                        user = await app.get_chat_member(chat.id, user_id)
                        print(f"{user.user.first_name} поставил реакцию '{reaction}' на сообщение: {message.text}")

if __name__ == "__main__":
    app.run(main())
