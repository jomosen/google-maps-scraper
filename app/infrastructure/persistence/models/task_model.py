from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from app.infrastructure.persistence.base import Base
from typing import TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .scraping_model import ScrapingModel

class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scraping_id = Column(String(36), ForeignKey('scrapings.id'), nullable=False)
    keyword = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    scraping: Mapped["ScrapingModel"] = relationship(
        "ScrapingModel",
        back_populates="tasks"
    )

    def __repr__(self):
        return (
            f"<Task(id='{self.id}', location='{self.location}', "
            f"keyword='{self.keyword}', status='{self.status}')>"
        )
