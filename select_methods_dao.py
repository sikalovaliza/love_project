import csv
from dao.dao import TgStatisticsDAO, UserDAO, VkUserDAO, VkActionDAO, VkPostDAO, TgUserDAO, TgGroupStatsDAO, TgUserGroupActionDAO, TgStatisticsDAO, TgGroupMessageDAO, TgChannelStatsDAO 
from database import connection
from asyncio import run
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sql_enums import VkActionEnum, TgActionEnum, FamilyStatusEnum, GenderEnum

import nltk
from rake_nltk import Rake

@connection
async def select_all_tg_users(session):
    res = await TgUserGroupActionDAO.get_all(session)
    if not res:
        return 'not found', None
    users = set()
    for item in res:
        users.add(item.action_from)
    return users

@connection
async def select_all_tg_messages_by_user(session):
    user = '4850058'
    res = await TgUserGroupActionDAO.get_all(session, action_from=user, action=TgActionEnum.message)
    if not res:
        return 'not found', None

    messages =[]
    time = []
    for item in res:
        message = await TgGroupMessageDAO.get_all(session, id=item.message_id, chat_id=item.message_chat_id)
        messages.append(message)
        time.append(item.time)
    return messages, time

@connection
async def tg_user_mentioned_in(session):
    user_id = '4850058'
    user = await TgUserDAO.get_all(session, tg_id=user_id)
    res = await TgUserGroupActionDAO.get_all(session, action=TgActionEnum.message)
    if not res:
        return 'not found', None
    
    res = []
    for item in res:
        message = await TgGroupMessageDAO.get_all(session, id=item.message_id, chat_id=item.message_chat_id)
        if user.user_name in message[0].text:
            res.append({'from_user': item.action_from, 'text': message[0].text, 'mentioned': user.user_id, 'time': item.time})
    return res

filename = 'messages.csv'
all_messages, time = run(select_all_tg_messages_by_user())

nltk.download('stopwords')

text = all_messages[0][0].text
print(text)
rake_nltk_var = Rake(language='russian')
rake_nltk_var.extract_keywords_from_text(text)
keywords_with_scores = rake_nltk_var.get_ranked_phrases_with_scores()

for score, keyword in keywords_with_scores:
    print(f"Ключевое слово: {keyword}, Рейтинг: {score}")
