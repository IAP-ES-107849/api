from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from db.database import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate

def create_task(task: TaskCreate, user_id: str, db: Session = Depends(get_db)):
    """
    Function that creates a new task.

    :param task: Task data to be created.
    :param db: Database session.
    :return: Task created.
    """

    new_task = Task(**task.model_dump(), user_id=user_id)
    if new_task.deadline and new_task.deadline < datetime.now(timezone.utc):
        raise ValueError("Deadline must be in the future.")

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_task_by_id(task_id: str, db: Session = Depends(get_db)):
    """
    Function that retrieves a task by its ID.

    :param task_id: ID of the task to be retrieved.
    :param db: Database session.
    :return: Task retrieved.
    """

    return db.query(Task).filter(Task.id == task_id).first()

def get_task_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """
    Function that retrieves a task by its ID.

    :param task_id: ID of the task to be retrieved.
    :param db: Database session.
    :return: Task retrieved.
    """

    return db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at).all()

def delete_task_by_id(task_id: str, db: Session = Depends(get_db)):
    """
    Function that deletes a task by its ID.

    :param task_id: ID of the task to be deleted.
    :param db: Database session.
    :return: Task deleted.
    """

    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise ValueError("Task not found.")

    db.delete(task)
    db.commit()

    return task

def update_task_by_id(task_id: str, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Function that updates a task by its ID.

    :param task_id: ID of the task to be updated.
    :param task: Task data to be updated.
    :param db: Database session.
    :return: Task updated.
    """

    task_db = db.query(Task).filter(Task.id == task_id).first()
    if task_db is None:
        raise ValueError("Task not found.")

    for key, value in task.dict().items():
        setattr(task_db, key, value)

    db.commit()
    db.refresh(task_db)

    return task_db
