from turtle import title
from unittest import result
from sqlalchemy import Integer, and_, cast, func, select, text, insert
from database import engin, async_engin, session, Base
from queries.models import VacansiORM, WorkersORM, ResumesORM
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from schemas import DTO_select, ResumeRelVacansisRelDTO, WorkersGetDTO, WorkersRelDTO

class Work_Table_ORM():
    @staticmethod
    def create_table():
        engin.echo = True  # отключаем логи на период дропа таблиц
        Base.metadata.drop_all(engin)
        Base.metadata.create_all(engin)
        engin.echo = False

    @staticmethod
    def insert_data():
        with session() as ses:
            worker_volk = WorkersORM(username="VOLK")
            worker_bobr = WorkersORM(username="BOBR")
            ses.add_all((worker_bobr, worker_volk))
            ses.commit()

    @staticmethod
    def select_workers():
        with session() as ses:
            qery = select(WorkersORM)
            result = ses.execute(qery)
            workers = result.scalars().all()
            print()
            return f'{workers=}'

    @staticmethod
    def update_workers(item: int = 2, new_username: str = "AIST"):
        with session() as ses:
            animal_Bobr = ses.get(WorkersORM, item)
            animal_Bobr.username = new_username
            # ses.expire(animal_Bobr) #отмена всех изменений для конкретного обьекта expire_all для всех обьектов
            ses.commit()

    @staticmethod
    def insert_resum():
        with session() as ses:
            worker_volk = ResumesORM(title='Python junior', price=50_000, workload='fulltime', worker_id=1)
            worker_volk2 = ResumesORM(title='Python разработчик', price=100_000, workload='fulltime', worker_id=1)
            worker_volk1 = ResumesORM(title='Python midle', price=150_000, workload='parttime', worker_id=2)
            worker_bobr = ResumesORM(title='Архитектор БД', price=250_000, workload='fulltime', worker_id=2)
            ses.add_all((worker_volk, worker_volk1, worker_volk2, worker_bobr))
            ses.commit()
    """
    select workload, avg(price)::int as avg_price from resume 
    where title like '%Python%' and price >= 100_000
    group by workload
    """

    @staticmethod
    def select_avg_price(like_lng: str = 'Python'):
        with session() as ses:
            query = (
                select(
                    ResumesORM.workload,
                    cast(func.avg(ResumesORM.price),
                         Integer).label("avg_price")
                )
                # сообщаем из какой таблицы делаем запрос
                .select_from(ResumesORM)
                .filter(and_(
                    ResumesORM.title.contains(like_lng),
                    ResumesORM.price > 40_000
                ))  # .filter_by(id = 1, price >= 40_000) принимает конкретные значения конкретных столбцов
                .group_by(ResumesORM.workload)
                # .having(cast(func.avg(ResumesORM.price), Integer) > 70_000)
            )
            # print(query)
            # print(query.compile(compile_kwargs={"literal_binds": True}))      #такой же запрос с уточненными именами переменных в запросе
            # res = ses.execute(query)
            # result = res.all()
            # print(result[0].avg_price)                                         #извлекаем данные из запроса
    
    @staticmethod
    def insert_additional_resumes():
        with session() as ses:
            workers = [
                {"username": "LIS"},  # id 3
                {"username": "EJ"},  # id 4
                {"username": "OREL"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "price": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "price": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "price": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "price": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "price": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(WorkersORM).values(workers)
            insert_resumes = insert(ResumesORM).values(resumes)
            ses.execute(insert_workers)
            ses.execute(insert_resumes)
            ses.commit()

    @staticmethod
    def join_and_sort(like_lng:str = 'Python'):
        with session() as ses:
            """with helper_2 as (
                    select *, price-avg_price as price_diff
                        from
                    (select
                        w.worker_id,
                        w.username,
                        r.price,
                        r.workload,
                        avg(r.price) over (PARTITION BY workload):: int as avg_price
                    from resume r
                    join workers w on r.worker_id = w.worker_id) helper_1
                    )
                select * from helper_2 
                order by price_diff
            """
            r = aliased(ResumesORM)
            w = aliased(WorkersORM)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.price).over(partition_by=r.workload).cast(Integer).label('avg_price')  #аналог avg(r.price) over (PARTITION BY workload):: int as avg_price
                    ) 
                .join(r, r.worker_id == w.worker_id).subquery("helper1")             #По умолчанию иннерджоин. Если нужен фулл - full=True, если нужен лефтджоин isouter=True
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.price,
                    subq.c.workload,
                    subq.c.avg_price,
                    (subq.c.price - subq.c.avg_price).label("price_diff"),
                )
                .cte("helper2")
            )
            q = (
                select(cte)
                .order_by(cte.c.price_diff.desc())
            )
            # print(q.compile(compile_kwargs={"literal_binds": True}))
            res = ses.execute(q)
            result = res.all()
            print(f"{result=}")
    
    @staticmethod
    def select_workers_with_lazy_relationship():
        with session() as ses:
            q = (
                select(WorkersORM)
            )
            res = ses.execute(q)
            result = res.scalars().all()
            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)
            #для ленивой загрузги, характерна проблема n+1. Когда для одного запроса (q) будет выполнено n запросов (по колличеству строк)

    @staticmethod
    def select_workers_with_joined_relationship():
        with session() as ses:
            q = (
                select(WorkersORM)
                .options(joinedload(WorkersORM.resumes))         #joinedload не очень подходит для один-ко-многим. Лучшее применение один-к-одному или много-к-одгному
            )
            res = ses.execute(q)
            result = res.unique().scalars().all()       #unique запрос на уровне питона(алхимии) оставлят только уникальные первичные ключи

            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)
 
    @staticmethod
    def select_workers_with_selectin_relationship():
        with session() as ses:
            q = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.resumes))         #selectinload Лучшее применение многие-к-многим и один-ко-многим
            )
            res = ses.execute(q)
            result = res.unique().scalars().all()       #unique запрос на уровне питона(алхимии) оставлят только уникальные первичные ключи

            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)
    
    @staticmethod
    def select_wokers_with_reletionship():
        with session() as ses:
            query = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.best_resumes))
            )
            res = ses.execute(query)
            result = res.all()
            print(f"{result=}")

    @staticmethod
    def select_wokers_with_reletionship_contains_eager():           #contains_eager выгружает ТОЛЬКО строки с наличием ResumesORM.workload == 'parttime'
        with session() as ses:
            query = (
                select(WorkersORM)
                .join(WorkersORM.resumes)
                .options(contains_eager(WorkersORM.resumes))
                .filter(ResumesORM.workload == 'parttime')
            )
            res = ses.execute(query)
            result = res.unique().all()
            print(f"{result=}")
        return result
    
    @staticmethod
    def easy_select():
        with session() as ses:
            query = (
                select(WorkersORM)
                .limit(2)
            )

            res = ses.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [WorkersGetDTO.model_validate(i, from_attributes=True) for i in result_orm]
            print(f"{result_dto=}")

    @staticmethod
    def hard_select():
        with session() as ses:
            query = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.resumes))
                .limit(2)
            )

            res = ses.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [WorkersRelDTO.model_validate(i, from_attributes=True) for i in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    def DTO_select():
        with session() as ses:
            query = (
                select(
                    ResumesORM.workload,
                    cast(func.avg(ResumesORM.price),
                         Integer).label("avg_price")
                )
                # сообщаем из какой таблицы делаем запрос
                .select_from(ResumesORM)
                .filter(and_(
                    ResumesORM.title.contains("Python"),
                    ResumesORM.price > 40_000
                ))  # .filter_by(id = 1, price >= 40_000) принимает конкретные значения конкретных столбцов
                .group_by(ResumesORM.workload)
                # .having(cast(func.avg(ResumesORM.price), Integer) > 70_000)
            )
            # print(query)
            # print(query.compile(compile_kwargs={"literal_binds": True}))      #такой же запрос с уточненными именами переменных в запросе
            res = ses.execute(query)
            result_orm = res.all()
            print(f"{result_orm=}")  
            result_dto = [DTO_select.model_validate(i, from_attributes=True) for i in result_orm] 
            print(f"{result_dto=}")
            return result_dto
        
    @staticmethod
    def add_vacasis():
        with session() as ses:
            new_vacansis = VacansiORM(title= "Python junior", price = 100_000)
            resume1 = ses.get(ResumesORM, 1)
            resume2 = ses.get(ResumesORM, 2)
            resume1.resume_answer.append(new_vacansis)
            resume2.resume_answer.append(new_vacansis)
            ses.commit()

    @staticmethod
    def select_users_with_resume():
        with session() as ses:
            query = (
            select(ResumesORM)
            .options(joinedload(ResumesORM.worker))
            .options(selectinload(ResumesORM.resume_answer))       #опционально можно сделать ...ResumesORM.vacansis_answer)load_only(Vacansii.title)
            )
            res = ses.execute(query)
            result_orm = res.unique().scalars().all()
            print(f"{result_orm=}")

    @staticmethod
    def select_resume_with_workersDTO():
        with session() as ses:
            query = (
            select(ResumesORM)
            .options(joinedload(ResumesORM.worker))
            .options(selectinload(ResumesORM.resume_answer))       #опционально можно сделать ...ResumesORM.vacansis_answer)load_only(Vacansii.title)
            )
            res = ses.execute(query)
            result_orm = res.unique().scalars().all()
            # print(f"{result_orm=}")
            result_DTO = [ResumeRelVacansisRelDTO.model_validate(i, from_attributes=True) for i in result_orm]
            # print(f"{result_DTO=}")
            return result_DTO

class PostInfo():
    @staticmethod
    def add_workers(listname):
        with session() as ses:
            # answer = (WorkersORM(username = i) for i in listname.split())
            ses.add_all(listname)
            ses.commit()
            return listname