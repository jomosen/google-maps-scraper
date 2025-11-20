from extraction.domain.value_objects.geoname import GeoName


class GeoNameInputMapper:

    @staticmethod
    def from_graphql(data: dict) -> GeoName:
        """
        Maps a GraphQL GeoNameType response into a local Extraction GeoName entity.
        """

        return GeoName(
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            country_code=data.get("countryCode"),
        )