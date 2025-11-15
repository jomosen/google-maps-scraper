from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .task_status import TaskStatus


@dataclass
class JobTask:
    """Represents a single unit of work within an ExtractionJob."""

    id: str
    job_id: str
    search_seed: str
    geoname_id: int
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0
    last_error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def create(job_id: str, search_seed: str, geoname_id: int) -> JobTask:
        """Factory method to create a new pending task."""
        return JobTask(
            id=str(uuid.uuid4()),
            job_id=job_id,
            search_seed=search_seed,
            geoname_id=geoname_id,
            status=TaskStatus.PENDING,
        )

    def mark_running(self) -> None:
        """Mark task as running."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.touch()

    def mark_completed(self) -> None:
        """Mark task as successfully completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.touch()

    def mark_failed(self, error_message: Optional[str] = None) -> None:
        """Mark task as failed and store last error."""
        self.status = TaskStatus.FAILED
        self.attempts += 1
        self.last_error = error_message
        self.completed_at = datetime.utcnow()
        self.touch()

    def can_retry(self, max_attempts: int) -> bool:
        """Return True if the task can be retried based on attempts."""
        return self.status == TaskStatus.FAILED and self.attempts < max_attempts

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
