from sqlalchemy import Enum, create_engine, Column, Integer, String, ForeignKey, Text, DateTime, ARRAY
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class VkActionEnum(enum.Enum):
    like = "like"
    comment = "comment"


class TgActionEnum(enum.Enum):
    tag = "tag"
    react = "react"
    message = "message"
    add_user = "add_user"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey('vk_users.vk_id'))
    tg_id = Column(Integer, ForeignKey('tg_users.tg_id'))

class VkUser(Base):
    __tablename__ = 'vk_users'
    
    vk_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    city = Column(String)
    education = Column(String)
    family_status = Column(String)
    friends = Column(ARRAY(Integer))
    groups = Column(ARRAY(String))

class VkInteraction(Base):
    __tablename__ = 'vk_interactions'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    action = Column(Enum(VkActionEnum))
    action_from = Column(Integer, ForeignKey('vk_users.vk_id'))
    action_to = Column(Integer, ForeignKey('vk_users.vk_id'))
    text = Column(Text)
    time = Column(DateTime)

class Post(Base):
    __tablename__ = 'posts'
    
    post_id = Column(Integer, primary_key=True)
    image = Column(String)
    music = Column(String)
    posted_by = Column(Integer, ForeignKey('users.id'))

class TgUser(Base):
    __tablename__ = 'tg_users'
    
    tg_id = Column(Integer, primary_key=True)
    user_name = Column(String)

class Chat(Base):
    __tablename__ = 'chats'
    
    chat_id = Column(Integer, primary_key=True)
    chat_name = Column(String)
    users_count = Column(Integer)

class TgInteraction(Base):
    __tablename__ = 'tg_interactions'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    action = Column(Enum(TgActionEnum))
    action_from = Column(Integer, ForeignKey('tg_users.tg_id'))
    action_to = Column(Integer, ForeignKey('tg_users.tg_id'))
    time = Column(DateTime)
    text = Column(Text)

def create_database(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)