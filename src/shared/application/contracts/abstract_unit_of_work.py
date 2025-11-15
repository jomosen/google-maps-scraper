from contextlib import AbstractContextManager
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class AbstractUnitOfWork(Protocol, AbstractContextManager):

    geoname_repo: Any
    country_geoname_repo: Any
    admin_geoname_repo: Any
    city_geoname_repo: Any
    geoname_alternatename_repo: Any

    def __enter__(self) -> "AbstractUnitOfWork":
        ...

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
