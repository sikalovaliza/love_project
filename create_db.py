from db import create_database

# Замените на ваши параметры подключения
DATABASE_URL = "postgresql://tanya:123456@localhost/social_media_db"

create_database(DATABASE_URL)
