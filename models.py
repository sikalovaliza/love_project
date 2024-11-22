from datetime import datetime
from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey, ForeignKeyConstraint, Text, Integer, String, ARRAY
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
  birth_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
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
  birth_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
  city: Mapped[str | None]
  education: Mapped[str | None]
  work_place: Mapped[str | None]
  status: Mapped[str | None]
  family_status: Mapped[FamilyStatusEnum]
  friends: Mapped[list[int]] = mapped_column(ARRAY(Integer))
  groups: Mapped[list[str]] = mapped_column(ARRAY(String))


class VkAction(Base):
  __tablename__ = 'vk_actions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  post_id: Mapped[int] = mapped_column(ForeignKey('vk_posts_last.post_id'))
  action: Mapped[VkActionEnum]
  action_from: Mapped[str] = mapped_column(ForeignKey('vk_users_last.vk_id'))
  action_to: Mapped[str | None] = mapped_column(ForeignKey('vk_users_last.vk_id'))
  text: Mapped[str | None] = mapped_column(Text)
  time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class VkPost(Base):
  __tablename__ = 'vk_posts_last'

  post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
  image: Mapped[str | None]
  music: Mapped[str | None]
  description: Mapped[str | None] = mapped_column(Text)
  posted_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

class VkPostHist(Base):
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
  last_online: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class TgUserHist(Base):
  __tablename__ = 'tg_users_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  tg_id: Mapped[str]
  user_name: Mapped[str]
  first_name: Mapped[str]
  last_name: Mapped[str]
  last_online: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class TgChannelStats(Base):
  __tablename__ = 'tg_channels_stats_last'

  chat_id: Mapped[str] = mapped_column(primary_key=True)
  chat_name: Mapped[str]
  users_count: Mapped[int]
  description: Mapped[str] = mapped_column(Text)
  is_verified: Mapped[bool]

class TgChannelStatsHist(Base):
  __tablename__ = 'tg_channels_stats_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str]
  chat_name: Mapped[str]
  users_count: Mapped[int]
  is_verified: Mapped[bool]

class TgGroupStats(Base):
  __tablename__ = 'tg_groups_stats_last'

  chat_id: Mapped[str] = mapped_column(primary_key=True)
  chat_name: Mapped[str]
  users_count: Mapped[int]

class TgGroupStatsHist(Base):
  __tablename__ = 'tg_groups_stats_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str]
  chat_name: Mapped[str]
  users_count: Mapped[int]


class TgStatistics(Base):
  __tablename__ = 'tg_statistics_last'
  
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  reaction_count: Mapped[dict] = mapped_column(JSON)
 
class TgStatisticsHist(Base):
  __tablename__ = 'tg_statistics_hist'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  reaction_count: Mapped[dict] = mapped_column(JSON)

class TgGroupMessage(Base):
  __tablename__ = 'tg_groups_messages'

  id: Mapped[str] = mapped_column(primary_key=True)
  text: Mapped[str] = mapped_column(Text)
  statistics: Mapped[int] = mapped_column(ForeignKey('tg_statistics_last.id'))
  
class TgUserGroupAction(Base):
  __tablename__ = 'tg_users_groups_actions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column(ForeignKey('tg_groups_stats_last.chat_id'))
  action: Mapped[TgActionEnum]
  action_from: Mapped[str] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  action_to: Mapped[str | None] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  reply_on: Mapped[int | None] = mapped_column(ForeignKey('tg_groups_messages.id'))
  message_id: Mapped[int | None] = mapped_column(ForeignKey('tg_groups_messages.id'))
  time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

'''
class TgStatistics(Base):
  __tablename__ = 'tg_statistics_last'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column()
  message_id: Mapped[str] = mapped_column()
  reaction: Mapped[str]
  count: Mapped[int]
  __table_args__ = (
      ForeignKeyConstraint(
          ['chat_id', 'message_id'],
          ['tg_groups_messages.chat_id', 'tg_groups_messages.id']
      ),
  )
  

class TgStatisticsHist(Base):
  __tablename__ = 'tg_statistics_hist'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column()
  message_id: Mapped[str] = mapped_column()
  reaction: Mapped[str]
  count: Mapped[int]
  __table_args__ = (
      ForeignKeyConstraint(
          ['chat_id', 'message_id'],
          ['tg_groups_messages.chat_id', 'tg_groups_messages.id']
      ),
  )


class TgGroupMessage(Base):
  __tablename__ = 'tg_groups_messages'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column()
  message_id: Mapped[str] = mapped_column()
  text: Mapped[str] = mapped_column(Text)
  __table_args__ = (
      ForeignKeyConstraint(
          ['chat_id', 'message_id'],
          ['tg_users_groups_actions.chat_id', 'tg_users_groups_actions.reply_on_id']
      ),
      ForeignKeyConstraint(
          ['chat_id', 'message_id'],
          ['tg_users_groups_actions.chat_id', 'tg_users_groups_actions.message_id']
      ),
  )
  
  
class TgUserGroupAction(Base):
  __tablename__ = 'tg_users_groups_actions'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  chat_id: Mapped[str] = mapped_column(ForeignKey('tg_groups_stats_last.chat_id'))
  action: Mapped[TgActionEnum]
  action_from: Mapped[str] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  action_to: Mapped[str | None] = mapped_column(ForeignKey('tg_users_last.tg_id'))
  reply_on_id: Mapped[str | None] = mapped_column()
  message_id: Mapped[str | None] = mapped_column()
  time: Mapped[datetime] = mapped_column(DateTime(timezone=True))'''