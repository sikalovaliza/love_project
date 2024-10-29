from datetime import datetime
from sqlalchemy import ForeignKey, Text, Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sql_enums import VkActionEnum, TgActionEnum

class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  vk_id: Mapped[int] = mapped_column(ForeignKey('vk_users.vk_id'))
  tg_id: Mapped[int] = mapped_column(ForeignKey('tg_users.tg_id'))

class VkUser(Base):
  __tablename__ = 'vk_users'

  vk_id: Mapped[int] = mapped_column(primary_key=True)
  full_name: Mapped[str]
  city: Mapped[str | None]
  education: Mapped[str | None]
  family_status: Mapped[str | None]
  friends: Mapped[list[int]] = mapped_column(ARRAY(Integer))
  groups: Mapped[list[str]] = mapped_column(ARRAY(String))

class VkInteraction(Base):
  __tablename__ = 'vk_interactions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  post_id: Mapped[int] = mapped_column(ForeignKey('posts.post_id'))
  action: Mapped[VkActionEnum]
  action_from: Mapped[int] = mapped_column(ForeignKey('vk_users.vk_id'))
  action_to: Mapped[int | None] = mapped_column(ForeignKey('vk_users.vk_id'))
  text: Mapped[str | None] = mapped_column(Text)
  time: Mapped[datetime]

class Post(Base):
  __tablename__ = 'posts'

  post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
  image: Mapped[str | None]
  music: Mapped[str | None]
  description: Mapped[str | None] = mapped_column(Text)
  posted_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

class TgUser(Base):
  __tablename__ = 'tg_users'

  tg_id: Mapped[int] = mapped_column(primary_key=True)
  user_name: Mapped[str]

class Chat(Base):
  __tablename__ = 'chats'

  chat_id: Mapped[int] = mapped_column(primary_key=True)
  chat_name: Mapped[str]
  users_count: Mapped[int]

class TgInteraction(Base):
  __tablename__ = 'tg_interactions'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[int] = mapped_column(ForeignKey('chats.chat_id'))
  action: Mapped[TgActionEnum]
  action_from: Mapped[int] = mapped_column(ForeignKey('tg_users.tg_id'))
  action_to: Mapped[int | None] = mapped_column(ForeignKey('tg_users.tg_id'))
  time: Mapped[datetime]
  text: Mapped[str | None] = mapped_column(Text)