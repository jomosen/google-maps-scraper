import time
import random

from typing import Optional, List
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle, TimeoutError as PlaywrightTimeoutError
from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO
from app.domain.scraping.interfaces.browser_driver import BrowserDriver

WAIT_TIMEOUT = 10000  # en ms
SCROLL_PAUSE_TIME = 1

class PlaywrightDriver(BrowserDriver):
    def __init__(self, config: BrowserConfigVO):
        self.config = config
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=config.headless
        )

        context_args = {
            "locale": config.language
        }

        self.page = self.browser.new_context(**context_args).new_page()

    def go_to(self, url: str):
        self.page.goto(url)

    def click(self, selector, timeout=10000):
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            self.page.click(selector)
        except TimeoutError:
            print(f"Element with selector '{selector}' not found within {timeout} ms.")
        except Exception as e:
            print(f"Unexpected error while clicking element: {e}")

    def send_keys(self, selector: str, input_value: str, timeout=10000):
        try:
            input_element = self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            
            input_element.click()
            self.page.keyboard.press("Control+A")
            time.sleep(random.uniform(0.1, 0.2))
            self.page.keyboard.press("Delete")
            time.sleep(random.uniform(0.1, 0.2))

            for char in input_value:
                self.page.keyboard.insert_text(char)
                time.sleep(random.uniform(0.025, 0.125))

            time.sleep(random.uniform(0.2, 0.4))
            self.page.keyboard.press("Enter")

        except TimeoutError:
            print(f"[ERROR] Input field with selector '{selector}' not found in time.")
        except Exception as e:
            print(f"[ERROR] Unexpected error while sending keys: {e}")

    def scroll(self, selector: str, number_of_times: int = 100):
        try:
            element_handle = self.page.wait_for_selector(selector, timeout=10000, state="visible")

            previous_scroll_height = self.page.evaluate("(el) => el.scrollHeight", element_handle)
            end_reached = False
            i = 0

            while not end_reached and i < number_of_times:
                self.page.evaluate("(el) => el.scrollTop = el.scrollHeight", element_handle)
                time.sleep(1)

                new_scroll_height = self.page.evaluate("(el) => el.scrollHeight", element_handle)
                if new_scroll_height == previous_scroll_height:
                    end_reached = True

                previous_scroll_height = new_scroll_height
                i += 1

        except TimeoutError:
            print(f"[ERROR] Element with selector '{selector}' not found.")
        except Exception as e:
            print(f"[ERROR] Unexpected error while scrolling: {e}")

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def get_elements(self, selector_value) -> List[ElementHandle]:
        return self.page.query_selector_all(selector_value)

    def get_element(self, selector_value) -> Optional[ElementHandle]:
        return self.page.query_selector(selector_value)

    def get_element_attribute(self, selector_value, attribute) -> Optional[str]:
        element = self.get_element(selector_value)
        if element:
            return element.get_attribute(attribute)
        return None

    def get_element_text(self, selector_value) -> Optional[str]:
        element = self.get_element(selector_value)
        if element:
            return element.inner_text()
        return None

    def get_elements_within_parent(self, parent: ElementHandle, element_selector_value) -> List[ElementHandle]:
        return parent.query_selector_all(element_selector_value)

    def get_element_within_parent(self, parent: ElementHandle, element_selector_value) -> Optional[ElementHandle]:
        try:
            return parent.query_selector(element_selector_value)
        except Exception as e:
            print(f"Error getting element within parent: {e}")
            return None

    def get_element_attribute_within_parent(self, parent: ElementHandle, element_selector_value, attribute) -> Optional[str]:
        element = self.get_element_within_parent(parent, element_selector_value)
        if element:
            return element.get_attribute(attribute)
        return None

    def get_element_text_within_parent(self, parent: ElementHandle, element_selector_value) -> Optional[str]:
        element = self.get_element_within_parent(parent, element_selector_value)
        if element:
            return element.inner_text()
        return None

    def click_element_when_present(self, selector_value):
        try:
            self.page.wait_for_selector(selector_value, state="visible", timeout=WAIT_TIMEOUT)
            self.page.click(selector_value)
        except PlaywrightTimeoutError:
            print(f"Element with selector '{selector_value}' not found.")
        except Exception as e:
            print(f"Unexpected error while clicking element: {e}")

    def send_keys_after_waiting(self, selector_value, input_value: str):
        try:
            self.page.wait_for_selector(selector_value, state="visible", timeout=WAIT_TIMEOUT)
            input_element = self.page.query_selector(selector_value)
            if not input_element:
                print(f"Input field with selector '{selector_value}' not found.")
                return

            # limpiar valor existente
            input_element.fill("")

            # simular tipeo humano
            for char in input_value:
                input_element.type(char, delay=50)  # delay en ms
            time.sleep(0.3)
            input_element.press("Enter")

        except PlaywrightTimeoutError:
            print(f"Input field with selector '{selector_value}' not found.")
        except Exception as e:
            print(f"Unexpected error while sending keys: {e}")

    def scroll_element(self, selector_value, number_of_times=10, selector_type=None) -> bool:
        element = self.page.query_selector(selector_value) #self.page.wait_for_selector(selector_value, state="visible", timeout=WAIT_TIMEOUT)
        if not element:
            return False

        previous_scroll_height = self.page.evaluate("(el) => el.scrollHeight", element)
        end_reached = False
        i = 0

        while not end_reached and i < number_of_times:
            self.page.evaluate("(el) => { el.scrollTop = el.scrollHeight }", element)
            time.sleep(SCROLL_PAUSE_TIME)

            new_scroll_height = self.page.evaluate("(el) => el.scrollHeight", element)
            if new_scroll_height == previous_scroll_height:
                end_reached = True

            previous_scroll_height = new_scroll_height
            i += 1
        
        return True

    def scroll_element_by_xpath(self, xpath_value, number_of_times=10):
        selector = f"xpath={xpath_value}"
        return self.scroll_element(selector, number_of_times)

    def get_parents_of_elements(self, selector_value) -> List[ElementHandle]:
        elements = self.page.query_selector_all(selector_value)
        parents = []
        for el in elements:
            parent = el.evaluate_handle("el => el.parentElement")
            parents.append(parent.as_element())
        return parents

    def scroll_until_element_into_view(self, element: ElementHandle):
        self.page.evaluate("(el) => el.scrollIntoView({block: 'center'})", element)
