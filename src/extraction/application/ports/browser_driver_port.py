from typing import Any


class BrowserDriverPort:
    """
    Abstraction of a browser driver used by the scraping subsystem.
    Implementations may use Playwright, Selenium, undetected-chromedriver, etc.
    """
    
    def open(self) -> None:
        """Launch the browser instance (if required by the driver)."""
        raise NotImplementedError

    def goto(self, url: str) -> None:
        """Navigate to a given URL."""
        raise NotImplementedError

    def get_content(self) -> str:
        """
        Return the current page HTML content as a string.
        Useful for parsers, extractors and debugging.
        """
        raise NotImplementedError

    def evaluate(self, script: str) -> Any:
        """
        Evaluate a JS script in the browser context.
        Optional depending on implementation.
        """
        raise NotImplementedError

    def screenshot(self, path: str | None = None) -> bytes:
        """
        Take a screenshot. Return raw bytes if no path is provided.
        """
        raise NotImplementedError

    def wait_for_selector(self, selector: str, timeout: int | float = 5000) -> None:
        """
        Wait until the DOM element matching 'selector' appears.
        Essential for dynamic pages like Google Maps.
        """
        raise NotImplementedError

    def close(self) -> None:
        """Close browser and release resources."""
        raise NotImplementedError