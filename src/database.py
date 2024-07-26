import asyncio
from typing import Annotated
from sqlalchemy import URL, String, create_engine, text
from config import setting
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

engin = create_engine(
    url=setting.DB_URL_psycopg,
    echo=True,
)

async_engin = create_async_engine(
    url=setting.DB_URL_asyncpg,
    echo=False,
)

session = sessionmaker(engin)
async_session = async_sessionmaker(async_engin)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    # def __repr__(self):                         #текущее определение позволяет полчать в выгрузке ВСЮ конкретную информацию об обьекте
    #     """Relationship не используется в repr() т.к. могут привести к неожиданным подгрузкам"""
    #     cols = [f'{i}={getattr(self, i)}' for i in self.__table__.columns.keys()]
    #     return f"<{self.__class__.__name__}> {', '.join(cols)}"

    def __repr__(self):                         #текущее определение позволяет полчать в выгрузке ВСЮ конкретную информацию об обьекте
        """Relationship не используется в repr() т.к. могут привести к неожиданным подгрузкам"""
        cols = [f'{j}={getattr(self, j)}' for i,j in enumerate(self.__table__.columns.keys()) if j in self.repr_cols or i < self.repr_cols_num]
        return f"<{self.__class__.__name__}> {', '.join(cols)}"

# async def get_123():  # рабочий контекстный менеджер!!
#     async with async_engin.connect() as start:
#         res = await start.execute(text("SELECT 1,2,3 union select 4,5,6"))
#         print(f"{res.all()=}")


# asyncio.run(get_123())


# with engin.connect() as start: #рабочий контекстный менеджер # лучше использовать коннект (хотя можно и бегин) для вызова метода commit врукчную
#     res = start.execute(text("SELECT 1,2,3 union select 4,5,6"))
#     print(f"{res.all()=}")
#     start.commit()
