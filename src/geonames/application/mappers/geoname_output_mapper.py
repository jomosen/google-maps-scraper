from typing import Type, TypeVar, List
from pydantic import BaseModel

from geonames.domain.geoname import GeoName
from geonames.application.dto.geoname_dto import GeoNameDTO

T = TypeVar("T")

class GeoNameOutputMapper:
    """
    Maps domain GeoName entities to API DTOs (for FastAPI responses).
    """

    @staticmethod
    def to_dto(entity: GeoName) -> GeoNameDTO:
        """Convert a single GeoName entity to a GeoNameDTO."""
        return GeoNameDTO(
            geoname_id=entity.geoname_id,
            name=entity.name,
            asciiname=getattr(entity, "asciiname", None),
            alternatenames=getattr(entity, "alternatenames", None),
            latitude=entity.latitude,
            longitude=entity.longitude,
            feature_class=entity.feature_class,
            feature_code=entity.feature_code,
            country_code=entity.country_code,
            cc2=getattr(entity, "cc2", None),
            admin1_code=getattr(entity, "admin1_code", None),
            admin2_code=getattr(entity, "admin2_code", None),
            admin3_code=getattr(entity, "admin3_code", None),
            admin4_code=getattr(entity, "admin4_code", None),
            population=getattr(entity, "population", 0),
            elevation=getattr(entity, "elevation", None),
            dem=getattr(entity, "dem", None),
            timezone=getattr(entity, "timezone", None),
            modification_date=getattr(entity, "modification_date", None),
        )

    @staticmethod
    def to_dto_list(entities: List[GeoName]) -> List[GeoNameDTO]:
        """Convert a list of GeoName entities to a list of GeoNameDTOs."""
        return [GeoNameOutputMapper.to_dto(entity) for entity in entities]
    
    @staticmethod
    def to_graphql(type_cls: Type[T], entity: GeoName) -> T:
        dto = GeoNameOutputMapper.to_dto(entity)
        clean_dict = GeoNameOutputMapper._clean_dto_for_graphql(type_cls, dto)
        return type_cls(**clean_dict)
    
    @staticmethod
    def to_graphql_list(type_cls: Type[T], entities: List[GeoName]) -> List[T]:
        dtos = GeoNameOutputMapper.to_dto_list(entities)
        return [type_cls(**GeoNameOutputMapper._clean_dto_for_graphql(type_cls, d)) for d in dtos]
    
    @staticmethod
    def _clean_dto_for_graphql(type_cls: Type[T], dto: GeoNameDTO) -> dict:
        dto_dict = dto.model_dump()
        return {
            key: dto_dict[key]
            for key in type_cls.__annotations__.keys()
            if key in dto_dict
        }
