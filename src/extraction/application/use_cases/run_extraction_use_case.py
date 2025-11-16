from shared.application.ports.logger_port import LoggerPort
from shared.application.use_case import UseCase
from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService


class RunExtractionUseCase(UseCase):

    def __init__(self, extraction_job_runner: ExtractionJobRunnerService, logger: LoggerPort = None):
        self.extraction_job_runner = extraction_job_runner
        self.logger = logger

    def execute(self):
        pass