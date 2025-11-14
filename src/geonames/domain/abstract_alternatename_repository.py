from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from src.geonames.domain.alternatename import AlternateName


class AbstractAlternateNameRepository(ABC):

    @abstractmethod
    def find_by_id(self, geoname_id: int) -> Optional[AlternateName]:
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict] = None) -> List[AlternateName]:
        pass

    @abstractmethod
    def save(self, entity: AlternateName) -> None:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def bulk_insert(self, entities: List[AlternateName]) -> None:
        pass

    @abstractmethod
    def truncate(self) -> None: 
        pass
