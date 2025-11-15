import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from extraction.infrastructure.persistence.database.base import ExtractionBase as Base

if TYPE_CHECKING:
    from .extraction_job_model import ExtractionJobModel


class JobTaskModel(Base):

    __tablename__ = "extraction_job_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    job_id = Column(
        String(36),
        ForeignKey("extraction_jobs.id"),
        nullable=False
    )

    search_seed = Column(String(255), nullable=False)
    geoname_id = Column(Integer, ForeignKey("geonames.geoname_id"), nullable=False)

    status = Column(String(30), nullable=False, default="pending")
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job: Mapped["ExtractionJobModel"] = relationship(
        "ExtractionJobModel",
        back_populates="tasks"
    )
