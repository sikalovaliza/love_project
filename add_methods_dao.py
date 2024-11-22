import asyncio
from datetime import datetime
from typing import List
from dao.dao import TgStatisticsDAO, UserDAO, VkUserDAO, VkActionDAO, VkPostDAO, TgUserDAO, TgGroupStatsDAO, TgUserGroupActionDAO, TgStatisticsDAO, TgGroupMessageDAO, TgChannelStatsDAO 
from models import TgStatistics
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
  {'vk_id': '2', 'gender': GenderEnum.female,'first_name': "Анна", 'last_name': "Смирнова", 'city': "Санкт-Петербург", 'education': "СПбГУ", 'family_status': FamilyStatusEnum.single_female, 'friends': [1, 5], 'groups': ["фотография", "спорт"]},
  {'vk_id': '1', 'gender': GenderEnum.male, 'first_name': "Иван", 'last_name': "Иванов", 'city': "Москва", 'education': "МФТИ", 'family_status': FamilyStatusEnum.married_male, 'friends':[2, 3, 4], 'groups':["друзья", "музыка", "путешествия"]}
]
#run(add_many_users(users_data=users))

@connection
async def add_many_users_tg_chat(users_data: List[dict], session: AsyncSession):
    new_users = await TgGroupStatsDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.chat_id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

@connection
async def add_many_user_tg(users_data: List[dict], session: AsyncSession):
    new_users = await TgGroupStatsDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.tg_id for user in new_users]
    print(f"{user_ilds_list}")
    return user_ilds_list

@connection
async def add_one_user_tg(user_data: dict, session: AsyncSession):
    new_user = await TgUserDAO.add(session=session,  **user_data)
    print(f"{new_user.tg_id}")
    return new_user.tg_id

@connection
async def add_one_action_tg_interaction(interaction_data: dict, session: AsyncSession):
    new_user = await TgUserGroupActionDAO.add(session=session,  **interaction_data)
    print(f"{new_user.chat_id}")
    return new_user.chat_id

@connection
async def add_one_tg_message(message_data: dict, session: AsyncSession):
    new_mess = await TgGroupMessageDAO.add(session=session,  **message_data)
    print(f"{new_mess.id}")
    return new_mess

@connection
async def add_one_tg_stats(stats_data: dict, session: AsyncSession):
    new_stat = await TgStatisticsDAO.add(session=session,  **stats_data)
    print(f"{new_stat.id}")
    return new_stat.id

@connection
async def add_one_tg_group(group_data: dict, session: AsyncSession):
    new_group = await TgGroupStatsDAO.add(session=session,  **group_data)
    print(f"{new_group.chat_id}")
    return new_group.chat_id


async def main():
    dt = datetime.fromisoformat('2023-10-25T15:30:00')
    group = {'chat_id':'1', 'chat_name': 'hggg', 'users_count': 4}
    new_group_id = await add_one_tg_group(group_data=group)

    tg_user = {'tg_id': '11', 'user_name': "@new_user5", 'first_name': 'Иван', 'last_name': 'Иванов', 'last_online': dt}
    new_tg_user_id = await add_one_user_tg(user_data=tg_user)

    statistics = {'reaction_count': {'heart': 3}}
    new_stat_id = await add_one_tg_stats(stats_data=statistics)

    message = {'id':'12', 'chat_id': '1', 'text': 'hi', 'statistics': new_stat_id}
    new_message = await add_one_tg_message(message_data=message)
    
    tg_action = {'chat_id': new_group_id, 'action': TgActionEnum.message, 'action_from': new_tg_user_id, 'message_id': new_message.id, 'message_chat_id': new_message.chat_id, 'time': dt}
    new_tg_action = await add_one_action_tg_interaction(interaction_data=tg_action)
    print(new_tg_action + ' добавлено')

asyncio.run(main())



#run(add_many_users_tg(users_data=tg_users, dao=TgUserDAO))

#chats = [{'chat_id': 3, 'chat_name': 'new', 'users_count' : 5}]
#run(add_many_users_tg_chat(users_data=chats))