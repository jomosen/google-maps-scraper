from abc import ABC, abstractmethod
from .abstract_unit_of_work import AbstractUnitOfWork


class AbstractUnitOfWorkFactory(ABC):

    @abstractmethod
    def __call__(self) -> AbstractUnitOfWork:
        raise NotImplementedError
