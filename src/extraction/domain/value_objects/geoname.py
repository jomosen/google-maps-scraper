from dataclasses import dataclass


@dataclass(frozen=True)
class GeoName:
    
    name: str
    latitude: float
    longitude: float
    country_code: str
