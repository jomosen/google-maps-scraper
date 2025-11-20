from typing import cast

from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from extraction.domain.extraction_job import ExtractionJob
from shared.application.ports.logger_port import LoggerPort
from shared.application.use_case import UseCase
from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService


class RunExtractionJobUseCase(UseCase):

    def __init__(self, 
                 extraction_job_runner: ExtractionJobRunnerService, 
                 logger: LoggerPort = None):
        
        self.extraction_job_runner = extraction_job_runner
        self.logger = logger

    def execute(self, job: ExtractionJob) -> ExtractionJob:

        if self.logger:
            self.logger.info(f"Starting job {job.id}...")

        if job.is_finished():
            if self.logger:
                self.logger.info(f"Job {job.id} is already finished.")
            return job
        
        uow_factory = self.extraction_job_runner.extraction_uow_factory

        with uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            job.mark_in_progress()
            uow.extraction_job_repo.save(job)
            uow.commit()
        
        try:
            self.extraction_job_runner.run(job)

        except Exception as e:

            with uow_factory() as uow:
                uow = cast(ExtractionUnitOfWorkPort, uow)
                job.mark_failed()
                uow.extraction_job_repo.save(job)
                uow.commit()

            if self.logger:
                self.logger.error(f"Job {job.id} failed: {e}")

            raise e
        
        with uow_factory() as uow:
            uow = cast(ExtractionUnitOfWorkPort, uow)
            job.mark_completed()
            uow.extraction_job_repo.save(job)
            uow.commit()

        if self.logger:
            self.logger.info(f"Job {job.id} completed successfully.")

        return job