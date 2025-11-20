from typing import List, Optional, cast

from geonames.domain.country import Country
from geonames.domain.geoname import GeoName
from geonames.domain.repositories.country_geoname_repository import CountryGeoNameRepository
from geonames.domain.repositories.geoname_repository import GeoNameRepository
from geonames.application.ports.geonames_unit_of_work_port import GeoNamesUnitOfWorkFactoryPort, GeoNamesUnitOfWorkPort


class GeoNameNotFoundError(Exception):
    """Exception raised when a GeoName is not found."""
    pass

class GeoNameQueryService:

    def __init__(self, uow_factory: GeoNamesUnitOfWorkFactoryPort, logger=None):
        self.uow_factory = uow_factory
        self.logger = logger

    def get_geoname(self, geoname_id: int):
        with self.uow_factory() as uow:
            uow = cast(GeoNamesUnitOfWorkPort, uow)
            repo: GeoNameRepository = uow.geoname_repo

            geoname = repo.find_by_id(geoname_id)
            if not geoname:
                raise GeoNameNotFoundError(geoname_id)
            return geoname
        
    def get_admin_geonames(self, filters: dict) -> List[GeoName]:
        with self.uow_factory() as uow:
            uow = cast(GeoNamesUnitOfWorkPort, uow)
            repo: GeoNameRepository = uow.admin_geoname_repo

            geonames = repo.find_all(filters)
            return geonames
        
    def get_city_geonames(self, filters: dict) -> List[GeoName]:
        with self.uow_factory() as uow:
            uow = cast(GeoNamesUnitOfWorkPort, uow)
            repo: GeoNameRepository = uow.city_geoname_repo

            geonames = repo.find_all(filters)
            return geonames
        
    def get_country(self, geoname_id: int):
        with self.uow_factory() as uow:
            uow = cast(GeoNamesUnitOfWorkPort, uow)
            repo: CountryGeoNameRepository = uow.country_geoname_repo

            country = repo.find_by_id(geoname_id)
            if not country:
                raise GeoNameNotFoundError(geoname_id)
            return country
        
    def get_countries(self, filters: dict) -> List[Country]:
        with self.uow_factory() as uow:
            uow = cast(GeoNamesUnitOfWorkPort, uow)
            repo: CountryGeoNameRepository = uow.country_geoname_repo

            countries = repo.find_all(filters)
            return countries
