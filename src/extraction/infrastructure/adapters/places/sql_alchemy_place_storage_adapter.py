from sqlalchemy.orm import Session

from extraction.application.ports.places_storage_port import PlaceStoragePort
from extraction.domain.extracted_place import ExtractedPlace
from extraction.infrastructure.persistence.models.extracted_place_model import ExtractedPlaceModel
from extraction.infrastructure.persistence.mappers.extracted_place_persistence_mapper import ExtractionPlacePersistenceMapper


class SqlAlchemyPlaceStorageAdapter(PlaceStoragePort):

    def __init__(self, session_factory: Session):
        """
        session_factory: Callable[[], Session]
        """
        self._session_factory = session_factory

    def save(self, place: ExtractedPlace) -> None:
        """
        Persist the Place using SQLAlchemy.
        """
        session = self._session_factory()

        try:
            model = ExtractionPlacePersistenceMapper.to_model(place)
            session.merge(model)
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()
