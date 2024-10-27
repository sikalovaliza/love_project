from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import User, VkUser, VkInteraction, Post, TgUser, Chat, TgInteraction

DATABASE_URL = "postgresql://tanya:123456@localhost/social_media_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# В User, VkInteraction, TgInteraction добавлять id не нужно (auto increment)
# Пример добавления пользователя из вк
'''new_vk_user = VkUser(
  vk_id=1, 
  full_name='Иван Иванов', 
  city='Москва', 
  education='МФТИ', 
  family_status='Не женат', 
  friends=[2, 3], 
  groups=['Котики', 'Собачки']
)
session.add(new_vk_user)'''
# Пример добавления пользователя из тг
'''new_tg_user = TgUser(
  tg_id=2, 
  user_name='fedya_fedorov'
)
session.add(new_tg_user)'''
   
session.commit()
session.close()