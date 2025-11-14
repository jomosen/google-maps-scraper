from src.infrastructure.logging.system_logger import SystemLogger
from src.infrastructure.persistence.database.mysql_connector import MySQLConnector
from src.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work_factory import SqlAlchemyUnitOfWorkFactory

logger = SystemLogger()
db_connector = MySQLConnector(logger)
db_connector.init_db()
uow_factory = SqlAlchemyUnitOfWorkFactory(db_connector)

def get_uow_factory():
    return uow_factory