from dataclasses import dataclass

from extraction.domain.enums.extraction_job_depth_level import ExtractionJobDepthLevel
from extraction.domain.enums.extraction_job_scope import ExtractionJobScope


@dataclass(frozen=True)
class GeoNameSelectionParamsForExtractionJob:
    scope: ExtractionJobScope = ExtractionJobScope.COUNTRY
    scope_geoname_id: int | None = None
    scope_geoname_name: str | None = None
    depth_level: ExtractionJobDepthLevel = ExtractionJobDepthLevel.ADMIN1
    min_population: int = 15000