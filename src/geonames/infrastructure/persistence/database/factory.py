import os
from dotenv import load_dotenv

from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector
from geonames.infrastructure.persistence.database.base import GeoNamesBase

load_dotenv()


def create_geonames_connector(init_schema: bool = False) -> MySQLConnector:
    db_url = os.environ["GEONAMES_DB_URL"]
    connector = MySQLConnector(db_url)

    if init_schema:
        import geonames.infrastructure.persistence.models

        GeoNamesBase.metadata.create_all(bind=connector.engine)

    return connector
