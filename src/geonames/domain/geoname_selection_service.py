from typing import List, Any
from src.geonames.domain.geoname import GeoName
from src.geonames.domain.abstract_geoname_repository import AbstractGeoNameRepository
from src.geonames.domain.abstract_country_geoname_repository import AbstractCountryGeoNameRepository


class GeoNameSelectionService:
    
    def __init__(self, 
                 geoname_repository: AbstractGeoNameRepository, 
                 country_repository: AbstractCountryGeoNameRepository):
        
        self.geoname_repository = geoname_repository
        self.country_repository = country_repository

    def select(self, filters: dict[str, Any]) -> List[GeoName]:

        try:
            if not filters:
                return []
        
            geonames = []

            if filters.get("scope") == "country" and filters.get("geoname_id"):
                country = self.country_repository.find_by_id(filters.get("geoname_id"))
                if not country:
                    return filters

                filters["country_code"] = country.iso_alpha2

                if filters.get("depth_level") == "admin1":
                    filters["feature_code"] = "ADM1"
                elif filters.get("depth_level") == "admin2":
                    filters["feature_code"] = "ADM2"
                elif filters.get("depth_level") == "admin3":
                    filters["feature_code"] = "ADM3"
                else:
                    filters["feature_class"] = "P"
                    filters["min_population"] = filters.get("min_population")
                
            geonames = self.geoname_repository.find_all(filters)
        except Exception as e:
            raise e
        
        return geonames
