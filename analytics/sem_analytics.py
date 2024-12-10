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

tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment')
model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment', return_dict=True)
def process_sentiment_analysis(texts, model, batch_size=16, device='cpu') -> np.array:
  sentiments = []
  model = model.to(device)

  with torch.no_grad():
      for i in tqdm(range(0, len(texts), batch_size)):
          batch = texts[i:i+batch_size]
          try:
              inputs = tokenizer(batch, max_length=512, padding=True, truncation=True, return_tensors='pt').to(device)
          except:
              print(batch)
              break
          outputs = model(**inputs)
          predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
          predicted = torch.argmax(predicted, dim=1).cpu().numpy()
          sentiments.append(predicted)

  sentiments = np.concatenate(sentiments)

  return sentiments

def sentiment_analytics(sentiments):
  answer = {}

  mask_positive = sentiments == 1
  mask_negative = sentiments == 2
  mask_neutral = sentiments == 0

  cnt_positive = np.sum(mask_positive)
  cnt_negative = np.sum(mask_negative)
  cnt_neutral = np.sum(mask_neutral)

  answer['positive'] = cnt_positive
  answer['negative'] = cnt_negative
  answer['neutral'] = cnt_neutral

  max_key = max(answer, key=answer.get)

  return max_key     

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

def get_sem_analytics(messages, time):
    i = 1
    res = []
    print(len(time))
    while i < len(time):
        texts = [messages[i - 1]]
        while i < len(time) and time[i-1] == time[i]:
            texts.append(messages[i])
            i += 1
        sentiments = process_sentiment_analysis(texts, model, batch_size=16, device=device) 
        answer = sentiment_analytics(sentiments=sentiments)
        res.append([answer, time[i-1]])
        texts.clear()
        i += 1
        print(i)

    print(res)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
messages, time = run(select_all_tg_messages_by_user())
get_sem_analytics(messages[:200], time[:200])