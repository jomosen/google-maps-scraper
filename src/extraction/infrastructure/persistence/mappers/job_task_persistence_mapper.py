from extraction.domain.job_task import JobTask
from extraction.infrastructure.persistence.models.job_task_model import JobTaskModel
from extraction.domain.job_status import JobStatus


class JobTaskPersistenceMapper:
    """Maps JobTask domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: JobTaskModel) -> JobTask:
        """Converts a JobTaskModel to a JobTask entity."""

        return JobTask(
            id=model.id,
            job_id=model.job_id,
            search_seed=model.search_seed,
            geoname_id=model.geoname_id,
            status=JobStatus(model.status),
            created_at=model.created_at,
            completed_at=model.completed_at
        )

    @staticmethod
    def to_model(entity: JobTask) -> JobTaskModel:
        """Converts a JobTask entity to a JobTaskModel."""

        return JobTaskModel(
            id=entity.id,
            job_id=entity.job_id,
            search_seed=entity.search_seed,
            geoname_id=entity.geoname_id,
            status=entity.status.value,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )
