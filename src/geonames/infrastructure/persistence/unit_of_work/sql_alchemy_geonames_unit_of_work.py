from geonames.application.ports.geonames_unit_of_work_port import GeoNamesUnitOfWorkPort
from shared.application.ports.unit_of_work_port import UnitOfWorkFactoryPort
from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector


class SqlAlchemyGeoNamesUnitOfWork(GeoNamesUnitOfWorkPort):

    def __init__(self, 
                 session_factory, 
                 geoname_repo_cls, 
                 country_geoname_repo_cls, 
                 geoname_alternatename_repo_cls, 
                 admin_geoname_repo_cls, 
                 city_geoname_repo_cls):
        
        self._session_factory = session_factory
        self._geoname_repo_cls = geoname_repo_cls
        self._country_geoname_repo_cls = country_geoname_repo_cls
        self._geoname_alternatename_repo_cls = geoname_alternatename_repo_cls
        self._admin_geoname_repo_cls = admin_geoname_repo_cls
        self._city_geoname_repo_cls = city_geoname_repo_cls

        self.session = None
        self.geoname_repo = None
        self.country_geoname_repo = None
        self.geoname_alternatename_repo = None
        self.admin_geoname_repo = None
        self.city_geoname_repo = None

    def __enter__(self):
        self.session = self._session_factory()
        self.geoname_repo = self._geoname_repo_cls(self.session)
        self.country_geoname_repo = self._country_geoname_repo_cls(self.session)
        self.geoname_alternatename_repo = self._geoname_alternatename_repo_cls(self.session)
        self.admin_geoname_repo = self._admin_geoname_repo_cls(self.session)
        self.city_geoname_repo = self._city_geoname_repo_cls(self.session)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SqlAlchemyGeoNamesUnitOfWorkFactory(UnitOfWorkFactoryPort):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def __call__(self) -> SqlAlchemyGeoNamesUnitOfWork:

        from geonames.infrastructure.persistence.repositories.sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository
        from geonames.infrastructure.persistence.repositories.sql_alchemy_alternatename_repository import SqlAlchemyAlternateNameRepository
        from geonames.infrastructure.persistence.repositories.sql_alchemy_country_geoname_repository import SqlAlchemyCountryGeoNameRepository
        from geonames.infrastructure.persistence.repositories.sql_alchemy_admin_geoname_repository import SqlAlchemyAdminGeoNameRepository
        from geonames.infrastructure.persistence.repositories.sql_alchemy_city_geoname_repository import SqlAlchemyCityGeoNameRepository

        return SqlAlchemyGeoNamesUnitOfWork(
            session_factory=self.connector.get_session,
            geoname_repo_cls=SqlAlchemyGeoNameRepository,
            country_geoname_repo_cls=SqlAlchemyCountryGeoNameRepository,
            geoname_alternatename_repo_cls=SqlAlchemyAlternateNameRepository,
            admin_geoname_repo_cls=SqlAlchemyAdminGeoNameRepository,
            city_geoname_repo_cls=SqlAlchemyCityGeoNameRepository,
        )
