import asyncio
from datetime import datetime
from sqlalchemy import func, text
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import settings

DATABASE_URL = settings.get_db_url()
engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True 

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e 
            finally:
                await session.close()

    return wrapper

'''def trigger_to_hist_table(table_name_last: str, column_names: set):
    table_name_hist = table_name_last.replace('_last', '_hist')
    return text(f"""
                CREATE OR REPLACE TRIGGER {table_name_last}_to_hist_table
                BEFORE UPDATE ON {table_name_last}
                FOR EACH ROW
                BEGIN
                    INSERT INTO {table_name_hist} ({', '.join(column_names)})
                    VALUES ({', '.join(map(lambda item: 'OLD.' + item, column_names))});
                END;
                """)

async def create_triggers():
    async with engine.connect() as connection:
        all_tables = Base.metadata.tables
        # leave only table names where '_last' ends
        tables_name_last = [name for name in all_tables if '_last' in name]

        for name in tables_name_last:
            table = all_tables[name]
            columns = {column.name for column in table.columns} - {'id'}
            await connection.execute(trigger_to_hist_table(table_name_last=name, column_names=columns))

asyncio.run(create_triggers())'''