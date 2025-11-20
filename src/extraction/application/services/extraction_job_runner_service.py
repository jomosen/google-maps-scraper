from typing import Callable, List, cast
from math import ceil

from concurrent.futures import ThreadPoolExecutor, as_completed
from extraction.application.ports.browser_driver_port import BrowserDriverPort
from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from extraction.application.services.job_task_worker_service import JobTaskWorkerService
from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.value_objects.browser_driver_config import BrowserDriverConfig
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig
from extraction.domain.extraction_task import ExtractionTask
from extraction.application.ports.places_storage_port import PlaceStoragePort
from shared.application.ports.logger_port import LoggerPort


class ExtractionJobRunnerService:

    def __init__(self,
                 extraction_uow_factory: Callable[[], ExtractionUnitOfWorkPort],
                 task_worker_service_class: type[JobTaskWorkerService],
                 browser_driver_class: type[BrowserDriverPort],
                 browser_driver_config: BrowserDriverConfig,
                 place_extractor_class: type[PlaceExtractorPort],
                 places_storage_class: type[PlaceStoragePort],
                 logger: LoggerPort | None = None):
        
        self.task_worker_service_class = task_worker_service_class
        self.browser_driver_class = browser_driver_class
        self.browser_driver_config = browser_driver_config
        self.place_extractor_class = place_extractor_class
        self.extraction_uow_factory = extraction_uow_factory
        self.places_storage_class = places_storage_class
        self.logger = logger

    def run(self, extraction_job: ExtractionJob) -> ExtractionJob:
        
        with self.extraction_uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            pending_tasks = uow.job_task_repo.find_pending_by_job_id(extraction_job.id)
            total_pending = len(pending_tasks)

            if total_pending == 0:
                if self.logger:
                    self.logger.info(f"No pending tasks for job {extraction_job.id}.")
                return extraction_job

            if self.logger:
                self.logger.info(f"Running {total_pending} tasks for job {extraction_job.id}...")

            task_chunks = self._split_tasks_into_chunks(pending_tasks, extraction_job.config.max_workers)

            if self.logger:
                self.logger.info(f"Divided {total_pending} tasks into {len(task_chunks)} chunks.")

            self._execute_task_chunks(task_chunks, extraction_job)

            if self.logger:
                self.logger.info(f"All workers completed for job {extraction_job.id}.")

        return extraction_job

    def _split_tasks_into_chunks(self, tasks: List[ExtractionTask], max_workers: int) -> List[List[ExtractionTask]]:

        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        total_tasks = len(tasks)
        if total_tasks == 0:
            return [[] for _ in range(max_workers)]

        chunk_size = ceil(total_tasks / max_workers)

        chunks = [
            tasks[i * chunk_size : (i + 1) * chunk_size]
            for i in range(max_workers)
        ]

        chunks_without_empties = [chunk for chunk in chunks if len(chunk) > 0]
        return chunks_without_empties
    
    def _execute_task(self, tasks: list[ExtractionTask], job_config: ExtractionJobConfig, worker_id: int):
        try:
            browser_driver = self.browser_driver_class(config=self.browser_driver_config)

            place_extractor = self.place_extractor_class(
                browser_driver=browser_driver,
                job_config=job_config,
                logger=self.logger
            )
            
            places_storage = self.places_storage_port_class()

            worker = self.task_worker_service_class(
                tasks, 
                job_config, 
                place_extractor, 
                places_storage, 
                self.extraction_uow_factory, 
                self.logger)
            
            worker.process()

        except Exception as e:
            if self.logger:
                self.logger.error(f"Worker {worker_id} failed: {e}")

    def _execute_task_chunks(self, task_chunks: List[List[ExtractionTask]], job: ExtractionJob):

        with ThreadPoolExecutor(max_workers=job.config.max_workers) as executor:
            futures = []
            for i, chunk in enumerate(task_chunks, start=1):
                if self.logger:
                    self.logger.info(f"Worker {i} assigned {len(chunk)} tasks.")

                # Create a future for each worker
                futures.append(
                    executor.submit(self._execute_task, chunk, job.config, i)
                )

            # Wait for all workers to finish
            for future in as_completed(futures):
                try:
                    future.result()  # propagate any exception from the worker
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Worker execution failed: {e}")