from models.task import Task

from db.database import engine


def create_tables():
    Task.metadata.create_all(bind=engine)
    