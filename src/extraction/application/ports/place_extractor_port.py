from typing import Iterable
from extraction.domain.job_task import JobTask
from extraction.domain.job_config import JobConfig
from geonames.domain.geoname import GeoName
from places.domain.place import Place

class PlaceExtractorPort:
    
    def extract(self, 
                job_task: JobTask, 
                geoname: GeoName,
                job_config: JobConfig
                ) -> Iterable[Place]:
        
        raise NotImplementedError
