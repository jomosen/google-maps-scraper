from src.geonames.infrastructure.persistence.models.abstract_geoname_model import AbstractGeoNameModel


class AdminGeoNameModel(AbstractGeoNameModel):

    __tablename__ = "admin_divisions"