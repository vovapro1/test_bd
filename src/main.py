# from queries.core import create_table, insert_data,
from typing import Optional
from fastapi import FastAPI
import uvicorn
from queries.core import Work_Table
from queries.orm import Work_Table_ORM
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "..'"))
from database import engin, async_engin, session, Base
from sqlalchemy import insert
from queries.models import WorkersORM, ResumesORM
from queries.models import Workload


# Work_Table.create_table()
# Work_Table.insert_data()
# Work_Table.select_workers()
# Work_Table.update_workers()

# Work_Table_ORM.create_table()
# Work_Table_ORM.insert_data()
# Work_Table_ORM.update_workers()
# Work_Table_ORM.select_workers()
Work_Table_ORM.insert_resum()
# Work_Table_ORM.insert_additional_resumes()
# Work_Table_ORM.join_and_sort()
# Work_Table_ORM.select_workers_with_lazy_relationship()
# Work_Table_ORM.select_workers_with_joined_relationship()
# Work_Table_ORM.select_workers_with_selectin_relationship()
# Work_Table_ORM.select_wokers_with_reletionship()
# ans = Work_Table_ORM.select_wokers_with_reletionship_contains_eager()
# answer = [i[0].username for i in ans if i[0].worker_id == 2]
# print(answer)

# app = FastAPI(title="MOI FASTAPI")


# @app.get("/")
# def get_fast(id: int):
#     ans = Work_Table_ORM.select_wokers_with_reletionship_contains_eager()
#     answer = [i[0].username for i in ans if i[0].worker_id == id]
#     return f"{answer[0]}"

# @app.post("/add_worker")
# def add_new_worker(username:str):
#     with session() as ses:
#         workers = [
#             {"username": username}  # id 6

#         ]
#         insert_workers = insert(WorkersORM).values(workers)
#         ses.execute(insert_workers)
#         ses.commit()
#         return f'добавлен пользователь {username}'

# @app.post("/add_resume")
# def add_new_resume(title: str, price: int, workload: Workload, worker_id: int):
#     with session() as ses:
#         resumes = [
#             {"title": title, "price": price, "workload": workload, "worker_id": worker_id},
#         ]
#         insert_resumes = insert(ResumesORM).values(resumes)
#         ses.execute(insert_resumes)
#         ses.commit()
#         return f"Новое резюме для пользователя с id {worker_id}, добавлено"




# if __name__ == '__main__':
#     uvicorn.run(reload=True, app='main:app')
