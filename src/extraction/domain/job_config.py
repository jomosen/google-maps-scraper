from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any


@dataclass(frozen=True)
class JobConfig:
    search_seeds: Tuple[str, ...] = field(default_factory=tuple)
    scope: str = "country"
    geoname_id: Optional[int] = None
    language_code: str = "en"
    depth_level: str = "populated_places"
    min_population: int = 15000
    max_results: int = 50
    min_rating: float = 4.0
    max_reviews: int = 0
    max_workers: int = 5

    def __post_init__(self) -> None:

        cleaned_seeds = tuple(
            s.strip() for s in self.search_seeds if s and s.strip()
        )
        object.__setattr__(self, "search_seeds", cleaned_seeds)

        if self.min_population < 0:
            raise ValueError("min_population must be >= 0")

        if self.max_results <= 0:
            raise ValueError("max_results must be > 0")

        if not 0.0 <= self.min_rating <= 5.0:
            raise ValueError("min_rating must be between 0.0 and 5.0")

        if self.max_workers <= 0:
            raise ValueError("max_workers must be > 0")

    def __str__(self) -> str:
        return (
            f"JobConfig(search_seeds={self.search_seeds}, "
            f"scope='{self.scope}', "
            f"geoname_id={self.geoname_id}, "
            f"language_code='{self.language_code}', "
            f"depth_level='{self.depth_level}', "
            f"min_population={self.min_population}, "
            f"max_results={self.max_results}, "
            f"min_rating={self.min_rating}, "
            f"max_reviews={self.max_reviews}, "
            f"max_workers={self.max_workers})"
        )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "search_seeds": list(self.search_seeds),
            "scope": self.scope,
            "geoname_id": self.geoname_id,
            "language_code": self.language_code,
            "depth_level": self.depth_level,
            "min_population": self.min_population,
            "max_results": self.max_results,
            "min_rating": self.min_rating,
            "max_reviews": self.max_reviews,
            "max_workers": self.max_workers,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "JobConfig":

        return JobConfig(
            search_seeds=tuple(data.get("search_seeds") or []),
            scope=data.get("scope", "country"),
            geoname_id=data.get("geoname_id"),
            language_code=data.get("language_code", "en"),
            depth_level=data.get("depth_level", "populated_places"),
            min_population=data.get("min_population", 15000),
            max_results=data.get("max_results", 50),
            min_rating=data.get("min_rating", 4.0),
            max_reviews=data.get("max_reviews", 0),
            max_workers=data.get("max_workers", 5),
        )
