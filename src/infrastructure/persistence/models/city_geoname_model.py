from src.infrastructure.persistence.models.abstract_geoname_model import AbstractGeoNameModel


class CityGeoNameModel(AbstractGeoNameModel):

    __tablename__ = "cities"