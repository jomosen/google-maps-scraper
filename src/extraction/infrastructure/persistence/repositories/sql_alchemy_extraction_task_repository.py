from sqlalchemy.orm import Session
from extraction.domain.extraction_task import ExtractionTask
from extraction.domain.repositories.extraction_task_repository import ExtractionTaskRepository
from extraction.infrastructure.persistence.models.extraction_task_model import ExtractionTaskModel
from extraction.infrastructure.persistence.mappers.extraction_task_persistence_mapper import ExtractionTaskPersistenceMapper


class SqlAlchemyExtractionTaskRepository(ExtractionTaskRepository):
    """SQLAlchemy implementation of the TaskRepository interface."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, task: ExtractionTask) -> None:
        model = ExtractionTaskPersistenceMapper.to_model(task)
        self.session.merge(model)
        self.session.commit()

    def find_by_id(self, task_id: str) -> ExtractionTask | None:
        model = self.session.query(ExtractionTaskModel).filter_by(id=task_id).first()
        if model:
            return ExtractionTaskPersistenceMapper.to_domain(model)
        return None