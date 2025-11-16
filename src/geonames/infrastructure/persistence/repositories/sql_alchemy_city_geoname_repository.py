from typing import Type
from sqlalchemy.orm import Session
from geonames.infrastructure.persistence.models.city_geoname_model import CityGeoNameModel
from .sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository


class SqlAlchemyCityGeoNameRepository(SqlAlchemyGeoNameRepository):

    def __init__(self, 
                 session: Session, 
                 model_class: Type[CityGeoNameModel] = CityGeoNameModel):
        
        self.session = session
        self.model_class = model_class