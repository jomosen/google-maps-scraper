import uuid
from datetime import datetime
from typing import List

from extraction.domain.extraction_job import ExtractionJob
from app.domain.scraping.value_objects.job_config_vo import JobConfigVO
from app.domain.scraping.repositories.i_job_repository import IJobRepository
from app.domain.scraping.entities.job import Task
from app.domain.geoname.services.geoname_selector_service import GeoNameSelectorService

class CreateExtractionJobUseCase:
    """Service to create Scraping entities and generate associated tasks."""

    def __init__(self, job_repository: IJobRepository, 
                 geoname_selector_service: GeoNameSelectorService):
        self.job_repository = job_repository
        self.geoname_selector_service = geoname_selector_service

    def execute(self, title: str | None, config: JobConfigVO) -> Job:
        job_id = str(uuid.uuid4())
        title = title or job_id

        job = Job.build(
            title=title,
            config=config,
        )

        job.tasks = self._generate_tasks(job)

        self.job_repository.save(job)

        return job

    def _generate_tasks(self, job: Job) -> List[Task]:
        """Generates tasks for the given scraping entity based on its options."""

        geonames = self.geoname_selector_service.select_geonames_for_config(job.config)

        return [
            Task.build(
                job_id=job.id,
                search_seed=search_seed,
                geoname_id=geoname.geoname_id
            )
            for geoname in geonames
            for search_seed in job.config.search_seeds
        ]