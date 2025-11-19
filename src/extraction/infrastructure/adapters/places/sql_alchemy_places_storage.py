from extraction.application.ports.places_storage_port import PlacesStoragePort
from extraction.domain.extracted_place import ExtractedPlace
from places.infrastructure.persistence.models.place_model import PlaceModel


class SqlAlchemyPlacesStorageAdapter(PlacesStoragePort):

    def __init__(self, session_factory):
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
            model = PlaceModel.from_domain(place)
            session.add(model)
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()
