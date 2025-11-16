from typing import Protocol
from shared.application.ports.unit_of_work_port import UnitOfWorkPort
from extraction.domain.repositories.extraction_job_repository import ExtractionJobRepository
from extraction.domain.repositories.job_task_repository import JobTaskRepository


class ExtractionUnitOfWorkPort(UnitOfWorkPort, Protocol):
    extraction_job_repo: ExtractionJobRepository
    job_task_repo: JobTaskRepository
