from shared.application.ports.unit_of_work_port import UnitOfWorkPort
from extraction.domain.repositories.extraction_job_repository import ExtractionJobRepository
from extraction.domain.repositories.extraction_task_repository import ExtractionTaskRepository


class ExtractionUnitOfWorkPort(UnitOfWorkPort):
    extraction_job_repo: ExtractionJobRepository
    job_task_repo: ExtractionTaskRepository
