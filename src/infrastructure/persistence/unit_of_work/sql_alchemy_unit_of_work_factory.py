from src.application.contracts.abstract_unit_of_work_factory import AbstractUnitOfWorkFactory
from src.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.persistence.database.mysql_connector import MySQLConnector
from src.infrastructure.persistence.repositories.sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository
from src.infrastructure.persistence.repositories.sql_alchemy_alternatename_repository import SqlAlchemyAlternateNameRepository
from src.infrastructure.persistence.repositories.sql_alchemy_country_geoname_repository import SqlAlchemyCountryGeoNameRepository
from src.infrastructure.persistence.repositories.sql_alchemy_admin_geoname_repository import SqlAlchemyAdminGeoNameRepository
from src.infrastructure.persistence.repositories.sql_alchemy_city_geoname_repository import SqlAlchemyCityGeoNameRepository


class SqlAlchemyUnitOfWorkFactory(AbstractUnitOfWorkFactory):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def __call__(self) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(
            session_factory=self.connector.get_session,
            geoname_repo_cls=SqlAlchemyGeoNameRepository,
            country_geoname_repo_cls=SqlAlchemyCountryGeoNameRepository,
            geoname_alternatename_repo_cls=SqlAlchemyAlternateNameRepository,
            admin_geoname_repo_cls=SqlAlchemyAdminGeoNameRepository,
            city_geoname_repo_cls=SqlAlchemyCityGeoNameRepository,
        )
