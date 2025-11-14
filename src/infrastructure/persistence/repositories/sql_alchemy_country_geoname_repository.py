from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from src.domain.abstract_country_geoname_repository import AbstractCountryGeoNameRepository
from src.domain.country import Country
from src.infrastructure.persistence.models.country_model import CountryModel
from src.infrastructure.persistence.models.geoname_model import GeoNameModel
from src.infrastructure.persistence.mappers.country_persistence_mapper import CountryPersistenceMapper


class SqlAlchemyCountryGeoNameRepository(AbstractCountryGeoNameRepository):

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, geoname_id: int) -> Optional[Country]:
        record = self.session.get(CountryModel, geoname_id)
        return CountryPersistenceMapper.to_entity(record) if record else None

    def find_all(self, filters: Optional[Dict] = None) -> List[Country]:
        filters = filters or {}

        query = (
            self.session.query(
                CountryModel,
                func.count(GeoNameModel.geoname_id).label("geoname_count")
            )
            .outerjoin(GeoNameModel, GeoNameModel.country_code == CountryModel.iso_alpha2)
            .group_by(CountryModel.iso_alpha2)
            .order_by(CountryModel.country_name)
        )

        if "continent_code" in filters and filters["continent_code"]:
            query = query.filter(CountryModel.continent == filters["continent_code"])

        if "min_population" in filters and filters["min_population"]:
            query = query.filter(CountryModel.population >= filters["min_population"])

        if "max_population" in filters and filters["max_population"]:
            query = query.filter(CountryModel.population <= filters["max_population"])

        if "currency_code" in filters and filters["currency_code"]:
            query = query.filter(CountryModel.currency_code == filters["currency_code"])

        results = query.all()

        countries = []
        for country_model, geoname_count in results:
            country = CountryPersistenceMapper.to_entity(country_model)
            country.has_geonames = geoname_count > 0
            countries.append(country)

        return countries

    def save(self, entity: Country) -> None:
        model = CountryPersistenceMapper.to_model(entity)
        existing = self.session.get(CountryModel, model.geoname_id)

        if existing:
            for attr, value in vars(model).items():
                if hasattr(existing, attr) and value is not None:
                    setattr(existing, attr, value)
        else:
            self.session.add(model)

        self.session.commit()

    def count_all(self) -> int:
        count = self.session.query(CountryModel).count()
        return count
    
    def bulk_insert(self, entities: List[Country]) -> None:
        models = [
            CountryPersistenceMapper.to_model(entity) for entity in entities
        ]
        self.session.bulk_save_objects(models)
        self.session.commit()

    def truncate(self):
        table_name = CountryModel.__tablename__
        self.session.execute(text(f"TRUNCATE TABLE {table_name}"))
        self.session.commit()
