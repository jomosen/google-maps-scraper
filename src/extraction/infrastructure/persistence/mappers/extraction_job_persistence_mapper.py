from extraction.domain.extraction_job import ExtractionJob
from extraction.infrastructure.persistence.models.extraction_job_model import ExtractionJobModel
from extraction.infrastructure.persistence.mappers.job_task_persistence_mapper import JobTaskPersistenceMapper
from extraction.domain.job_status import JobStatus
from extraction.domain.job_config import JobConfig


class ExtractionJobPersistenceMapper:
    """Maps ExtractionJob domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: ExtractionJobModel) -> ExtractionJob:
        """Converts a ExtractionJobModel to a ExtractionJob entity."""

        config = JobConfig(**model.config)

        return ExtractionJob(
            id=model.id,
            title=model.title,
            status=JobStatus(model.status),
            config=config,
            created_at=model.created_at,
            completed_at=model.completed_at,
            tasks=[JobTaskPersistenceMapper.to_entity(task) for task in model.tasks]
        )

    @staticmethod
    def to_model(entity: ExtractionJob) -> ExtractionJobModel:
        """Converts a ExtractionJob entity to a ExtractionJobModel."""

        model = ExtractionJobModel(
            id=entity.id,
            title=entity.title,
            config={
                "search_seeds": entity.config.search_seeds,
                "scope": entity.config.scope,
                "geoname_id": entity.config.geoname_id,
                "language_code": entity.config.language_code,
                "depth_level": entity.config.depth_level,
                "min_population": entity.config.min_population,
                "max_results": entity.config.max_results,
                "min_rating": entity.config.min_rating,
                "max_reviews": entity.config.max_reviews,
                "max_workers": entity.config.max_workers,
            },
            status=entity.status.value,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )

        model.tasks = []
        for task_entity in entity.tasks:
            task_model = JobTaskPersistenceMapper.to_model(task_entity)
            task_model.job = model
            model.tasks.append(task_model)

        return model
