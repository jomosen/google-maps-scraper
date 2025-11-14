from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from src.geonames.domain.geoname import GeoName


class AbstractGeoNameRepository(ABC):

    @abstractmethod
    def find_by_id(self, geoname_id: int) -> Optional[GeoName]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[GeoName]:
        pass

    @abstractmethod
    def save(self, entity: GeoName) -> None:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[GeoName]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None:
        pass
