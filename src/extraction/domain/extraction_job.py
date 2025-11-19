from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .enums.extraction_job_status import ExtractionJobStatus
from .value_objects.extraction_job_config import ExtractionJobConfig


@dataclass
class ExtractionJob:
    id: str
    title: str
    status: ExtractionJobStatus
    config: ExtractionJobConfig

    # Counters are OK if updated externally (via Application Service)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0

    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @staticmethod
    def create(title: str, config: ExtractionJobConfig) -> ExtractionJob:
        return ExtractionJob(
            id=str(uuid.uuid4()),
            title=title,
            status=ExtractionJobStatus.PENDING,
            config=config,
        )
    
    def mark_in_progress(self) -> None:
        if self.status == ExtractionJobStatus.COMPLETED:
            raise ValueError("Cannot start a completed job.")
        if self.status == ExtractionJobStatus.FAILED:
            raise ValueError("Cannot start a failed job.")

        self.status = ExtractionJobStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
        self.touch()

    def mark_completed(self) -> None:
        if self.status != ExtractionJobStatus.IN_PROGRESS:
            raise ValueError("Cannot complete a job not in progress.")

        self.status = ExtractionJobStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.touch()

    def mark_failed(self) -> None:
        if self.status == ExtractionJobStatus.COMPLETED:
            raise ValueError("Cannot fail a completed job.")

        self.status = ExtractionJobStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.touch()
        
    def is_completed(self) -> bool:
        return self.status == ExtractionJobStatus.COMPLETED

    def is_finished(self) -> bool:
        return self.status in {
            ExtractionJobStatus.COMPLETED,
            ExtractionJobStatus.FAILED,
        }

    def progress(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks + self.failed_tasks) / self.total_tasks

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
