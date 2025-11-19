from typing import Protocol, List, Dict, Any
from extraction.domain.value_objects.search_point import SearchPoint


class SearchPointSelectionPort(Protocol):

    def select(self, filters: Dict[str, Any]) -> List[SearchPoint]:
        ...
