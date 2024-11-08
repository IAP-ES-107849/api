import logging
from typing import List
from crud.task import delete_task_by_id, get_task_by_id, get_task_by_user_id, update_task_by_id
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db

from crud.user import get_user_by_id, get_user_by_username, create_user
from crud.task import create_task
from schemas.task import TaskCreate, TaskInDB, TaskUpdate
from auth.auth import jwks, get_current_user
from auth.JWTBearer import JWTBearer

router = APIRouter(tags=["Tasks"])

auth = JWTBearer(jwks)


@router.post(
    "/tasks",
    response_model=TaskInDB,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth)],
)
async def create_new_task(
    task_data: TaskCreate,
    user_username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint that creates a new task.

    :param task_data: Task data to be created.
    :param user_username: Username of the user creating the task.
    :param db: Database session.
    :return: Task created.
    """

    user = get_user_by_username(user_username, db)
    if user is None:
        logging.error(f"User with username {user_username} not found.")
        raise HTTPException(status_code=404, detail="User not found.")

    return create_task(task=task_data, user_id=user.id, db=db)

@router.get("/tasks", response_model=List[TaskInDB], dependencies=[Depends(auth)])
async def get_all_tasks(user_username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Endpoint that retrieves all tasks from a user.

    :param user_username: Username of the user to retrieve tasks.
    :param db: Database session.
    :return: List of tasks.
    """

    user = get_user_by_username(user_username, db)
    if user is None:
        logging.error(f"User with username {user_username} not found.")
        raise HTTPException(status_code=404, detail="User not found.")

    tasks = get_task_by_user_id(user_id = user.id, db = db)
    return tasks

@router.delete("/tasks/{task_id}", dependencies=[Depends(auth)])
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Endpoint that deletes a task by its ID.

    :param task_id: ID of the task to be deleted.
    :param db: Database session.
    :return: Task deleted.
    """

    task = get_task_by_id(task_id, db)
    if task is None:
        logging.error(f"Task with ID {task_id} not found.")
        raise HTTPException(status_code=404, detail="Task not found.")

    return delete_task_by_id(task_id, db)

@router.put("/tasks/{task_id}", response_model=TaskInDB, dependencies=[Depends(auth)])
async def update_task(task_id: str, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Endpoint that updates a task by its ID.

    :param task_id: ID of the task to be updated.
    :param task_data: Task data to be updated.
    :param db: Database session.
    :return: Task updated.
    """

    task = get_task_by_id(task_id, db)
    if task is None:
        logging.error(f"Task with ID {task_id} not found.")
        raise HTTPException(status_code=404, detail="Task not found.")

    return update_task_by_id(task_id=task_id, task=task_data, db=db)