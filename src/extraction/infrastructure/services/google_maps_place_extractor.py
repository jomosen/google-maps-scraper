from typing import Callable
from extraction.application.ports.place_extractor_port import PlaceExtractorPort
from extraction.domain.job_config import JobConfig
from extraction.domain.job_task import JobTask
from extraction.application.ports.browser_driver_port import BrowserDriverPort as IBrowserDriverPort
from geonames.application.ports.geonames_unit_of_work_port import GeoNamesUnitOfWorkPort


class GoogleMapsPlaceExtractor(PlaceExtractorPort):
    """Google Maps implementation of the PlaceExtractorPort interface."""
    
    def __init__(self, 
                 browser_driver: IBrowserDriverPort,
                 geonames_uow_factory: Callable[[], GeoNamesUnitOfWorkPort]):
        
        self.browser_driver = browser_driver
        self.geonames_uow_factory = geonames_uow_factory

    def extract(self, job_task: JobTask, job_config: JobConfig):
        
        try:
            print(f"Extracting data for task {job_task.id}...")
            
        except Exception as e:
            self.browser_driver.close()
            print(f"Extraction failed for task {job_task.id}: {e}")
            raise