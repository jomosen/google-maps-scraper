from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from geonames.domain.alternatename import AlternateName
from geonames.domain.repositories.alternatename_repository import AlternateNameRepository
from geonames.infrastructure.persistence.models.alternatename_model import AlternateNameModel
from geonames.infrastructure.persistence.mappers.alternatename_persistence_mapper import AlternateNamePersistenceMapper


class SqlAlchemyAlternateNameRepository(AlternateNameRepository):

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, alternate_name_id: int) -> Optional[AlternateName]:
        model = (
            self.session.query(AlternateNameModel)
            .filter_by(alternate_name_id=alternate_name_id)
            .first()
        )
        return AlternateNamePersistenceMapper.to_entity(model) if model else None
    
    def find_all(self, filters: Optional[dict] = None) -> List[AlternateName]:
        query = self.session.query(AlternateNameModel)

        if filters:
            if "geoname_id" in filters and filters["geoname_id"]:
                query = query.filter(AlternateNameModel.geoname_id == filters["geoname_id"])
            if "iso_language" in filters and filters["iso_language"]:
                query = query.filter(AlternateNameModel.iso_language == filters["iso_language"])
            if "is_preferred_name" in filters and filters["is_preferred_name"]:
                query = query.filter(AlternateNameModel.is_preferred_name == filters["is_preferred_name"])
            if "is_short_name" in filters and filters["is_short_name"]:
                query = query.filter(AlternateNameModel.is_short_name == filters["is_short_name"])
            if "is_colloquial" in filters and filters["is_colloquial"]:
                query = query.filter(AlternateNameModel.is_colloquial == filters["is_colloquial"])
            if "is_historic" in filters and filters["is_historic"]:
                query = query.filter(AlternateNameModel.is_historic == filters["is_historic"])

        models = query.all()
        entities = [
            e for e in (AlternateNamePersistenceMapper.to_entity(r) for r in models)
            if e is not None
        ]
        return entities
    
    def save(self, entity: AlternateName) -> None:
        model = AlternateNamePersistenceMapper.to_model(entity)
        self.session.merge(model)
        self.session.commit()
    
    def count_all(self) -> int:
        count = self.session.query(AlternateNameModel).count()
        return count
    
    def bulk_insert(self, entities: List[AlternateName]) -> None:
        models = [
            AlternateNamePersistenceMapper.to_model(entity) for entity in entities
        ]
        self.session.bulk_save_objects(models)
        self.session.commit()

    def truncate(self):
        table_name = AlternateNameModel.__tablename__
        self.session.execute(text(f"TRUNCATE TABLE {table_name}"))
        self.session.commit()
