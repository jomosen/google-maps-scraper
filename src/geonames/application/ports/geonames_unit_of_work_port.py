from abc import ABC, abstractmethod

from geonames.domain.repositories.alternatename_repository import AlternateNameRepository
from geonames.domain.repositories.country_geoname_repository import CountryGeoNameRepository
from geonames.domain.repositories.geoname_repository import GeoNameRepository
from shared.application.ports.unit_of_work_port import UnitOfWorkPort

class GeoNamesUnitOfWorkPort(UnitOfWorkPort, ABC):

    geoname_repo: "GeoNameRepository"
    country_geoname_repo: "CountryGeoNameRepository"
    alternate_name_repo: "AlternateNameRepository"
    admin_geoname_repo: "GeoNameRepository"
    city_geoname_repo: "GeoNameRepository"
