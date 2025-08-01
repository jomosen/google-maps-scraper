from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped
from app.infrastructure.persistence.base import Base
from typing import List, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .task_model import TaskModel

class ScrapingModel(Base):
    __tablename__ = "scrapings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    language = Column(String(10), nullable=False)
    max_reviews = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    tasks: Mapped[List["TaskModel"]] = relationship(
        "TaskModel",
        back_populates="scraping",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Scraping(id={self.id}, status={self.status}, created_at={self.created_at})>"
