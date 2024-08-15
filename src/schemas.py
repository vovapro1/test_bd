from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from queries.models import WorkersORM, Workload

class WorkersPostDTO(BaseModel):
    username : str

class WorkersGetDTO(WorkersPostDTO):
    worker_id : int

class ResumePostDTO(BaseModel):
    title : str
    price : Optional[int]
    workload : Workload
    worker_id : int

class ResumeGetDTO(ResumePostDTO):               #DTO = Data Transfer Object, Обьект для передачи даннх между слоями/сервисами приложениями
    id : int
    create_at : datetime
    update_at : datetime

class ResumeRelDTO(ResumeGetDTO):
    worker : "WorkersPostDTO"

class WorkersRelDTO(WorkersGetDTO):
    resumes : list["ResumePostDTO"]

class DTO_select(BaseModel):
    workload : Workload
    avg_price : int

class VacansisPostDTO(BaseModel):
    title : str
    price : Optional[int]

class VacansisGetDTO(VacansisPostDTO):
    id : int

class ResumeRelVacansisRelDTO(ResumePostDTO):
    worker : "WorkersPostDTO"
    resume_answer : list["VacansisPostDTO"]

