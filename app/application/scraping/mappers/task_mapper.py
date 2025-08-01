from app.domain.scraping.entities.task import Task
from app.infrastructure.persistence.models.task_model import TaskModel
from app.domain.scraping.value_objects.status_vo import StatusVO

class TaskMapper:
    @staticmethod
    def to_entity(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            scraping_id=model.scraping_id,
            keyword=model.keyword,
            location=model.location,
            status=StatusVO(model.status),
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: Task) -> TaskModel:
        return TaskModel(
            id=entity.id,
            scraping_id=entity.scraping_id,
            keyword=entity.keyword,
            location=entity.location,
            status=entity.status.value,
            created_at=entity.created_at
        )
    
    @staticmethod
    def to_gmaps_query(task: Task,) -> str:
        return f"{task.keyword} in {task.location}"
