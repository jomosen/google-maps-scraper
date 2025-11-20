from typing import List
from datetime import datetime

from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig
from extraction.domain.repositories.extraction_job_repository import ExtractionJobRepository
from extraction.domain.extraction_task import ExtractionTask
from extraction.application.services.geoname_selection_service import GeoNameSelectionService


class CreateExtractionJobUseCase:

    def __init__(self, 
                 job_repo: ExtractionJobRepository, 
                 geoname_selection_service: GeoNameSelectionService):
        
        self.job_repository = job_repo
        self.geoname_selection_service = geoname_selection_service

    def execute(self, config: ExtractionJobConfig, title: str | None = None) -> ExtractionJob:

        if not title:
            title = f"{config.search_seeds[0].title()} {config.geoname_selection_params.scope_geoname_name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".capitalize()
        
        job = ExtractionJob.create(
            title=title,
            config=config,
        )

        tasks = self._generate_tasks(job)

        job.add_tasks(tasks)

        self.job_repository.save(job)

        return job

    def _generate_tasks(self, job: ExtractionJob) -> List[ExtractionTask]:

        geonames = self.geoname_selection_service.select(job.config.geoname_selection_params)

        return [
            ExtractionTask.create(
                job_id=job.id,
                search_seed=search_seed,
                geoname=geoname
            )
            for geoname in geonames
            for search_seed in job.config.search_seeds
        ]