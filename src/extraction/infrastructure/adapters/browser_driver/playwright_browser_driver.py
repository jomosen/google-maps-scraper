import os
import time
import random
from typing import Optional, List
from playwright.sync_api import sync_playwright, Page, ElementHandle, TimeoutError as PlaywrightTimeoutError
from extraction.application.ports.browser_driver_port import BrowserDriverPort
from extraction.domain.value_objects.browser_driver_config import BrowserDriverConfig


class PlaywrightBrowserDriver(BrowserDriverPort):
    """Playwright implementation of the BrowserDriverPort interface."""

    def __init__(self, config: BrowserDriverConfig):
        self.config = config
        self._playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def open(self) -> None:
        self._playwright = sync_playwright().start()

        self.browser = self._playwright.chromium.launch(
            headless=self.config.headless
        )

        context_args = {
            "locale": self.config.locale,
        }

        self.context = self.browser.new_context(**context_args)
        self.page = self.context.new_page()

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def get_content(self) -> str:
        return self.page.content()

    def close(self) -> None:
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()

    