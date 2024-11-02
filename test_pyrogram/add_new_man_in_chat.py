from pyrogram import Client, filters
from decouple import config

# Создаем экземпляр клиента
bot = Client(
    name=config('LOGIN'),
    api_id=config('API_ID'),
    api_hash=config('API_HASH'),
    phone_number=config('PHONE'),
)

# Название чата (группы или канала) без '@'
CHAT_NAME = 'this_chat_love'

@bot.on_chat_member_updated(filters.group)  # Отслеживаем изменения участников групп
def member_updated(_, update):
    # Проверяем, был ли участник добавлен
    if update.new_chat_member.status == "member":
        new_user = update.new_chat_member.user
        bot.send_message(
            CHAT_NAME,
            f"Привет! Добро пожаловать в группу!"
        )
        print(f"Сообщение отправлено новому участнику: ")

# Запуск клиента
if __name__ == "__main__":
    bot.run()
