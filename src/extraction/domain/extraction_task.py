from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .enums.extraction_task_status import ExtractionTaskStatus
from .value_objects.geoname import GeoName


@dataclass
class ExtractionTask:
    """
    Represents a single unit of work within an ExtractionJob.
    Each task defines a search operation starting from a geographic point.
    """

    id: str
    job_id: str
    search_seed: str
    geoname: GeoName

    status: ExtractionTaskStatus = ExtractionTaskStatus.PENDING
    attempts: int = 0
    last_error: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def create(
        job_id: str,
        search_seed: str,
        geoname: GeoName,
    ) -> ExtractionTask:
        """Factory method to create a new pending task."""
        return ExtractionTask(
            id=str(uuid.uuid4()),
            job_id=job_id,
            search_seed=search_seed,
            geoname=geoname,
        )
    
    def mark_running(self) -> None:
        self.status = ExtractionTaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.touch()

    def mark_completed(self) -> None:
        self.status = ExtractionTaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.touch()

    def mark_failed(self, error_message: Optional[str] = None) -> None:
        self.status = ExtractionTaskStatus.FAILED
        self.attempts += 1
        self.last_error = error_message
        self.completed_at = datetime.utcnow()
        self.touch()

    def can_retry(self, max_attempts: int) -> bool:
        return (
            self.status == ExtractionTaskStatus.FAILED
            and self.attempts < max_attempts
        )

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
