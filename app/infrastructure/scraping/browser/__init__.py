from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO
from .selenium_driver import SeleniumDriver
from .playwright_driver import PlaywrightDriver

def get_browser_driver(engine: str, config: BrowserConfigVO):
    if engine == "selenium":
        return SeleniumDriver(config)
    elif engine == "playwright":
        return PlaywrightDriver(config)
    else:
        raise ValueError(f"Unknown browser engine: {engine}")
