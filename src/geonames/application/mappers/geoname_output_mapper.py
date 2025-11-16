from typing import List
from geonames.domain.geoname import GeoName
from geonames.application.dtos.geoname_dto import GeoNameDTO


class GeoNameMapper:
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
        return [GeoNameMapper.to_dto(entity) for entity in entities]
