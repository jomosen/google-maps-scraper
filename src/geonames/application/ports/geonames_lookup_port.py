from typing import Protocol, Optional
from geonames.domain.geoname import GeoName


class GeoNamesLookupPort(Protocol):
    """
    Port for retrieving a Geoname entry from any source (DB, API, cache...).
    Used by the extraction bounded context to enrich places.
    """

    def find_by_geoname_id(self, geoname_id: int) -> Optional[GeoName]:
        """
        Return the corresponding Geoname or None if not found.
        """
        ...
