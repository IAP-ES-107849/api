from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import String, Integer, Boolean, Float, ARRAY, Text

from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, index=True)
    created_at = Column(DateTime, index=True)
    deadline = Column(DateTime, index=True)
    priority = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    category = Column(String, index=True)
