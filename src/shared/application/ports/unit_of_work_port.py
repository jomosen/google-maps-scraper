from abc import ABC, abstractmethod
from contextlib import AbstractContextManager


class UnitOfWorkPort(AbstractContextManager):

    @abstractmethod
    def __enter__(self) -> "UnitOfWorkPort":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
