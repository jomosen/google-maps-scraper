from abc import ABC, abstractmethod
from app.domain.place.entities.place import Place

class PlaceRepository(ABC):
    @abstractmethod
    def save(self, place: Place) -> None:
        pass

    @abstractmethod
    def find_by_scraping_id(self, scraping_id: str) -> list[Place]:
        pass