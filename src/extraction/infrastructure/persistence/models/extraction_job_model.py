import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.orm import relationship, Mapped
from extraction.infrastructure.persistence.database.base import ExtractionBase as Base

if TYPE_CHECKING:
    from .extraction_task_model import ExtractionTaskModel


class ExtractionJobModel(Base):
    __tablename__ = "extraction_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String(255), nullable=False)

    status = Column(String(30), nullable=False, default="pending")

    config = Column(JSON, nullable=False, default=dict)

    total_tasks = Column(Integer, nullable=False, default=0)
    completed_tasks = Column(Integer, nullable=False, default=0)
    failed_tasks = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks: Mapped[List["ExtractionTaskModel"]] = relationship(
        "ExtractionTaskModel",
        back_populates="job",
        cascade="all, delete-orphan"
    )
