from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    done: bool
    created_at: Optional[str]
    deadline: Optional[str]
    priority: Optional[int]
    user_id: Optional[int]
    category: Optional[str]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDB(TaskBase):
    id: int

    class Config:
        orm_mode = True