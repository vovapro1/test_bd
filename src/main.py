import sys
import os

from fastapi import FastAPI
import uvicorn
from queries.orm import Work_Table_ORM
from queries.core import Work_Table
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(1, os.path.join(sys.path[0], "..'"))


# Work_Table.create_table()
# Work_Table.insert_data()
# Work_Table.select_workers()
# Work_Table.update_workers()

# Work_Table_ORM.create_table()
# Work_Table_ORM.insert_data()
# Work_Table_ORM.select_workers()
# Work_Table_ORM.update_workers()
# Work_Table_ORM.insert_resum()
# Work_Table_ORM.insert_additional_resumes()
# Work_Table_ORM.join_and_sort()
# Work_Table_ORM.select_workers_with_lazy_relationship()
# Work_Table_ORM.select_workers_with_joined_relationship()
# Work_Table_ORM.select_workers_with_selectin_relationship()
# Work_Table_ORM.select_wokers_with_reletionship()
# Work_Table_ORM.select_wokers_with_reletionship_contains_eager()
# Work_Table_ORM.easy_select()
# Work_Table_ORM.hard_select()
# Work_Table_ORM.DTO_select()
# Work_Table_ORM.add_vacasis()
# Work_Table_ORM.select_users_with_resume()
# Work_Table_ORM.select_resume_with_workersDTO()

def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/workers", tags=["Кандидат"])
    def get_workers():
        workers = Work_Table_ORM.hard_select()
        return workers
    
    @app.get("/resume", tags=["Резюме"])
    def get_resum():
        resum = Work_Table_ORM.select_resume_with_workersDTO()
        return resum

    return app


app = create_fastapi_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
    )
