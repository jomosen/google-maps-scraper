from extraction.domain.extraction_task import ExtractionTask
from extraction.domain.value_objects.geoname import GeoName
from extraction.infrastructure.persistence.models.extraction_task_model import ExtractionTaskModel
from extraction.domain.enums.extraction_job_status import ExtractionJobStatus


class ExtractionTaskPersistenceMapper:

    @staticmethod
    def to_domain(model: ExtractionTaskModel) -> ExtractionTask:

        return ExtractionTask(
            id=model.id,
            job_id=model.job_id,
            search_seed=model.search_seed,
            geoname=GeoName(
                name=model.geoname_name,
                latitude=model.geoname_latitude,
                longitude=model.geoname_longitude,
                country_code=model.geoname_country_code
            ),
            status=ExtractionJobStatus(model.status),
            created_at=model.created_at,
            completed_at=model.completed_at
        )

    @staticmethod
    def to_model(entity: ExtractionTask) -> ExtractionTaskModel:

        return ExtractionTaskModel(
            id=entity.id,
            job_id=entity.job_id,
            search_seed=entity.search_seed,
            geoname_name=entity.geoname.name,
            geoname_latitude=entity.geoname.latitude,
            geoname_longitude=entity.geoname.longitude,
            geoname_country_code=entity.geoname.country_code,
            status=entity.status.value,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )
