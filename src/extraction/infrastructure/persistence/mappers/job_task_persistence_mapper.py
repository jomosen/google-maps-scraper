from extraction.domain.extraction_task import ExtractionTask, JobTask
from extraction.infrastructure.persistence.models.extraction_task_model import ExtractionTaskModel
from extraction.domain.extraction_job_status import ExtractionJobStatus


class ExtractionTaskPersistenceMapper:
    """Maps ExtractionTask domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: ExtractionTaskModel) -> ExtractionTask:
        """Converts a ExtractionTaskModel to a ExtractionTask entity."""

        return ExtractionTask(
            id=model.id,
            job_id=model.job_id,
            search_seed=model.search_seed,
            geoname_id=model.geoname_id,
            status=ExtractionJobStatus(model.status),
            created_at=model.created_at,
            completed_at=model.completed_at
        )

    @staticmethod
    def to_model(entity: ExtractionTask) -> ExtractionTaskModel:
        """Converts a ExtractionTask entity to a ExtractionTaskModel."""

        return ExtractionTaskModel(
            id=entity.id,
            job_id=entity.job_id,
            search_seed=entity.search_seed,
            geoname_id=entity.geoname_id,
            status=entity.status.value,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )
