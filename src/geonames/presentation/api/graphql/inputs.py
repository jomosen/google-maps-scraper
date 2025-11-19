import strawberry
from typing import Optional


@strawberry.input
class AdminFiltersInput:
    country_code: str
    feature_code: str

@strawberry.input
class CityFiltersInput:
    country_code: str
    min_population: int

@strawberry.input
class CountryFiltersInput:
    iso_alpha2: Optional[str] = None
    continent: Optional[str] = None