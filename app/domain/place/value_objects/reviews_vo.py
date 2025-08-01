from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Review:
    author: str
    rating: float
    text: str
    date: str


@dataclass(frozen=True)
class ReviewsVO:
    reviews: List[Review] = field(default_factory=list)
