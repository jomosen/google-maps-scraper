from typing import Protocol
from shared.application.ports.unit_of_work_port import UnitOfWorkPort
from places.domain.repositories.place_repository import PlaceRepository


class PlacesUnitOfWorkPort(UnitOfWorkPort, Protocol):
    place_repo: PlaceRepository