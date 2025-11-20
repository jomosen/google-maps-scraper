from extraction.domain.value_objects.country import Country


class CountryInputMapper:

    @staticmethod
    def from_graphql(data: dict) -> Country:
        """
        Maps a GraphQL CountryType response into a local Extraction Country entity.
        """

        return Country(
            geoname_id=data.get("geonameId"),
            iso_alpha2=data.get("isoAlpha2"),
            country_name=data.get("countryName"),
            continent=data.get("continent"),
            capital=data.get("capital"),
            population=data.get("population"),
        )