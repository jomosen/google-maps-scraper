from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionTaskGeoName:

    name: str
    latitude: float
    longitude: float
