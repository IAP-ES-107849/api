from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from db.database import get_db
from models.task import Task as TaskModel
from schemas.task import TaskCreate, TaskUpdate


def create_task(task: TaskCreate, user_id: str, db: Session = Depends(get_db)):
    ...

def get_tasks_by_user_id(user_id: str, db: Session = Depends(get_db)):
    ...