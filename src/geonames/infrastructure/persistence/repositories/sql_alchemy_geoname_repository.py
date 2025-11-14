from typing import Generic, List, Optional, Dict, Type, TypeVar
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.geonames.domain.abstract_geoname_repository import AbstractGeoNameRepository
from src.geonames.domain.geoname import GeoName
from src.geonames.infrastructure.persistence.models.geoname_model import GeoNameModel
from src.geonames.infrastructure.persistence.mappers.geoname_persistence_mapper import GeoNamePersistenceMapper


class SqlAlchemyGeoNameRepository(AbstractGeoNameRepository):

    def __init__(self, 
                 session: Session, 
                 model_class: Type[GeoNameModel] = GeoNameModel):
        
        self.session = session
        self.model_class = model_class

    def find_by_id(self, geoname_id: int) -> Optional[GeoName]:
        record = self.session.get(self.model_class, geoname_id)
        return GeoNamePersistenceMapper.to_entity(record, model_class=self.model_class) if record else None

    def find_all(self, filters: Optional[Dict] = None) -> List[GeoName]:
        filters = filters or {}
        query = self.session.query(self.model_class)

        if "country_code" in filters and filters["country_code"]:
            query = query.filter(self.model_class.country_code == filters["country_code"])
        if "admin1_code" in filters and filters["admin1_code"]:
            query = query.filter(self.model_class.admin1_code == filters["admin1_code"])
        if "admin2_code" in filters and filters["admin2_code"]:
            query = query.filter(self.model_class.admin2_code == filters["admin2_code"])
        if "admin3_code" in filters and filters["admin3_code"]:
            query = query.filter(self.model_class.admin3_code == filters["admin3_code"])
        if "admin4_code" in filters and filters["admin4_code"]:
            query = query.filter(self.model_class.admin4_code == filters["admin4_code"])
        if "min_population" in filters and filters["min_population"]:
            query = query.filter(self.model_class.population >= filters["min_population"])
        if "max_population" in filters and filters["max_population"]:
            query = query.filter(self.model_class.population <= filters["max_population"])
        if "feature_class" in filters and filters["feature_class"]:
            query = query.filter(self.model_class.feature_class == filters["feature_class"])
        if "feature_code" in filters and filters["feature_code"]:
            query = query.filter(self.model_class.feature_code == filters["feature_code"])
        if "name_like" in filters and filters["name_like"]:
            query = query.filter(self.model_class.name.ilike(f"%{filters['name_like']}%"))
        if "timezone" in filters and filters["timezone"]:
            query = query.filter(self.model_class.timezone == filters["timezone"])

        return [GeoNamePersistenceMapper.to_entity(r, model_class=self.model_class) for r in query.all()]
    
    def save(self, entity: GeoName) -> None:
        model = GeoNamePersistenceMapper.to_model(entity, model_class=self.model_class)
        existing = self.session.get(self.model_class, model.geoname_id)
        if existing:
            for attr, value in vars(model).items():
                if hasattr(existing, attr):
                    setattr(existing, attr, value)
        else:
            self.session.add(model)

        self.session.commit()

    def count_all(self) -> int:
        count = self.session.query(self.model_class).count()
        return count
    
    def bulk_insert(self, entities: List[GeoName]) -> None:
        models = [GeoNamePersistenceMapper.to_model(entity, model_class=self.model_class) for entity in entities]
        self.session.bulk_save_objects(models)
        self.session.commit()

    def truncate(self):
        table_name = self.model_class.__tablename__
        self.session.execute(text(f"TRUNCATE TABLE {table_name}"))
        self.session.commit()
