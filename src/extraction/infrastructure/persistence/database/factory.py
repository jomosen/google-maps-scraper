import os
from dotenv import load_dotenv

from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector
from .base import ExtractionBase as Base

load_dotenv()


def create_extraction_connector(init_schema: bool = False) -> MySQLConnector:
    db_url = os.environ["EXTRACTION_DB_URL"]
    connector = MySQLConnector(db_url)

    if init_schema:
        import extraction.infrastructure.persistence.models

        Base.metadata.create_all(bind=connector.engine)

    return connector
