from dataclasses import dataclass


@dataclass(frozen=True)
class SearchPoint:
    
    name: str
    latitude: float
    longitude: float
    country_code: str
