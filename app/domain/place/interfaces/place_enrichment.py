from abc import ABC, abstractmethod


class PlaceEnrichment(ABC):
    def __init__(self, place_id: str):
        self.place_id = place_id

    @property
    def source(self) -> str:
        """
        Returns an identifier for the enrichment source.
        By default, the class name.
        """
        return self.__class__.__name__

    @abstractmethod
    def get_properties(self) -> dict:
        """
        Optional method (not strictly required by DDD) to obtain the properties
        as a dict if it is necessary to persist or serialize them (for example, in an API or database).
        Each implementation can override it.
        """
        pass
