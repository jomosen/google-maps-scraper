from typing import List
from app.domain.scraping.entities.scraping import Scraping
from app.domain.scraping.entities.task import Task

class TaskGenerator:
    @staticmethod
    def generate(scraping: Scraping) -> List[Task]:
        return [
            Task.build(
                scraping_id=scraping.id,
                keyword=keyword,
                location=location
            )
            for keyword in scraping.options.keywords
            for location in scraping.options.locations
        ]

