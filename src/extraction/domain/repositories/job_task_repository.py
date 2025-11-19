from abc import ABC, abstractmethod
from extraction.domain.extraction_task import JobTask


class ExtractionTaskRepository(ABC):
    
    @abstractmethod
    def save(self, job_task: JobTask) -> None:
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> JobTask | None:
        pass

    @abstractmethod
    def find_pending_by_job_id(self, job_id: str) -> list[JobTask]:
        pass