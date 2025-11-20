from abc import ABC, abstractmethod
from extraction.domain.extraction_task import ExtractionTask


class ExtractionTaskRepository(ABC):
    
    @abstractmethod
    def save(self, task: ExtractionTask) -> None:
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> ExtractionTask | None:
        pass