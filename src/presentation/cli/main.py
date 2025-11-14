from datetime import date
from pyfiglet import Figlet
from src.infrastructure.persistence.repositories.sql_alchemy_admin_geoname_repository import SqlAlchemyAdminGeoNameRepository
from src.infrastructure.persistence.models.admin_geoname_model import AdminGeoNameModel
from src.infrastructure.logging.system_logger import SystemLogger
from src.infrastructure.persistence.database.mysql_connector import MySQLConnector
from src.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work_factory import SqlAlchemyUnitOfWorkFactory
from src.presentation.cli.commands.import_geonames_command import import_geonames_command


def main():
    figlet = Figlet(font="slant")
    print(figlet.renderText("GeoNames Importer"))

    logger = SystemLogger()
    logger.info("Import process started")

    db_connector = MySQLConnector(logger)
    db_connector.init_db()
    uow_factory = SqlAlchemyUnitOfWorkFactory(db_connector)

    import_geonames_command(uow_factory, logger)

    logger.info("Import process finished")

if __name__ == "__main__":
    main()