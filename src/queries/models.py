import datetime
from typing import Annotated
from sqlalchemy import TIMESTAMP, CheckConstraint, Enum, ForeignKey, Index, PrimaryKeyConstraint, Table, Column, Integer, String, MetaData, func, text
from database import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column, relationship 
import enum


# добавление Аннотации для сокращения кода (!)
intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]

updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)]


class WorkersORM(Base):  # декларативный стиль создание таблиц
    __tablename__ = "workers"
    # intpk применяется здесь для сокращения кода (!)
    worker_id: Mapped[intpk]
    username: Mapped[str]

    # resumes:Mapped[list["ResumesORM"]] = relationship(
    #     back_populates="worker",        #явное создание связи между таблицами. Наличие синтаксиса необходимо в каждой связанной таблице
    #       # backref="worker",                   #неявное создание связи. Автоматически "создает" ситаксис для обратной связи в связуемой таблице (НЕ РЕКОМЕНДУЕТСЯ (ПО ДОКУМЕНТАЦИИ))
    # )

    # best_resumes:Mapped[list["ResumesORM"]] = relationship(
    #     back_populates="worker",        #явное создание связи между таблицами. Наличие синтаксиса необходимо в каждой связанной таблице
    #     primaryjoin= "and_(WorkersORM.worker_id == ResumesORM.worker_id, ResumesORM.workload == 'parttime')" ,  # backref="worker",   #неявное создание связи. Автоматически "создает" ситаксис для обратной связи в связуемой таблице (НЕ РЕКОМЕНДУЕТСЯ (ПО ДОКУМЕНТАЦИИ))
    #     order_by="ResumesORM.ID.desc()",        #lazy="selectin" Неявная установка метода подгрузки (orm.select_wokers_with_reletionship() строка с .options(selectinload(WorkersORM.best_resumes)) становится ненужна)
        
    # )

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesORM(Base):
    __tablename__ = "resume"
    ID: Mapped[intpk]
    title: Mapped[str_256]
    price: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int | None] = mapped_column(
        ForeignKey("workers.worker_id", ondelete="CASCADE"))   #РК и FК рекомендуется оставлять рядом с значениями столбцов
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at] # (!)

    # worker:Mapped["WorkersORM"] = relationship(
    #     back_populates="resumes",
    # )

    # repr_cols_num = 4
    # repr_cols = ("updated_at",)

    # __table_args__ = (             #Индексы и ограничения лучше задавать здесь
    #     Index("title_index", "title"),           #название индекса, через запятую индексируемые стобцы 
    #     CheckConstraint("price > 0", name="chek_price_positiv"),
    #     PrimaryKeyConstraint("ID", "title")          #возможность добавить РК 
    # )


meta = MetaData()

workers_table = Table(  # обьявление таблицы через императивный стиль
    "workers",
    meta,
    Column('worker_id', Integer, primary_key=True),  #Если изменить название столбцов, дальнейшая работоспособность не гарантирована...
    Column("username", String)
)
resumes_table = Table(
    "resumes",
    meta,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("workers.worker_id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow),
)