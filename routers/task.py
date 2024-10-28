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
    """
    Create a new task for a specific user.

    :param task_data: Task data to create
    :param user_id: User ID
    :param db: Database session
    :return: Task created

    :raises HTTPException: If the user does not exist or if there is an internal server error
    :raises Exception: If there is an internal server error
    """

    # Check if the user exists in the database
    user = get_user_by_username(user_username, db=db)

    if not user:
        logging.error(f"User with username {user_username} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        # Create a new task
        new_task = create_task(task=task_data, user_id=user.id, db=db)

        # If successful, return the task in the response
        return new_task

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions to maintain the status code
        raise http_exc

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )

    except Exception as e:
        logging.error(f"Failed to create task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating the task",
        )

