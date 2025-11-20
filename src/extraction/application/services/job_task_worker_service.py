from typing import Callable, cast
from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.domain.extraction_task import JobTask
from extraction.domain.extraction_job_config import ExtractionJobConfig
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from extraction.application.ports.geonames_lookup_port import GeoNamesLookupPort
from extraction.application.ports.places_storage_port import PlaceStoragePort
from shared.application.ports.logger_port import LoggerPort


class JobTaskWorkerService:
    
    def __init__(self,
                 job_tasks: list[JobTask],
                 job_config: ExtractionJobConfig,
                 place_extractor: PlaceExtractorPort,
                 geonames_lookup: GeoNamesLookupPort,
                 places_storage: PlaceStoragePort,
                 extraction_uow_factory: Callable[[], ExtractionUnitOfWorkPort],
                 logger: LoggerPort | None = None):
        
        self.job_tasks = job_tasks
        self.job_config = job_config
        self.place_extractor = place_extractor
        self.geonames_lookup = geonames_lookup
        self.places_storage = places_storage
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

                    geoname = self.geonames_lookup.find_by_geoname_id(task.geoname_id)
                    if not geoname:
                        raise ValueError(f"GeoName with ID {task.geoname_id} not found.")

                    for place in self.place_extractor.extract(task, geoname, self.job_config):
                        self.places_storage.save(place)

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