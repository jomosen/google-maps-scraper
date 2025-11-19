from geonames.application.services.geoname_query_service import GeoNameQueryService
from geonames.infrastructure.persistence.database.factory import create_geonames_connector
from geonames.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWorkFactory
from shared.infrastructure.logging.system_logger import SystemLogger

logger = SystemLogger()

db_connector = create_geonames_connector(init_schema=True)
uow_factory = SqlAlchemyUnitOfWorkFactory(db_connector)


def get_uow_factory() -> SqlAlchemyUnitOfWorkFactory:
    return uow_factory

def get_geoname_query_service() -> GeoNameQueryService:
    return GeoNameQueryService(uow_factory=uow_factory, logger=logger)