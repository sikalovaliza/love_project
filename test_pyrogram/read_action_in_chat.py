#стягивает историю чата и выводит кто был удален/добавлен в чат, дату и время

from pyrogram import Client, enums
from decouple import config
import datetime

app = Client(
    "my_account", 
    api_id=config('API_ID'),
    api_hash=config('API_HASH')
)

CHAT_NAME = 'this_chat_love'

async def main():
    async with app:
        chat = await app.get_chat(CHAT_NAME)

        # Получаем историю действий участников
        async for action in app.get_chat_history(chat.id):  # Укажите нужное количество сообщений
            if action.chat.type == enums.ChatType.GROUP or action.chat.type == enums.ChatType.SUPERGROUP:
                if action.new_chat_members:
                    for member in action.new_chat_members:
                        print(f"{member.first_name} был добавлен в чат {action.date.strftime('%Y-%m-%d %H:%M:%S')}")
                if action.left_chat_member:
                    print(f"{action.left_chat_member.first_name} был удален из чата {action.date.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    app.run(main())
