from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .job_status import JobStatus
from .job_config import JobConfig

@dataclass
class ExtractionJob:
    id: str
    title: str
    status: JobStatus
    config: JobConfig

    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0

    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def create(title: str, config: JobConfig) -> ExtractionJob:
        return ExtractionJob(
            id=str(uuid.uuid4()),
            title=title,
            status=JobStatus.PENDING,
            config=config,
        )

    def add_task(self) -> None:
        self.total_tasks += 1
        self.touch()

    def register_task_completed(self) -> None:
        self.completed_tasks += 1
        self._recalculate_status()
        self.touch()

    def register_task_failed(self) -> None:
        self.failed_tasks += 1
        self._recalculate_status()
        self.touch()

    def _recalculate_status(self) -> None:
        if self.total_tasks == 0:
            return

        processed = self.completed_tasks + self.failed_tasks

        if processed < self.total_tasks:
            if self.status == JobStatus.PENDING:
                self.status = JobStatus.RUNNING
            return

        # All tasks processed
        if self.failed_tasks == 0:
            self.status = JobStatus.COMPLETED
        else:
            self.status = JobStatus.PARTIAL_COMPLETED

        self.completed_at = datetime.utcnow()

    def progress(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks + self.failed_tasks) / self.total_tasks

    def is_finished(self) -> bool:
        return self.status in {
            JobStatus.COMPLETED,
            JobStatus.PARTIAL_COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        }

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
