from turtle import end_fill
from sqlalchemy import text, insert, select, update
from database import engin, async_engin
from sqlalchemy.ext.asyncio import create_async_engine
from queries.models import meta, workers_table, Workload, resumes_table


def get_123_sync():
    with engin.connect() as start:  # рабочий контекстный менеджер # лучше использовать коннект (хотя можно и бегин) для вызова метода commit врукчную
        res = start.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}")
        start.commit()


async def get_123():  # рабочий контекстный менеджер!!
    async with async_engin.connect() as start:
        res = await start.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}")


class Work_Table():
    @staticmethod
    def create_table():
        engin.echo = False  # отключаем логи на период дропа таблиц
        meta.drop_all(engin)
        meta.create_all(engin)
        engin.echo = True

    @staticmethod
    def insert_data():
        with engin.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES #сырой SQL запрос
            #         ('Bobr'),
            #         ('VOLK');"""
            stmt = insert(workers_table).values(  # запрос через queri-bilder
                [
                    {"username": "LIS"},
                    {"username": "Bobr"}
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with engin.connect() as conn:
            qery = select(workers_table)  # SELECT * FROM workers
            # возвращает специальный итератор с методами .all .one_or_none . first и.т.д
            result = conn.execute(qery)
            workers = result.all()
            print(f'{workers=}')

    @staticmethod
    def update_workers(item: int = 2, new_username: str = "SLON"):
        with engin.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:ID")  сырой запрос
            # stmt = stmt.bindparams(username=new_username, ID=item)
            stmt = (
                update(workers_table)
                .values(username = new_username)
                #.where(workers_table.c.worker_id==item)
                .filter_by(worker_id=item)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod        
    def insert_resumes():
        with engin.connect() as conn:
            resumes = [
                {"title": "Python Junior Developer", "price": 50000, "workload": Workload.fulltime, "worker_id": 1},
                {"title": "Python Разработчик", "price": 150000, "workload": Workload.fulltime, "worker_id": 1},
                {"title": "Python Data Engineer", "price": 250000, "workload": Workload.parttime, "worker_id": 2},
                {"title": "Data Scientist", "price": 300000, "workload": Workload.fulltime, "worker_id": 2},
            ]
            stmt = insert(resumes_table).values(resumes)
            conn.execute(stmt)
            conn.commit()
    