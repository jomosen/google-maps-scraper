import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO

class SeleniumDriver:
    def __init__(self, config: BrowserConfigVO):
        self.config = config
        options = webdriver.ChromeOptions()

        if config.headless:
            options.add_argument("--headless")

        options.add_argument("--lang=" + config.language)

        if config.user_agent:
            options.add_argument(f"user-agent={config.user_agent}")

        chromedriver_path = self._get_chromedriver_path()

        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    def _get_chromedriver_path(self):
        chromedriver_filename = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", f"./{chromedriver_filename}")

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(
                f"ChromeDriver not found at {chromedriver_path}.\n"
                "Please set the CHROMEDRIVER_PATH environment variable, "
                "or place the appropriate chromedriver binary in the root of the project.\n"
                f"(Expected: {chromedriver_filename})"
            )
        return chromedriver_path

    def go_to(self, url: str):
        self.driver.get(url)

    def get_element_text(self, selector: str) -> str:
        el = self.driver.find_element(By.CSS_SELECTOR, selector)
        return el.text

    def close(self):
        self.driver.quit()
