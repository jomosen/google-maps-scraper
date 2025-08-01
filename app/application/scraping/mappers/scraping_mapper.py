from app.domain.scraping.entities.scraping import Scraping
from app.infrastructure.persistence.models.scraping_model import ScrapingModel
from app.application.scraping.mappers.task_mapper import TaskMapper
from app.domain.scraping.value_objects.status_vo import StatusVO
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO

class ScrapingMapper:
    @staticmethod
    def to_entity(model: ScrapingModel) -> Scraping:
        keywords = list({task.keyword for task in model.tasks})
        locations = list({task.location for task in model.tasks})

        options = ScrapingOptionsVO(
            keywords=keywords,
            locations=locations,
            language=model.language,
            max_reviews=model.max_reviews
        )

        return Scraping(
            id=model.id,
            options=options,
            created_at=model.created_at,
            status=StatusVO(model.status),
            tasks=[TaskMapper.to_entity(task) for task in model.tasks]
        )

    @staticmethod
    def to_model(entity: Scraping) -> ScrapingModel:
        model = ScrapingModel(
            id=entity.id,
            language=entity.options.language,
            max_reviews=entity.options.max_reviews,
            status=entity.status.value,
            created_at=entity.created_at
        )

        model.tasks = [TaskMapper.to_model(task) for task in entity.tasks]
        return model
