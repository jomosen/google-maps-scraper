from src.infrastructure.persistence.repositories.sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository
from src.infrastructure.persistence.models.admin_geoname_model import AdminGeoNameModel


class SqlAlchemyAdminGeoNameRepository(SqlAlchemyGeoNameRepository):

    def __init__(self, session):
        super().__init__(session, model_class=AdminGeoNameModel)
