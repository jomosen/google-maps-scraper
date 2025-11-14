from abc import ABC, abstractmethod
from src.geonames.application.contracts.abstract_unit_of_work import AbstractUnitOfWork


class AbstractUnitOfWorkFactory(ABC):

    @abstractmethod
    def __call__(self) -> AbstractUnitOfWork:
        raise NotImplementedError
