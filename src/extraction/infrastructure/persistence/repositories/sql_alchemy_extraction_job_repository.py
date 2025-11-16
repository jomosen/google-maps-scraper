from sqlalchemy.orm import Session
from extraction.domain.extraction_job import ExtractionJob
from extraction.domain.repositories.extraction_job_repository import ExtractionJobRepository
from extraction.infrastructure.persistence.models.extraction_job_model import ExtractionJobModel
from extraction.infrastructure.persistence.mappers.extraction_job_persistence_mapper import ExtractionJobPersistenceMapper


class SqlAlchemyExtractionJobRepository(ExtractionJobRepository):
    """SQLAlchemy implementation of the ScrapingRepository interface."""
    
    def __init__(self, session: Session):
        self.session = session

    def save(self, job: ExtractionJob) -> None:
        model = ExtractionJobPersistenceMapper.to_model(job)

        existing = self.session.get(ExtractionJobModel, job.id)
        if existing:
            self.session.merge(model)
        else:
            self.session.add(model)

        self.session.commit()

    def find_all(self) -> list[ExtractionJob]:
        models = self.session.query(ExtractionJobModel).all()
        return [ExtractionJobPersistenceMapper.to_entity(model) for model in models]

    def find_by_id(self, job_id: str) -> ExtractionJob | None:
        model = self.session.query(ExtractionJobModel).filter_by(id=job_id).first()
        if model:
            return ExtractionJobPersistenceMapper.to_entity(model)
        return None
    
    def find_by_status(self, status: str) -> list[ExtractionJob]:
        models = self.session.query(ExtractionJobModel).filter_by(status=status).all()
        return [ExtractionJobPersistenceMapper.to_entity(model) for model in models]
    
    def delete(self, id: str) -> None:
        model = self.session.query(ExtractionJobModel).filter_by(id=id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
