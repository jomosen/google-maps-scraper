from typing import cast
from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.domain.extraction_job import ExtractionJob
from shared.application.ports.logger_port import LoggerPort
from shared.application.use_case import UseCase
from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService


class RunExtractionUseCase(UseCase):

    def __init__(self, extraction_job_runner: ExtractionJobRunnerService, logger: LoggerPort = None):
        self.extraction_job_runner = extraction_job_runner
        self.logger = logger

    def execute(self, extraction_job: ExtractionJob) -> ExtractionJob:

        if self.logger:
            self.logger.info(f"Starting job {extraction_job.id}...")

        if extraction_job.is_finished():
            if self.logger:
                self.logger.info(f"Job {extraction_job.id} is already finished.")
            return extraction_job
        
        uow_factory = self.extraction_job_runner.extraction_uow_factory

        with uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            extraction_job.mark_in_progress()
            uow.extraction_job_repo.save(extraction_job)
            uow.commit()
        
        try:
            self.extraction_job_runner.run(extraction_job)

        except Exception as e:

            with uow_factory() as uow:
                uow = cast(ExtractionUnitOfWorkPort, uow)
                extraction_job.mark_failed()
                uow.extraction_job_repo.save(extraction_job)
                uow.commit()

            if self.logger:
                self.logger.error(f"Job {extraction_job.id} failed: {e}")

            raise e
        
        with uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            extraction_job.mark_completed()
            uow.extraction_job_repo.save(extraction_job)
            uow.commit()

        if self.logger:
            self.logger.info(f"Job {extraction_job.id} completed successfully.")

        return extraction_job