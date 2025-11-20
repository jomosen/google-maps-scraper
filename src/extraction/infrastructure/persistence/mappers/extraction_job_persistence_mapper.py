from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.value_objects.geoname_selection_params_for_extraction_job import GeoNameSelectionParamsForExtractionJob
from extraction.infrastructure.persistence.models.extraction_job_model import ExtractionJobModel
from extraction.infrastructure.persistence.mappers.extraction_task_persistence_mapper import ExtractionTaskPersistenceMapper
from extraction.domain.enums.extraction_job_status import ExtractionJobStatus
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig


class ExtractionJobPersistenceMapper:
    """Maps ExtractionJob domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: ExtractionJobModel) -> ExtractionJob:
        """Converts a ExtractionJobModel to a ExtractionJob entity."""

        cfg = model.config

        geoname_params = GeoNameSelectionParamsForExtractionJob(
            scope=cfg["geoname_selection_params"]["scope"],
            scope_geoname_id=cfg["geoname_selection_params"]["scope_geoname_id"],
            depth_level=cfg["geoname_selection_params"]["depth_level"],
            min_population=cfg["geoname_selection_params"]["min_population"],
        )

        config = ExtractionJobConfig(
            search_seeds=cfg["search_seeds"],
            geoname_selection_params=geoname_params,
            locale=cfg["locale"],
            max_results=cfg["max_results"],
            min_rating=cfg["min_rating"],
            max_reviews=cfg["max_reviews"],
            max_workers=cfg["max_workers"],
        )

        return ExtractionJob(
            id=model.id,
            title=model.title,
            status=ExtractionJobStatus(model.status),
            config=config,
            total_tasks=model.total_tasks,
            completed_tasks=model.completed_tasks,
            failed_tasks=model.failed_tasks,
            created_at=model.created_at,
            completed_at=model.completed_at,
            tasks=[ExtractionTaskPersistenceMapper.to_domain(task) for task in model.tasks]
        )

    @staticmethod
    def to_model(entity: ExtractionJob) -> ExtractionJobModel:
        """Converts a ExtractionJob entity to a ExtractionJobModel."""

        geoname_selection_params = entity.config.geoname_selection_params

        model = ExtractionJobModel(
            id=entity.id,
            title=entity.title,
            config={
                "search_seeds": entity.config.search_seeds,
                "geoname_selection_params": {
                    "scope": geoname_selection_params.scope,
                    "scope_geoname_id": geoname_selection_params.scope_geoname_id,
                    "depth_level": geoname_selection_params.depth_level,
                    "min_population": geoname_selection_params.min_population,
                },
                "locale": entity.config.locale,
                "max_results": entity.config.max_results,
                "min_rating": entity.config.min_rating,
                "max_reviews": entity.config.max_reviews,
                "max_workers": entity.config.max_workers,
            },
            total_tasks=entity.total_tasks,
            completed_tasks=entity.completed_tasks,
            failed_tasks=entity.failed_tasks,
            status=entity.status.value,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )

        model.tasks = []
        for task_entity in entity.tasks:
            task_model = ExtractionTaskPersistenceMapper.to_model(task_entity)
            task_model.job = model
            model.tasks.append(task_model)

        return model
