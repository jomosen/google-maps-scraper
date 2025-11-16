from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserDriverConfig:

    language: str = "en"
    headless: bool = False
    timeout: int = 30