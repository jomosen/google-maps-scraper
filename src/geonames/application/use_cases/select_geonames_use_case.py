from typing import Any, List
from shared.application.contracts.abstract_logger import AbstractLogger
from geonames.domain.geoname import GeoName
from geonames.domain.geoname_selection_service import GeoNameSelectionService


class SelectGeoNamesUseCase:

    def __init__(self, 
                 service: GeoNameSelectionService, 
                 logger: AbstractLogger | None = None):
        
        self.service = service
        self.logger = logger

    def execute(self, filters: dict[str, Any]) -> List[GeoName]:

        try:
            geonames = self.service.select(filters)
            return geonames

        except Exception as e:
            if self.logger:
                self.logger.error(e)
            raise e