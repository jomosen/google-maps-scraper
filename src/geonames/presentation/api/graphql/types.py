import strawberry


@strawberry.type
class GeoNameType:
    geoname_id: int
    name: str
    latitude: float
    longitude: float
    country_code: str
    admin1_code: str
    admin2_code: str
    admin3_code: str
    admin4_code: str
    feature_class: str
    feature_code: str
    population: int
    timezone: str

@strawberry.type
class CountryType:
    geoname_id: int
    iso_alpha2: str
    country_name: str
    continent: str
    capital: str
    population: int