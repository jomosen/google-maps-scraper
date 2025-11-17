from typing import Protocol
from places.domain.place import Place


class PlacesStoragePort(Protocol):
    def save(self, place: Place) -> None:
        ...