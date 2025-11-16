from typing import Callable, cast
from extraction.application.ports.browser_driver_port import BrowserDriverPort
from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from extraction.application.services.job_task_worker_service import JobTaskWorkerService
from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.browser_driver_config import BrowserDriverConfig
from shared.application.ports.logger_port import LoggerPort


class ExtractionJobRunnerService:

    def __init__(self,
                 task_worker_service_class: type[JobTaskWorkerService],
                 browser_driver_class: type[BrowserDriverPort],
                 browser_driver_config: BrowserDriverConfig,
                 place_extractor_class: type[PlaceExtractorPort],
                 extraction_uow_factory: Callable[[], ExtractionUnitOfWorkPort],
                 logger: LoggerPort | None = None):
        
        self.task_worker_service_class = task_worker_service_class
        self.browser_driver_class = browser_driver_class
        self.browser_driver_config = browser_driver_config
        self.place_extractor_class = place_extractor_class
        self.extraction_uow_factory = extraction_uow_factory
        self.logger = logger

    def run(self, extraction_job: ExtractionJob) -> ExtractionJob:
        
        with self.extraction_uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            pending_tasks = uow.job_task_repo.find_pending_by_job_id(extraction_job.id)