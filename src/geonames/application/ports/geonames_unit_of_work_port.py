from abc import abstractmethod

from geonames.domain.repositories.alternatename_repository import AlternateNameRepository
from geonames.domain.repositories.country_geoname_repository import CountryGeoNameRepository
from geonames.domain.repositories.geoname_repository import GeoNameRepository
from shared.application.ports.unit_of_work_port import UnitOfWorkFactoryPort, UnitOfWorkPort


class GeoNamesUnitOfWorkPort(UnitOfWorkPort):

    geoname_repo: "GeoNameRepository"
    country_geoname_repo: "CountryGeoNameRepository"
    alternate_name_repo: "AlternateNameRepository"
    admin_geoname_repo: "GeoNameRepository"
    city_geoname_repo: "GeoNameRepository"

class GeoNamesUnitOfWorkFactoryPort(UnitOfWorkFactoryPort):

    @abstractmethod
    def __call__(self) -> "GeoNamesUnitOfWorkPort":
        raise NotImplementedError
