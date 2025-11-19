from typing import Iterable

from extraction.domain.extraction_task import ExtractionTask
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig
from extraction.domain.extracted_place import ExtractedPlace


class PlaceExtractorPort:
    
    def extract(self, job_task: ExtractionTask, job_config: ExtractionJobConfig) -> Iterable[ExtractedPlace]:
        raise NotImplementedError
