

import pytest
from unittest.mock import Mock
from extraction.application.use_cases.run_extraction_job_use_case import RunExtractionUseCase
from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.extraction_job_config import ExtractionJobConfig
from extraction.domain.extraction_job_status import ExtractionJobStatus
from shared.application.ports.unit_of_work_port import UnitOfWorkPort


def test_run_extraction_use_case_failure():

    job = ExtractionJob.create("Job", ExtractionJobConfig())

    mock_repo = Mock()
    mock_uow = Mock(spec=UnitOfWorkPort)
    mock_uow.__enter__ = Mock(return_value=mock_uow)
    mock_uow.__exit__ = Mock(return_value=False)
    mock_uow.extraction_job_repo = mock_repo
    mock_uow.commit = Mock()
    mock_uow.rollback = Mock()

    def uow_factory():
        return mock_uow

    mock_runner = Mock()
    mock_runner.extraction_uow_factory = uow_factory

    # runner falla
    mock_runner.run.side_effect = Exception("boom")

    use_case = RunExtractionUseCase(mock_runner, logger=None)

    with pytest.raises(Exception):
        use_case.execute(job)

    # El estado final debe ser FAILED
    assert job.status == ExtractionJobStatus.FAILED

    # Se llama a save 2 veces: in_progress + failed
    assert mock_repo.save.call_count == 2
