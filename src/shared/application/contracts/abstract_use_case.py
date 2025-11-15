from abc import ABC, abstractmethod


class AbstractUseCase(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")