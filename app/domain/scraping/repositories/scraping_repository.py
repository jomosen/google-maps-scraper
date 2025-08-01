from abc import ABC, abstractmethod
from app.domain.scraping.entities.scraping import Scraping

class ScrapingRepository(ABC):
    @abstractmethod
    def save(self, scraping: Scraping) -> None:
        pass

    @abstractmethod
    def find_by_id(self, scraping_id: str) -> Scraping | None:
        pass