import requests
from typing import List, Dict, Any
from extraction.domain.value_objects.search_point import SearchPoint
from extraction.application.ports.geoname_query_port import GeoNameQueryPort


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
    
    def find_search_point_by_geoname_id(self, geoname_id: int) -> SearchPoint:
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
        return SearchPoint(**data["findGeonameById"])

    def find_search_points_for_admins(self, filters: Dict[str, Any]) -> List[SearchPoint]:
        query = """
        query ($filters: AdminFiltersInput!) {
          findAdminGeonames(filters: $filters) {
            name
            latitude
            longitude
            countryCode
          }
        }
        """

        data = self._call(query, {"filters": filters})
        return [SearchPoint(**item) for item in data["findAdminGeonames"]]

    def find_search_points_for_cities(self, filters: Dict[str, Any]) -> List[SearchPoint]:
        query = """
        query ($filters: CityFiltersInput!) {
          findCityGeonames(filters: $filters) {
            name
            latitude
            longitude
            countryCode
          }
        }
        """

        data = self._call(query, {"filters": filters})
        return [SearchPoint(**item) for item in data["findCityGeonames"]]