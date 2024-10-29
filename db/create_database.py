from models.task import Task
from models.user import User
from db.database import engine


def create_tables():
    Task.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    