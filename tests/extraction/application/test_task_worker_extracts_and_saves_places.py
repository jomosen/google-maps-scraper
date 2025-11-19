import pytest
from unittest.mock import Mock

from extraction.application.services.job_task_worker_service import JobTaskWorkerService
from extraction.domain.extraction_task import JobTask
from extraction.domain.extraction_job_config import ExtractionJobConfig


def test_task_worker_extracts_and_saves_places():

    # --- Arrange ---
    task = JobTask(id="1", job_id="1", search_seed="seed", geoname_id=123)
    job_config = ExtractionJobConfig()

    # Fake places returned by extractor
    fake_place_1 = Mock()
    fake_place_2 = Mock()
    fake_places = [fake_place_1, fake_place_2]

    # Mock place extractor
    mock_extractor = Mock()
    mock_extractor.extract.return_value = fake_places

    # Mock geonames lookup (you need it if worker expects it)
    mock_geonames_lookup = Mock()
    mock_geonames_lookup.find_by_geoname_id.return_value = Mock()

    # Mock places storage
    mock_storage = Mock()

    mock_uow = Mock()
    mock_uow.__enter__ = Mock(return_value=mock_uow)
    mock_uow.__exit__ = Mock(return_value=False)
    mock_uow.places_storage = Mock()   # este es el repo al que se llama
    mock_uow.commit = Mock()
    mock_uow.rollback = Mock()

    def uow_factory():
        return mock_uow

    # Mock logger
    mock_logger = Mock()

    # Worker under test
    worker = JobTaskWorkerService(
        job_tasks=[task],
        job_config=job_config,
        place_extractor=mock_extractor,
        places_storage=mock_storage,
        geonames_lookup=mock_geonames_lookup,
        extraction_uow_factory=uow_factory,
        logger=mock_logger
    )

    # --- Act ---
    worker.process()

    # --- Assert ---

    # 1. extract() was called once with the correct args
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0] == task

    # 2. places_storage.save() called twice (once per place)
    assert mock_storage.save.call_count == 2
    mock_storage.save.assert_any_call(fake_place_1)
    mock_storage.save.assert_any_call(fake_place_2)
