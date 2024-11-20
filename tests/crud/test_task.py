import pytest
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.mysql import MySqlContainer

from db.database import get_db
from main import app
from models.task import Task as TaskModel
from models.user import User as UserModel
from schemas.task import TaskCreate, TaskUpdate
from crud.task import create_task, get_task_by_id, get_task_by_user_id, delete_task_by_id, update_task_by_id
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

my_sql_container = MySqlContainer(
    "mysql:8.0",
    root_password="test_root_password",
    dbname="test_db",
    username="test_username",
    password="test_password",
)


@pytest.fixture(name="session", scope="module")
def setup():
    my_sql_container.start()
    connection_url = my_sql_container.get_connection_url()
    engine = create_engine(connection_url, connect_args={})
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    UserModel.metadata.create_all(engine)
    TaskModel.metadata.create_all(engine)

    def override_get_db():
        db = sessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield sessionLocal
    my_sql_container.stop()


@pytest.fixture(name="test_db", scope="module")
def create_test_db(session):
    db = session()
    yield db
    db.close()


@pytest.fixture(name="test_user", scope="function")
def create_test_user(test_db):
    test_user = UserModel(
        id="test_user_id",
        given_name="Test",
        family_name="User",
        username="testuser",
        email="testuser@example.com",
    )
    test_db.add(test_user)
    test_db.commit()
    yield test_user
    test_db.delete(test_user)
    test_db.commit()
from datetime import datetime, timedelta, timezone

def test_create_task(test_db, test_user):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        created_at=datetime.now(timezone.utc),
        priority=1,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        status="Todo"
    )
    created_task = create_task(task_data, test_user.id, test_db)

    assert created_task is not None
    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.priority == 1
    assert created_task.status == "Todo"
    assert created_task.user_id == test_user.id


def test_get_task_by_id(test_db, test_user):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        created_at=datetime.now(timezone.utc),
        priority=1,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        status="Todo"
    )
    created_task = create_task(task_data, test_user.id, test_db)

    found_task = get_task_by_id(created_task.id, test_db)

    assert found_task is not None
    assert found_task.id == created_task.id


def test_get_task_by_user_id(test_db, test_user):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        created_at=datetime.now(timezone.utc),
        priority=1,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        status="Todo"
    )
    created_task = create_task(task_data, test_user.id, test_db)

    tasks = get_task_by_user_id(test_user.id, test_db)

    assert len(tasks) > 0
    assert tasks[0].user_id == test_user.id


def test_update_task_by_id(test_db, test_user):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        created_at=datetime.now(timezone.utc),
        priority=1,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        status="Todo"
    )
    created_task = create_task(task_data, test_user.id, test_db)

    update_data = TaskUpdate(
        title="Updated Task",
        description="This is an updated test task",
        priority=2,
        deadline=datetime.now(timezone.utc) + timedelta(days=2),
        status="Done"
    )

    updated_task = update_task_by_id(created_task.id, update_data, test_db)

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "This is an updated test task"
    assert updated_task.priority == 2
    assert updated_task.status == "Done"


def test_delete_task_by_id(test_db, test_user):
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        created_at=datetime.now(timezone.utc),
        priority=1,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        status="Todo"
    )
    created_task = create_task(task_data, test_user.id, test_db)

    deleted_task = delete_task_by_id(created_task.id, test_db)

    assert deleted_task is not None
    assert deleted_task.id == created_task.id

    found_task = get_task_by_id(created_task.id, test_db)
    assert found_task is None