from app.domain.scraping.entities.scraping import Scraping
from app.domain.scraping.value_objects.status_vo import StatusVO
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO
from app.domain.scraping.repositories.scraping_repository import ScrapingRepository
from app.application.scraping.services.task_generator import TaskGenerator
from datetime import datetime
import uuid

def create_scraping(options: ScrapingOptionsVO, repository: ScrapingRepository, task_generator: TaskGenerator) -> Scraping:
    scraping = Scraping(
        id=str(uuid.uuid4()),
        options=options,
        status=StatusVO.pending(),
        created_at=datetime.utcnow()
    )

    scraping.tasks = task_generator.generate(scraping)

    repository.save(scraping)
    return scraping
