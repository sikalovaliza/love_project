import nltk
from rake_nltk import Rake
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from asyncio import run
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
from database import connection
import torch
import numpy as np
from tqdm import tqdm
from dao.dao import TgStatisticsDAO, UserDAO, VkUserDAO, VkActionDAO, VkPostDAO, TgUserDAO, TgGroupStatsDAO, TgUserGroupActionDAO, TgStatisticsDAO, TgGroupMessageDAO, TgChannelStatsDAO 

@connection
async def select_all_tg_messages_by_user(session):
    user_id = '4850058'
    res = await TgUserGroupActionDAO.get_messages_with_time(session, action_from=user_id, window='month')
    if not res:
        return 'not found', None
    
    messages = []
    time = []
    for item in res:
        message = await TgGroupMessageDAO.get_all(session, id=item.message_id, chat_id=item.message_chat_id)
        messages.append(message[0].text)
        time.append(item.month)
    return messages, time

def get_main_words_analytics(messages, time, rake_nltk_var):
    i = 1
    res = []
    print(len(time))
    while i < len(time):
        text = messages[i - 1]
        while i < len(time) and time[i-1] == time[i]:
            text = text + ' ' + messages[i]
            i += 1
        rake_nltk_var.extract_keywords_from_text(text)
        keywords_with_scores = rake_nltk_var.get_ranked_phrases_with_scores()
        text = ''
        for score, key in keywords_with_scores:
            text = text.lower() + ' ' + key
        res.append([text, time[i-1]])
        print(i)

        i+=1

    return res

nltk.download('stopwords')
rake_nltk_var = Rake(language='russian')
messages, time = run(select_all_tg_messages_by_user())
res = get_main_words_analytics(messages[:100], time[:100], rake_nltk_var)
love_words = [
    "Любовь", "Нежность", "Страсть", "Сердце", "Мечты", "Забота", "Романтика",
    "Объятия", "Поцелуи", "Доверие", "Счастье", "Радость", "Вдохновение", "Улыбка",
    "Связь", "Тепло", "Взаимопонимание", "Единство", "Привязанность", "Очарование",
    "Эмоции", "Искренность", "Влюбленность", "Нежный", "Моя любовь", "Ты моя судьба",
    "Дорогой", "Дорогая", "Сладкий", "Чувства", "Душа", "Сердечный", "Уют", 
    "Секреты", "Воспоминания", "Подарки", "Совершенство", "Партнёрство", 
    "Поддержка", "Вера", "Надежда", "Слияние", "Ласка", "Понимание", 
    "Забавы", "Близость", "Жизнь вместе", "Мечтать о тебе", "Признание",
    "Совместные моменты", "Радость быть вместе", "Трепет", "Тоска по тебе",
    "Нежно обнять", "Защита", "Открытость", "Взаимная симпатия",
    "Долгожданный момент", "Влюблённые глаза", "Сердечные чувства",
    "Безумие любви", "Глубокие чувства", "Обожание", "Счастливые моменты",
    "Ощущение полноты жизни", "Уважение", "Интимность",
    "Стремление быть рядом", "Любовное письмо", "Флирт",
    "Вдохновение от тебя", "Романтический вечер",
    "Параллели душ", "Завораживающее чувство", 
    "Нежные слова", "Чувственное прикосновение",
    "Вместе навсегда", "Счастливое будущее",
    "Взаимная любовь", "Понимание без слов",
    "Лунная ночь с тобой", "Песни о любви",
    "Секреты любви ", "Клятва верности ",
    "Романтические прогулки ",
    "Моменты счастья", "Любовь с первого взгляда",
    "Объединение сердец", "Долгожданная встреча", "люблю", "лю", "Дорогой", 
    "Дорогая", "Любимый", "Любимая", "Солнышко", "Зайчик", "Котик",
    "Киска", "Малыш", "Малышка", "Сердечко", "Ласточка", "Птичка", "Сладкий",
    "Сладкая", "Звёздочка", "Моя радость", "Моя жизнь", "Душа моя", 
    "Светик", "Нежный", "Нежная", "Красавчик", "Красавица", "Чудо",
    "Сердечный", "Моя любовь", "Солнце моё", "Родной", "Родная",
    "Золотце", "Люба", "Любушка", "Моя прелесть", "Сердечко моё",
    "Котёнок", "Зайчонок", "Моя звезда", "Свет мой", "Лютик",
    "Пупсик", "Пупсик мой", "Душенька", "Моя мечта", 
    "Нежность моя", "Счастье моё", "Тигрёнок", "Левушка",
    "Крошка", "Моя радость", "Котенок"
]
for text, time in res:
    count = 0
    for word in love_words:
        if word in text:
            count += 1
    if count >= 3:
        print('Влюблён')
    else:
        print('Не влюблён')