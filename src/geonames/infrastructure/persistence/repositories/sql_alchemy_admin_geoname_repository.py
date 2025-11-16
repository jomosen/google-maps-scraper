from typing import Type
from sqlalchemy.orm import Session
from geonames.infrastructure.persistence.models.admin_geoname_model import AdminGeoNameModel
from .sql_alchemy_geoname_repository import SqlAlchemyGeoNameRepository


class SqlAlchemyAdminGeoNameRepository(SqlAlchemyGeoNameRepository):

    def __init__(self, 
                 session: Session, 
                 model_class: Type[AdminGeoNameModel] = AdminGeoNameModel):
        
        self.session = session
        self.model_class = model_class
