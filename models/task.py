from typing import Optional
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import String, Integer, Boolean, Float, ARRAY, Text
from datetime import datetime, timezone
import uuid

from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    priority = Column(Integer, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(500), default="Todo", nullable=False)
