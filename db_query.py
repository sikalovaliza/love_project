from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import User, VkUser, VkInteraction, Post, TgUser, Chat, TgInteraction
from db_url import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Запрос к бд
vk_users = session.query(VkUser).all()

for user in vk_users:
    print(user.full_name, user.city)

tg_users = session.query(TgUser).all()

for user in tg_users:
    print(user.user_name)

session.commit()
session.close()