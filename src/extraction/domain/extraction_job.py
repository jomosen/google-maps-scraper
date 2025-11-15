from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .job_status import JobStatus
from .job_task import JobTask
from .job_config import JobConfig


@dataclass
class ExtractionJob:
    """Aggregate root representing a full extraction job."""

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

    tasks: List[JobTask] = field(default_factory=list)

    @staticmethod
    def create(title: str, config: JobConfig) -> ExtractionJob:
        """Factory method to create a new pending job."""
        return ExtractionJob(
            id=str(uuid.uuid4()),
            title=title,
            status=JobStatus.PENDING,
            config=config,
        )

    def mark_running(self) -> None:
        """Mark job as running."""
        if self.status == JobStatus.PENDING:
            self.status = JobStatus.RUNNING
            self.started_at = datetime.utcnow()
            self.touch()

    def mark_completed(self) -> None:
        """Force job status to completed."""
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.touch()

    def mark_failed(self) -> None:
        """Force job status to failed."""
        self.status = JobStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.touch()

    def add_task(self, search_seed: str, geoname_id: int) -> JobTask:
        """Create and attach a new task to this job."""
        task = JobTask.create(
            job_id=self.id,
            search_seed=search_seed,
            geoname_id=geoname_id,
        )
        self.tasks.append(task)
        self.total_tasks += 1
        self.touch()
        return task

    def register_task_completed(self, task: JobTask) -> None:
        """Update counters when a task is completed."""
        self.completed_tasks += 1
        self._recalculate_status()
        self.touch()

    def register_task_failed(self, task: JobTask) -> None:
        """Update counters when a task fails."""
        self.failed_tasks += 1
        self._recalculate_status()
        self.touch()

    def _recalculate_status(self) -> None:
        """Recalculate job status based on tasks counters."""
        if self.total_tasks == 0:
            return

        processed = self.completed_tasks + self.failed_tasks

        if processed < self.total_tasks:
            # still running if at least one task started
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
        """Return job progress as a float between 0.0 and 1.0."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks + self.failed_tasks) / self.total_tasks

    def is_finished(self) -> bool:
        """Return True if job is in any finished terminal state."""
        return self.status in {
            JobStatus.COMPLETED,
            JobStatus.PARTIAL_COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        }

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
