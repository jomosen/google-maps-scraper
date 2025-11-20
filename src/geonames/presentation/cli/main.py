from pyfiglet import Figlet
from shared.infrastructure.logging.system_logger import SystemLogger
from geonames.infrastructure.persistence.database.factory import create_db_geonames_connector
from geonames.infrastructure.persistence.unit_of_work.sql_alchemy_geonames_unit_of_work import SqlAlchemyGeoNamesUnitOfWorkFactory
from geonames.presentation.cli.commands.import_geonames_command import import_geonames_command


def main():
    figlet = Figlet(font="slant")
    print(figlet.renderText("GeoNames Importer"))

    logger = SystemLogger()
    logger.info("Import process started")

    db_connector = create_db_geonames_connector(init_schema=True)
    uow_factory = SqlAlchemyGeoNamesUnitOfWorkFactory(db_connector)
    import_geonames_command(uow_factory, logger)
    logger.info("Import process finished")

if __name__ == "__main__":
    main()