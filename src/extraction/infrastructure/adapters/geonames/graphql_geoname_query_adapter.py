import requests
from typing import List, Dict, Any
from extraction.application.mappers.country_input_mapper import CountryInputMapper
from extraction.domain.value_objects.country import Country
from extraction.domain.value_objects.geoname import GeoName
from extraction.application.ports.geoname_query_port import GeoNameQueryPort
from extraction.application.mappers.geoname_input_mapper import GeoNameInputMapper


class GraphQLGeoNameQueryAdapter(GeoNameQueryPort):

    def __init__(self, graphql_url: str):
        self.url = graphql_url

    def _call(self, query: str, variables: Dict[str, Any]):
        response = requests.post(
            self.url,
            json={"query": query, "variables": variables},
            timeout=5,
        )
        response.raise_for_status()
        return response.json()["data"]
    
    def find_geoname_by_id(self, geoname_id: int) -> GeoName:
        query = """
        query ($id: Int!) {
          findGeonameById(geonameId: $id) {
            name
            latitude
            longitude
            countryCode
          }
        }
        """

        data = self._call(query, {"id": geoname_id})
        item = data.get("findGeonameById") or None
        return GeoNameInputMapper.from_graphql(item)

    def find_admin_geonames(self, filters: Dict[str, Any]) -> List[GeoName]:
        query = """
        query ($filters: AdminFiltersInput!) {
          findAdminGeonames(filters: $filters) {
            geonameId
            name
            latitude
            longitude
            countryCode
          }
        }
        """

        data = self._call(query, {"filters": filters})
        items = data.get("findAdminGeonames") or []
        return [GeoNameInputMapper.from_graphql(item) for item in items]

    def find_city_geonames(self, filters: Dict[str, Any]) -> List[GeoName]:
        query = """
        query ($filters: CityFiltersInput!) {
          findCityGeonames(filters: $filters) {
            geonameId
            name
            latitude
            longitude
            countryCode
          }
        }
        """

        data = self._call(query, {"filters": filters})
        items = data.get("findCityGeonames") or []
        return [GeoNameInputMapper.from_graphql(item) for item in items]
    
    def find_country_by_id(self, geoname_id: int) -> Country:
        query = """
        query ($id: Int!) {
          findCountryById(geonameId: $id) {
            countryName
            isoAlpha2
            continent
            capital
            population
          }
        }
        """

        data = self._call(query, {"id": geoname_id})
        item = data.get("findCountryById") or None
        return CountryInputMapper.from_graphql(item)
    
    def find_countries(self, filters: Dict[str, Any]) -> List[Country]:
        query = """
        query ($filters: CountryFiltersInput!) {
          findCountries(filters: $filters) {
            geonameId
            countryName
            isoAlpha2
            continent
            capital
            population
          }
        }
        """

        data = self._call(query, {"filters": filters})
        items = data.get("findCountries") or []
        return [CountryInputMapper.from_graphql(item) for item in items]