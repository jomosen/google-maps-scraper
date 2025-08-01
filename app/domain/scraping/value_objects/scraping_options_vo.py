from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ScrapingOptionsVO:
    keywords: List[str]
    locations: List[str]
    language: str
    max_reviews: int
