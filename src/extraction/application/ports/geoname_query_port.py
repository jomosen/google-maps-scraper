from typing import List, Dict, Any
from extraction.domain.value_objects.search_point import SearchPoint
from typing import Protocol


class GeoNameQueryPort(Protocol):
    """Port to query geographic search points from GeoNames."""

    def find_search_point_by_geoname_id(self, geoname_id: int) -> SearchPoint:
        ...

    def find_search_points_for_admins(self, filters: Dict[str, Any]) -> List[SearchPoint]:
        ...

    def find_search_points_for_cities(self, filters: Dict[str, Any]) -> List[SearchPoint]:
        ...
