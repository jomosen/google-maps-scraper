from sqlalchemy.orm import Session
from extraction.domain.job_task import JobTask
from extraction.domain.repositories.job_task_repository import JobTaskRepository
from extraction.infrastructure.persistence.models.job_task_model import JobTaskModel
from extraction.infrastructure.persistence.mappers.job_task_persistence_mapper import JobTaskPersistenceMapper


class SqlAlchemyJobTaskRepository(JobTaskRepository):
    """SQLAlchemy implementation of the TaskRepository interface."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, task: JobTask) -> None:
        model = JobTaskPersistenceMapper.to_model(task)
        self.session.merge(model)
        self.session.commit()

    def find_by_id(self, task_id: str) -> JobTask | None:
        model = self.session.query(JobTaskModel).filter_by(id=task_id).first()
        if model:
            return JobTaskPersistenceMapper.to_entity(model)
        return None