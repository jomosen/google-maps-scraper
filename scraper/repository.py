from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def get_all(self):
        pass
