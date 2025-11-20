from datetime import datetime
from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService
from extraction.domain.value_objects.geoname_selection_params_for_extraction_job import GeoNameSelectionParamsForExtractionJob
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig
from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.repositories.extraction_job_repository import ExtractionJobRepository
from extraction.application.use_cases.create_extraction_job_use_case import CreateExtractionJobUseCase
from extraction.application.use_cases.run_extraction_job_use_case import RunExtractionJobUseCase
from extraction.application.services.geoname_selection_service import GeoNameSelectionService
from shared.application.ports.logger_port import LoggerPort


def create(
        job_config: ExtractionJobConfig,
        job_repo: ExtractionJobRepository, 
        geoname_selection_service: GeoNameSelectionService):

    use_case = CreateExtractionJobUseCase(
        job_repo=job_repo,
        geoname_selection_service=geoname_selection_service
    )

    extraction_job = use_case.execute(config=job_config)
    return extraction_job

def run(extraction_job: ExtractionJob, 
        extraction_job_runner: ExtractionJobRunnerService, 
        logger: LoggerPort):
    
    use_case = RunExtractionJobUseCase(
        extraction_job_runner=extraction_job_runner,
        logger=logger
    )

    extraction_job = use_case.execute(job=extraction_job)
    return extraction_job