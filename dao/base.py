from typing import List, Any, Dict
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sql_enums import TgActionEnum

class BaseDAO:
    model = None
    history_model = None

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        # Добавить несколько записей
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances
    
    @classmethod
    async def get_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        records = result.scalars().all()
        return records
    
    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_value: Any):
        query = select(cls.model).filter(cls.model.id == id_value)  # Предполагается, что поле id существует
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def aggregate_user_activity(cls, session: AsyncSession, action_from: str, window = 'week'):
        query = (
            select(
                func.count(cls.model.id).label('count'),
                func.date_trunc(window, cls.model.time).label(window)
            )
            .filter(cls.model.action_from == action_from)
            .group_by(window)
            .order_by(window)
        )

        result = await session.execute(query)
        aggregated_records = result.all()

        return aggregated_records
    
    @classmethod
    async def get_messages_with_time(cls, session: AsyncSession, action_from: str, window = 'week'):
        query = (
            select(
                cls.model.message_id,
                cls.model.message_chat_id,
                func.date_trunc(window, cls.model.time).label(window)
            )
            .filter(
                cls.model.action_from == action_from,
                or_(cls.model.action == TgActionEnum.message, cls.model.action == TgActionEnum.reply)
            )
            .group_by(window, cls.model.message_id, cls.model.message_chat_id)
            .order_by(window)
        )

        result = await session.execute(query)
        messages = result.all()

        return messages
