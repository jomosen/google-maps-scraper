from typing import Callable
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from extraction.domain.extraction_job_config import ExtractionJobConfig
from extraction.domain.extraction_task import ExtractionTask
from extraction.application.ports.browser_driver_port import BrowserDriverPort as IBrowserDriverPort
from extraction.application.ports.geonames_lookup_port import GeoNamesLookupFactory


class GoogleMapsPlaceExtractor(PlaceExtractorPort):
    """Google Maps implementation of the PlaceExtractorPort interface."""
    
    def __init__(self, 
                 browser_driver: IBrowserDriverPort,
                 geonames_lookup_factory: GeoNamesLookupFactory):
        
        self.browser_driver = browser_driver
        self.geonames_lookup_factory = geonames_lookup_factory

    def extract(self, task: ExtractionTask, job_config: ExtractionJobConfig):
        
        try:
            print(f"Extracting data for task {task.id}...")
            
        except Exception as e:
            self.browser_driver.close()
            print(f"Extraction failed for task {task.id}: {e}")
            raise