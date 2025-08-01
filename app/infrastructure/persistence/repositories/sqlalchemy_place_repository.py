from app.domain.place.repositories.place_repository import PlaceRepository
from app.domain.place.entities.place import Place
from sqlalchemy.orm import Session
from app.infrastructure.persistence.models.place_model import PlaceModel
from app.application.place.mappers.place_mapper import PlaceMapper

class SQLAlchemyPlaceRepository(PlaceRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, place: Place) -> None:
        model = PlaceMapper.to_model(place)
        self.session.merge(model)
        self.session.commit()

    def find_by_scraping_id(self, scraping_id: str) -> list[Place]:
        results = (
            self.session.query(PlaceModel)
            .filter_by(scraping_id=scraping_id)
            .all()
        )
        return [PlaceMapper.to_entity(row) for row in results]
