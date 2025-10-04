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

    @abstractmethod
    def get_elements(self, selector_value):
        pass

    @abstractmethod
    def get_element(self, selector_value):
        pass

    @abstractmethod
    def get_element_attribute(self, selector_value, attribute):
        pass

    @abstractmethod
    def get_element_text(self, selector_value):
        pass

    @abstractmethod
    def get_elements_within_parent(self, parent, element_selector_value):
        pass

    @abstractmethod
    def get_element_within_parent(self, parent, element_selector_value):
        pass

    @abstractmethod
    def get_element_attribute_within_parent(self, parent, element_selector_value, attribute):
        pass

    @abstractmethod
    def get_element_text_within_parent(self, parent, element_selector_value):
        pass

    @abstractmethod
    def click_element_when_present(self, selector_value):
        pass

    @abstractmethod
    def send_keys_after_waiting(self, selector_value, input_value):
        pass

    @abstractmethod
    def scroll_element(self, selector_value, number_of_times=100, selector_type=None):
        pass

    @abstractmethod
    def scroll_element_by_xpath(self, xpath_value, number_of_times=100):
        pass

    @abstractmethod
    def get_parents_of_elements(self, selector_value):
        pass

    @abstractmethod
    def scroll_until_element_into_view(self, element):
        pass