import enum
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dao.dao import TgStatisticsDAO, UserDAO, VkUserDAO, VkActionDAO, VkPostDAO, TgUserDAO, TgGroupStatsDAO, TgUserGroupActionDAO, TgStatisticsDAO, TgGroupMessageDAO, TgChannelStatsDAO 
from database import connection
from asyncio import run
from sql_enums import VkActionEnum, TgActionEnum, FamilyStatusEnum, GenderEnum

class ActivityChange(enum.Enum):
    increased = 'увеличилась'
    no_changes = 'не изменилась'
    decreased = 'уменьшилась'

@connection
async def user_activity_aggregation(session):
    user = '4850058'
    agg_activity = await TgUserGroupActionDAO.aggregate_user_activity(session, action_from=user, window='week')
    if not agg_activity:
        return 'not found', None

    return agg_activity

def detect_anomaly_activity(agg_activity, periods_num):
    first_period_num = 0 if periods_num > len(agg_activity) else -(periods_num+1)
    activity = np.array(agg_activity[first_period_num:][:-1])[:,0]
    mean_activity = np.mean(activity)
    if agg_activity[-1:][0][0] > mean_activity:
        return ActivityChange.increased
    elif agg_activity[-1:][0][0] < mean_activity:
        return ActivityChange.decreased

    return ActivityChange.no_changes


agg_activity = run(user_activity_aggregation())
for count, week in agg_activity:
    print(count, week)
detected_anomaly = detect_anomaly_activity(agg_activity, 2)
print('Активность', detected_anomaly.value)