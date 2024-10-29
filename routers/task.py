import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from crud.task import (
    create_task,
    get_tasks_by_user_id,
    delete_task_by_id,
    get_task_by_id,
    update_task,
)
from crud.user import get_user_by_id, get_user_by_username
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
  ...