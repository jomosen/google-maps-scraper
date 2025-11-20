import os
from dotenv import load_dotenv
from pyfiglet import Figlet

from extraction.application.services.extraction_job_runner_service import ExtractionJobRunnerService
from extraction.application.services.job_task_worker_service import JobTaskWorkerService
from extraction.application.services.geoname_selection_service import GeoNameSelectionService
from extraction.domain.value_objects.extraction_job_config import ExtractionJobConfig
from extraction.domain.value_objects.geoname_selection_params_for_extraction_job import GeoNameSelectionParamsForExtractionJob
from extraction.domain.value_objects.browser_driver_config import BrowserDriverConfig
from extraction.infrastructure.adapters.places.google_maps_place_extractor_adapter import GoogleMapsPlaceExtractorAdapter
from extraction.infrastructure.adapters.places.sql_alchemy_place_storage_adapter import SqlAlchemyPlaceStorageAdapter
from extraction.infrastructure.persistence.database.factory import create_db_extraction_connector
from extraction.infrastructure.persistence.unit_of_work.sql_alchemy_extraction_unit_of_work import SqlAlchemyExtractionUnitOfWorkFactory
from extraction.infrastructure.adapters.geonames.graphql_geoname_query_adapter import GraphQLGeoNameQueryAdapter
from extraction.infrastructure.adapters.browser_driver.playwright_browser_driver import PlaywrightBrowserDriver
from extraction.presentation.cli.commands import extraction_job_command, api_server_command
from shared.infrastructure.logging.system_logger import SystemLogger

import extraction.presentation.cli.prompts as prompts

load_dotenv()

logger = SystemLogger()

extraction_db_connector = create_db_extraction_connector(init_schema=True)
extraction_uow_factory = SqlAlchemyExtractionUnitOfWorkFactory(extraction_db_connector)

api_process = api_server_command.start(host="127.0.0.1", port=8080, reload=True)


def create_extraction_job():

    geoname_query_adapter = GraphQLGeoNameQueryAdapter(
        graphql_url=os.environ["GEONAMES_API_GRAPHQL_URL"]
    )

    geoname_selection_service = GeoNameSelectionService(geoname_query_adapter)

    search_seed = prompts.prompt_for_search_seed()
    country = prompts.prompt_for_country(geoname_query_adapter)
    depth_level = prompts.prompt_for_depth_level()
    min_population = prompts.prompt_for_min_population(depth_level)
    max_results = prompts.prompt_for_max_results()
    min_rating = prompts.prompt_for_min_rating()
    max_reviews = prompts.prompt_for_max_reviews()

    geoname_selection_params = GeoNameSelectionParamsForExtractionJob(
        scope_geoname_id=country.geoname_id,
        scope_geoname_name=country.country_name,
        depth_level=depth_level,
        min_population=min_population
    )

    extraction_job_config = ExtractionJobConfig(
        search_seeds=(search_seed,),
        geoname_selection_params=geoname_selection_params,
        max_results=max_results,
        min_rating=min_rating,
        max_reviews=max_reviews
    )

    with extraction_uow_factory() as uow:
        extraction_job = extraction_job_command.create(
            job_config=extraction_job_config,
            job_repo=uow.extraction_job_repo,
            geoname_selection_service=geoname_selection_service
        )

    extraction_job_runner = ExtractionJobRunnerService(
        extraction_uow_factory = extraction_uow_factory,
        task_worker_service_class = JobTaskWorkerService,
        browser_driver_class = PlaywrightBrowserDriver,
        browser_driver_config = BrowserDriverConfig(),
        place_extractor_class = GoogleMapsPlaceExtractorAdapter,
        places_storage_class = SqlAlchemyPlaceStorageAdapter,
        logger = logger
    )

    with extraction_uow_factory() as uow:
        extraction_job = extraction_job_command.run(
            extraction_job=extraction_job,
            extraction_job_runner=extraction_job_runner,
            logger=logger
        )

def main():

    while True:
        prompts.prompt_main_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_extraction_job()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    api_process.terminate()

if __name__ == "__main__":
    main()