from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService
from extraction.application.services.job_task_worker_service import JobTaskWorkerService
from extraction.domain.value_objects.browser_driver_config import BrowserDriverConfig
from extraction.domain.extraction_job_config import ExtractionJobConfig
from extraction.infrastructure.adapters.browser_driver.playwright_browser_driver import PlaywrightBrowserDriver
from extraction.infrastructure.persistence.database.factory import create_extraction_connector
from extraction.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work_factory import SqlAlchemyUnitOfWorkFactory
from extraction.application.ports.places_storage_port import PlacesStoragePort
from extraction.infrastructure.adapters.places.google_maps_place_extractor import GoogleMapsPlaceExtractor
from extraction.infrastructure.adapters.geonames.graphql_geoname_query_adapter import HttpGeoNamesLookupAdapter
from shared.infrastructure.logging.system_logger import SystemLogger

logger = SystemLogger()

extraction_db_connector = create_extraction_connector(init_schema=True)
uow_factory = SqlAlchemyUnitOfWorkFactory(extraction_db_connector)

job_config = ExtractionJobConfig(
    search_seeds=("junkyards",),
    geoname_id=6252001,
)

extraction_job_runner = ExtractionJobRunnerService(
    task_worker_service_class = JobTaskWorkerService,
    browser_driver_class = PlaywrightBrowserDriver,
    browser_driver_config = BrowserDriverConfig(),
    place_extractor_class = GoogleMapsPlaceExtractor,
    extraction_uow_factory = uow_factory,
    geonames_lookup_class=HttpGeoNamesLookupAdapter,
    places_storage_port_class = PlacesStoragePort,
    logger = logger
)