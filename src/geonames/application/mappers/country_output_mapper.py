from typing import Type, TypeVar, List
from pydantic import BaseModel

from geonames.domain.country import Country
from geonames.application.dto.country_dto import CountryDTO

T = TypeVar("T")

class CountryOutputMapper:
    """
    Maps domain Country entities to API DTOs.
    """

    @staticmethod
    def to_dto(entity: Country) -> CountryDTO:
        """Convert a single Country entity to a CountryDTO."""
        return CountryDTO(
            geoname_id=entity.geoname_id,
            iso_alpha2=entity.iso_alpha2,
            iso_alpha3=getattr(entity, "iso_alpha3", None),
            iso_numeric=getattr(entity, "iso_numeric", None),
            fips_code=getattr(entity, "fips_code", None),
            country_name=entity.country_name,
            capital=getattr(entity, "capital", None),
            area_sqkm=getattr(entity, "area_sqkm", None),
            population=getattr(entity, "population", None),
            continent=getattr(entity, "continent", None),
            tld=getattr(entity, "tld", None),
            currency_code=getattr(entity, "currency_code", None),
            currency_name=getattr(entity, "currency_name", None),
            phone=getattr(entity, "phone", None),
            postal_code_format=getattr(entity, "postal_code_format", None),
            postal_code_regex=getattr(entity, "postal_code_regex", None),
            languages=getattr(entity, "languages", None),
            neighbours=getattr(entity, "neighbours", None),
            equivalent_fips_code=getattr(entity, "equivalent_fips_code", None),
        )

    @staticmethod
    def to_dto_list(entities: List[Country]) -> List[CountryDTO]:
        """Convert a list of Country entities to a list of CountryDTOs."""
        return [CountryOutputMapper.to_dto(entity) for entity in entities]
    
    @staticmethod
    def to_graphql(type_cls: Type[T], entity: Country) -> T:
        dto = CountryOutputMapper.to_dto(entity)
        clean_dict = CountryOutputMapper._clean_dto_for_graphql(type_cls, dto)
        return type_cls(**clean_dict)
    
    @staticmethod
    def to_graphql_list(type_cls: Type[T], entities: List[Country]) -> List[T]:
        dtos = CountryOutputMapper.to_dto_list(entities)
        return [type_cls(**CountryOutputMapper._clean_dto_for_graphql(type_cls, d)) for d in dtos]
    
    @staticmethod
    def _clean_dto_for_graphql(type_cls: Type[T], dto: CountryDTO) -> dict:
        dto_dict = dto.model_dump()
        return {
            key: dto_dict[key]
            for key in type_cls.__annotations__.keys()
            if key in dto_dict
        }
