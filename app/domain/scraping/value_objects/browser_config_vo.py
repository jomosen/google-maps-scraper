from dataclasses import dataclass
from typing import Optional

@dataclass
class BrowserConfigVO:
    language: str = "en"
    headless: bool = False
    timeout: int = 30
