from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from queries.models import Workload

class WorkersPostDTO(BaseModel):
    username : str

class WorkersDTO(WorkersPostDTO):
    id : int

class ResumeAddDTO(BaseModel):
    title : str
    price : Optional[int]
    workload : Workload
    worker_id : int

class ResumeDTO(ResumeAddDTO):               #DTO = Data Transfer Object, Обьект для передачи даннх между слоями/сервисами приложениями
    id : int
    create_at : datetime
    update_at : datetime

class ResumeRelDTO(ResumeDTO):
    worker : "WorkersPostDTO"

class WorkersRelDTO(WorkersDTO):
    resumes : list["ResumeAddDTO"]


