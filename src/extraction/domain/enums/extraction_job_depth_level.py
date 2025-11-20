from enum import Enum


class ExtractionJobDepthLevel(str, Enum):
    ADMIN1 = "admin1"
    ADMIN2 = "admin2"
    ADMIN3 = "admin3"
    CITY = "city"