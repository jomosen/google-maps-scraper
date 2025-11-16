from typing import Callable, cast
from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.domain.job_task import JobTask
from extraction.domain.job_config import JobConfig
from extraction.application.ports.browser_driver_port import BrowserDriverPort
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from shared.application.ports.logger_port import LoggerPort


class JobTaskWorkerService:
    
    def __init__(self,
                 job_tasks: list[JobTask],
                 job_config: JobConfig,
                 browser_driver: BrowserDriverPort,
                 place_extractor: PlaceExtractorPort,
                 extraction_uow_factory: Callable[[], ExtractionUnitOfWorkPort],
                 logger: LoggerPort | None = None):
        
        self.job_tasks = job_tasks
        self.job_config = job_config
        self.browser_driver = browser_driver
        self.place_extractor = place_extractor
        self.extraction_uow_factory = extraction_uow_factory
        self.logger = logger

    def process(self):
        
        for task in self.job_tasks:
            try:
                if self.logger:
                    self.logger.info(f"Starting task {task.id}...")

                task.mark_running()
                with self.extraction_uow_factory() as uow:
                    uow = cast(ExtractionUnitOfWorkPort, uow)
                    uow.job_task_repo.save(task)
                    uow.commit()

                    self.place_extractor.extract(task)

                    task.mark_completed()
                    uow.job_task_repo.save(task)
                    uow.commit()

                if self.logger:
                    self.logger.info(f"Task {task.id} completed.")

            except Exception as e:
                task.mark_failed()
                with self.extraction_uow_factory() as uow:
                    uow = cast(ExtractionUnitOfWorkPort, uow)
                    uow.job_task_repo.save(task)
                    uow.commit()

                if self.logger:
                    self.logger.error(f"Task {task.id} failed: {e}")

        try:
            self.browser_driver.close()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error closing browser driver: {e}")