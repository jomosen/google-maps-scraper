from geonames.infrastructure.persistence.database.factory import create_geonames_connector
from shared.infrastructure.logging.system_logger import SystemLogger
from geonames.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work_factory import SqlAlchemyUnitOfWorkFactory

logger = SystemLogger()

db_connector = create_geonames_connector(init_schema=True)
uow_factory = SqlAlchemyUnitOfWorkFactory(db_connector)

def get_uow_factory():
    return uow_factory