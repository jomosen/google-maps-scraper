import strawberry
from typing import List

from geonames.application.mappers.country_output_mapper import CountryOutputMapper
from geonames.domain.country import Country
from geonames.domain.geoname import GeoName
from geonames.presentation.api.dependencies import get_geoname_query_service
from geonames.application.mappers.geoname_output_mapper import GeoNameOutputMapper

from .types import CountryType, GeoNameType
from .inputs import AdminFiltersInput, CityFiltersInput, CountryFiltersInput


@strawberry.type
class Query:

    @strawberry.field
    def find_geoname_by_id(self, geoname_id: int) -> GeoNameType:
        service = get_geoname_query_service()
        entity: GeoName = service.get_geoname(geoname_id)
        return GeoNameOutputMapper.to_graphql(GeoNameType, entity)
    
    @strawberry.field
    def find_admin_geonames(self, filters: AdminFiltersInput) -> List[GeoNameType]:
        service = get_geoname_query_service()
        entities: List[GeoName] = service.get_admin_geonames(vars(filters))
        return GeoNameOutputMapper.to_graphql_list(GeoNameType, entities)

    @strawberry.field
    def find_city_geonames(self, filters: CityFiltersInput) -> List[GeoNameType]:
        service = get_geoname_query_service()
        entities: List[GeoName] = service.get_city_geonames(vars(filters))
        return GeoNameOutputMapper.to_graphql_list(GeoNameType, entities)
    
    @strawberry.field
    def find_countries(self, filters: CountryFiltersInput) -> List[CountryType]:
        service = get_geoname_query_service()
        entities: List[Country] = service.get_countries(vars(filters))
        return CountryOutputMapper.to_graphql_list(CountryType, entities)

schema = strawberry.Schema(query=Query)
