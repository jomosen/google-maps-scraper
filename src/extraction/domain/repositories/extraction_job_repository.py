from typing import Protocol, Optional
from extraction.domain.extraction_job import ExtractionJob


class ExtractionJobRepository(Protocol):
    """
    Port for persisting and retrieving ExtractionJob aggregate roots.
    Implementations live in the infrastructure layer.
    """

    def save(self, job: ExtractionJob) -> None:
        """
        Persist the ExtractionJob aggregate.
        Implementations should perform insert/update as needed.
        """
        ...

    def find_by_id(self, job_id: str) -> Optional[ExtractionJob]:
        """
        Retrieve an ExtractionJob by its ID.
        Return None if not found.
        """
        ...

    def delete(self, job_id: str) -> None:
        """
        Delete the ExtractionJob by ID.
        Optional in many systems but good to define.
        """
        ...
