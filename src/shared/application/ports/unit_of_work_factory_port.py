from abc import ABC, abstractmethod
from .unit_of_work_port import UnitOfWorkPort


class UnitOfWorkFactoryPort(ABC):

    @abstractmethod
    def __call__(self) -> "UnitOfWorkPort":
        raise NotImplementedError
