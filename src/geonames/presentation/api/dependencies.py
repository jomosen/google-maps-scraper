from geonames.application.services.geoname_query_service import GeoNameQueryService
from geonames.infrastructure.persistence.database.factory import create_db_geonames_connector
from geonames.infrastructure.persistence.unit_of_work.sql_alchemy_geonames_unit_of_work import SqlAlchemyGeoNamesUnitOfWorkFactory
from shared.infrastructure.logging.system_logger import SystemLogger

logger = SystemLogger()

db_connector = create_db_geonames_connector(init_schema=True)
uow_factory = SqlAlchemyGeoNamesUnitOfWorkFactory(db_connector)


def get_uow_factory() -> SqlAlchemyGeoNamesUnitOfWorkFactory:
    return uow_factory

def get_geoname_query_service() -> GeoNameQueryService:
    return GeoNameQueryService(uow_factory=uow_factory, logger=logger)