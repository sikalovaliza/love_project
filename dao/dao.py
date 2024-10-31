from dao.base import BaseDAO
from models import User, VkUser, VkInteraction, Post, TgUser, Chat, TgInteraction


class UserDAO(BaseDAO):
    model = User

class VkUserDAO(BaseDAO):
    model = VkUser


class VkInteractionDAO(BaseDAO):
    model = VkInteraction


class PostDAO(BaseDAO):
    model = Post


class TgUserDAO(BaseDAO):
    model = TgUser


class ChatDAO(BaseDAO):
    model = Chat


class TgInteractionDAO(BaseDAO):
    model = TgInteraction