from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    deadline: Optional[str]
    priority: Optional[int]
    user_id: Optional[int]
    status: Optional[str]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDB(TaskBase):
    id: int
