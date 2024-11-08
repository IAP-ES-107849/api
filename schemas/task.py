from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    priority: int
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]
    deadline: Optional[datetime]
    status: Optional[str]
    

class TaskInDB(TaskBase):
    id: str
    status: str
    created_at: datetime
