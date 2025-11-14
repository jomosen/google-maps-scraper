from src.infrastructure.persistence.repositories.sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository
from src.infrastructure.persistence.models.city_geoname_model import CityGeoNameModel


class SqlAlchemyCityGeoNameRepository(SqlAlchemyGeoNameRepository):

    def __init__(self, session):
        super().__init__(session, model_class=CityGeoNameModel)