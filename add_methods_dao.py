import asyncio
from typing import List
from dao.dao import UserDAO, VkUserDAO, VkInteractionDAO, PostDAO, TgUserDAO, ChatDAO, TgInteractionDAO
from sql_enums import VkActionEnum, TgActionEnum, FamilyStatusEnum, GenderEnum
from database import connection
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession


'''# Пример добавления одной записи в vk_users
@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await VkUserDAO.add(session=session, **user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

one_user = {'vk_id': 1, 'full_name': "Иван Иванов", 'city': "Москва", 'education': "МФТИ", 'family_status': FamilyStatusEnum.married_male, 'friends':[2, 3, 4], 'groups':["друзья", "музыка", "путешествия"]}
run(add_one(one_user))'''

# Пример добавления нескольких записей в vk_users
@connection
async def add_many_users(users_data: List[dict], session: AsyncSession):
    new_users = await VkUserDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.vk_id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

users = [
  {'vk_id': 2, 'gender': GenderEnum.female,'full_name': "Анна Смирнова", 'city': "Санкт-Петербург", 'education': "СПбГУ", 'family_status': FamilyStatusEnum.single_female, 'friends': [1, 5], 'groups': ["фотография", "спорт"]},
  {'vk_id': 1, 'gender': GenderEnum.male, 'full_name': "Иван Иванов", 'city': "Москва", 'education': "МФТИ", 'family_status': FamilyStatusEnum.married_male, 'friends':[2, 3, 4], 'groups':["друзья", "музыка", "путешествия"]}
]
#run(add_many_users(users_data=users))

tg_users = [
    {'tg_id': 11, 'user_name': "@new_user5"},
    {'tg_id': 12, 'user_name': "@new_user6"}
]

@connection
async def add_many_users_tg_chat(users_data: List[dict], session: AsyncSession):
    new_users = await ChatDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.chat_id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

@connection
async def add_many_user_tg(users_data: List[dict], session: AsyncSession):
    new_users = await ChatDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.tg_id for user in new_users]
    print(f"{user_ilds_list}")
    return user_ilds_list

@connection
async def add_one_user_tg(user_data: dict, session: AsyncSession):
    new_user = await TgUserDAO.add(session=session, **user_data)
    print(f"{new_user.tg_id}")
    return new_user.tg_id

@connection
async def add_one_action_tg_inter(user_data: dict, session: AsyncSession):
    new_user = await TgInteractionDAO.add(session=session, **user_data)
    print(f"{new_user.chat_id}")
    return new_user.chat_id

#run(add_many_users_tg(users_data=tg_users, dao=TgUserDAO))

#chats = [{'chat_id': 3, 'chat_name': 'new', 'users_count' : 5}]
#run(add_many_users_tg_chat(users_data=chats))