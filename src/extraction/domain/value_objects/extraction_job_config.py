from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any

from extraction.domain.value_objects.geoname_selection_params_for_extraction_job import GeoNameSelectionParamsForExtractionJob


@dataclass(frozen=True)
class ExtractionJobConfig:
    search_seeds: Tuple[str, ...]
    geoname_selection_params: GeoNameSelectionParamsForExtractionJob
    locale: str = "en-US"
    max_results: int = 50
    min_rating: float = 4.0
    max_reviews: int = 0
    max_workers: int = 5

    def __post_init__(self) -> None:

        cleaned_seeds = tuple(
            s.strip() for s in self.search_seeds if s and s.strip()
        )
        object.__setattr__(self, "search_seeds", cleaned_seeds)

        if self.geoname_selection_params.min_population < 0:
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
            f"scope='{self.geoname_selection_params.scope}', "
            f"geoname_id={self.geoname_selection_params.scope_geoname_id}, "
            f"locale='{self.locale}', "
            f"depth_level='{self.geoname_selection_params.depth_level}', "
            f"min_population={self.geoname_selection_params.min_population}, "
            f"max_results={self.max_results}, "
            f"min_rating={self.min_rating}, "
            f"max_reviews={self.max_reviews}, "
            f"max_workers={self.max_workers})"
        )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "search_seeds": list(self.search_seeds),
            "scope": self.geoname_selection_params.scope,
            "geoname_id": self.geoname_selection_params.scope_geoname_id,
            "locale": self.locale,
            "depth_level": self.geoname_selection_params.depth_level,
            "min_population": self.geoname_selection_params.min_population,
            "max_results": self.max_results,
            "min_rating": self.min_rating,
            "max_reviews": self.max_reviews,
            "max_workers": self.max_workers,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ExtractionJobConfig":

        return ExtractionJobConfig(
            search_seeds=tuple(data.get("search_seeds") or []),
            geoname_selection_params=GeoNameSelectionParamsForExtractionJob(
                scope=data.get("scope", "country"),
                scope_geoname_id=data.get("geoname_id"),
                depth_level=data.get("depth_level", "ADM1"),
                min_population=data.get("min_population", 15000),
            ),
            locale=data.get("locale", "en-US"),
            max_results=data.get("max_results", 50),
            min_rating=data.get("min_rating", 4.0),
            max_reviews=data.get("max_reviews", 0),
            max_workers=data.get("max_workers", 5),
        )
