from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import String, Integer, Boolean, Float, ARRAY, Text

from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    description = Column(String(500), index=True)
    deadline = Column(DateTime, index=True)
    priority = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    status = Column(String(500), index=True)
