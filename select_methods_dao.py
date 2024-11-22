from dao.dao import TgMessageDAO, TgStatisticsDAO, UserDAO, VkUserDAO, VkActionDAO, VkPostDAO, TgUserDAO, TgGroupStatsDAO, TgUserGroupActionDAO, TgStatisticsDAO, TgGroupMessageDAO, TgChannelStatsDAO
from database import connection
from asyncio import run
@connection
async def select_all_vk_users(session):
    # после session можно передать параметры фильтрации
    # Например, VkUserDAO.get_all(session, city='Москва') <=> SELECT * FROM vk_users WHERE city='Москва'
    res = await VkUserDAO.get_all(session)
    if res:
        return res
    return 'not found'

all_users = run(select_all_vk_users())
for i in all_users:
    print(i.to_dict())
