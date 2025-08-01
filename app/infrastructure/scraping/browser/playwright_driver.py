import time
import random

from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, TimeoutError
from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO

class PlaywrightDriver:
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


    def get_element_text(self, selector: str) -> str:
        return self.page.text_content(selector)

    def close(self):
        self.browser.close()
        self.playwright.stop()
