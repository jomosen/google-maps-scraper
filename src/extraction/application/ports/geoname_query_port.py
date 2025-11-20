from typing import List, Dict, Any
from extraction.domain.value_objects.country import Country
from extraction.domain.value_objects.geoname import GeoName
from typing import Protocol


class GeoNameQueryPort(Protocol):
    """Port to query geographic areas from GeoNames."""

    def find_geoname_by_id(self, geoname_id: int) -> GeoName:
        ...

    def find_admin_geonames(self, filters: Dict[str, Any]) -> List[GeoName]:
        ...

    def find_city_geonames(self, filters: Dict[str, Any]) -> List[GeoName]:
        ...

    def find_country_by_id(self, geoname_id: int) -> Country:
        ...

    def find_countries(self, filters: Dict[str, Any]) -> List[Country]:
        ...
