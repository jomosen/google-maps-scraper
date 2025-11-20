from typing import Protocol
from extraction.domain.extracted_place import ExtractedPlace


class PlaceStoragePort(Protocol):
    """
    Port for storing extracted Places into some persistence layer.
    Implementation could use SQL, NoSQL, files, etc.
    """

    def save(self, place: ExtractedPlace) -> None:
        """
        Persist a place into the target storage system.
        """
        ...


class PlacesStorageFactory(Protocol):
    """
    Factory that produces instances of PlacesStoragePort.
    Workers call this to obtain thread-safe storage ports.
    """

    def __call__(self) -> PlaceStoragePort:
        ...
