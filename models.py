from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, ForeignKeyConstraint, Text, Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sql_enums import VkActionEnum, TgActionEnum, FamilyStatusEnum, GenderEnum

class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  vk_id: Mapped[str] = mapped_column(ForeignKey('vk_users_last.vk_id'))
  tg_id: Mapped[str] = mapped_column(ForeignKey('tg_users_last.tg_id'))

class VkUser(Base):
  __tablename__ = 'vk_users_last'

  vk_id: Mapped[str] = mapped_column(primary_key=True)
  first_name: Mapped[str]
  last_name: Mapped[str]
  gender: Mapped[GenderEnum]
  birth_date: Mapped[datetime | None]
  city: Mapped[str | None]
  education: Mapped[str | None]
  work_place: Mapped[str | None]
  status: Mapped[str | None]
  family_status: Mapped[FamilyStatusEnum]
  friends: Mapped[list[int]] = mapped_column(ARRAY(Integer))
  groups: Mapped[list[str]] = mapped_column(ARRAY(String))

class VkUserHist(Base):
  __tablename__ = 'vk_users_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  vk_id: Mapped[str]
  first_name: Mapped[str]
  last_name: Mapped[str]
  gender: Mapped[GenderEnum]
  birth_date: Mapped[datetime | None]
  city: Mapped[str | None]
  education: Mapped[str | None]
  work_place: Mapped[str | None]
  status: Mapped[str | None]
  family_status: Mapped[FamilyStatusEnum]
  friends: Mapped[list[int]] = mapped_column(ARRAY(Integer))
  groups: Mapped[list[str]] = mapped_column(ARRAY(String))


class VkInteraction(Base):
  __tablename__ = 'vk_interactions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  post_id: Mapped[int] = mapped_column(ForeignKey('vk_posts_last.post_id'))
  action: Mapped[VkActionEnum]
  action_from: Mapped[str] = mapped_column(ForeignKey('vk_users_last.vk_id'))
  action_to: Mapped[str | None] = mapped_column(ForeignKey('vk_users_last.vk_id'))
  text: Mapped[str | None] = mapped_column(Text)
  time: Mapped[datetime]

class Post(Base):
  __tablename__ = 'vk_posts_last'

  post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
  image: Mapped[str | None]
  music: Mapped[str | None]
  description: Mapped[str | None] = mapped_column(Text)
  posted_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

class PostHist(Base):
  __tablename__ = 'vk_posts_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  post_id: Mapped[int]
  image: Mapped[str | None]
  music: Mapped[str | None]
  description: Mapped[str | None] = mapped_column(Text)
  posted_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

class TgUser(Base):
  __tablename__ = 'tg_users_last'

  tg_id: Mapped[str] = mapped_column(primary_key=True)
  user_name: Mapped[str]
  first_name: Mapped[str]
  last_name: Mapped[str]
  last_online: Mapped[datetime]

class TgUserHist(Base):
  __tablename__ = 'tg_users_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  tg_id: Mapped[str]
  user_name: Mapped[str]
  first_name: Mapped[str]
  last_name: Mapped[str]
  last_online: Mapped[datetime]

class Chat(Base):
  __tablename__ = 'tg_chats_last'

  chat_id: Mapped[str] = mapped_column(primary_key=True)
  chat_name: Mapped[str]
  users_count: Mapped[int]

class ChatHist(Base):
  __tablename__ = 'tg_chats_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str]
  chat_name: Mapped[str]
  users_count: Mapped[int]

class TgStatistics(Base):
  __tablename__ = 'tg_statistics_last'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  reaction: Mapped[str]
  count: Mapped[int]

class TgStatisticsHist(Base):
  __tablename__ = 'tg_statistics_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  reaction: Mapped[str]
  count: Mapped[int]

class TgMessage(Base):
  __tablename__ = 'tg_messages'

  chat_id: Mapped[str] = mapped_column(ForeignKey('tg_chats_last.chat_id'), primary_key=True)
  id: Mapped[str] = mapped_column(primary_key=True)
  text: Mapped[str]
  statistics: Mapped[int] = mapped_column(ForeignKey('tg_statistics_last.id'))
  
class TgInteraction(Base):
  __tablename__ = 'tg_interactions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column(ForeignKey('tg_chats_last.chat_id'))
  action: Mapped[TgActionEnum]
  action_from: Mapped[str] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  action_to: Mapped[str | None] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  reply_on_chat_id: Mapped[str] = mapped_column()
  reply_on_id: Mapped[str] = mapped_column()
  message_chat_id: Mapped[str] = mapped_column()
  message_id: Mapped[str] = mapped_column()
  time: Mapped[datetime]

  __table_args__ = (
      ForeignKeyConstraint(
          ['reply_on_chat_id', 'reply_on_id'],
          ['tg_messages.chat_id', 'tg_messages.id']
      ),
      ForeignKeyConstraint(
          ['message_chat_id', 'message_id'],
          ['tg_messages.chat_id', 'tg_messages.id']
      ),
  )