import time

from abc import ABC, abstractmethod
from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO

class BrowserDriver(ABC):
    def __init__(self, config: BrowserConfigVO):
        self.config = config

    @abstractmethod
    def go_to(self, url: str):
        pass

    @abstractmethod
    def get_element_text(self, selector: str) -> str:
        pass

    @abstractmethod
    def click(self, selector: str):
        pass

    @abstractmethod
    def send_keys(self, selector: str, query: str):
        pass

    @abstractmethod    
    def scroll(self, selector: str, number_of_times: int = 100):
        pass

    @abstractmethod
    def close(self):
        pass

    def sleep(self, seconds: int):
        time.sleep(seconds)
