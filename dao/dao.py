from dao.base import BaseDAO
from models import TgGroupMessage, TgStatistics, User, VkUser, VkAction, VkPost, TgUser, TgGroupStats, TgChannelStats, TgUserGroupAction


class UserDAO(BaseDAO):
    model = User

class VkUserDAO(BaseDAO):
    model = VkUser

class VkActionDAO(BaseDAO):
    model = VkAction

class VkPostDAO(BaseDAO):
    model = VkPost

class TgUserDAO(BaseDAO):
    model = TgUser

class TgGroupStatsDAO(BaseDAO):
    model = TgGroupStats

class TgUserGroupActionDAO(BaseDAO):
    model = TgUserGroupAction

class TgStatisticsDAO(BaseDAO):
    model = TgStatistics
    
class TgGroupMessageDAO(BaseDAO):
    model = TgGroupMessage

class TgChannelStatsDAO(BaseDAO):
    model = TgChannelStats