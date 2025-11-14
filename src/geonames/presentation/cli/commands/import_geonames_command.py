from typing import Any, Type
from src.geonames.infrastructure.services.file_downloader import FileDownloader
from src.geonames.application.contracts.abstract_logger import AbstractLogger
from src.geonames.application.contracts.abstract_unit_of_work_factory import AbstractUnitOfWorkFactory
from src.geonames.application.use_cases.base_use_case import BaseUseCase
from src.geonames.application.use_cases.import_geonames_use_case import ImportGeoNamesUseCase
from src.geonames.infrastructure.services.tqdm_progress_bar import TqdmProgressBar
from src.geonames.presentation.cli.commands.build_geonames_import_tasks import build_geonames_import_tasks


def import_geonames_command(uow_factory: AbstractUnitOfWorkFactory, logger: AbstractLogger | None = None):

    import_tasks = build_geonames_import_tasks(logger)
    
    with uow_factory() as uow:

        for task in import_tasks:
            
            _run_import(
                getattr(uow, task["repository_attr"]),
                task["importer_cls"],
                ImportGeoNamesUseCase,
                task["description"],
                logger,
            )

def _run_import(repository: Any, importer: Any, use_case_cls: Type[BaseUseCase], description: str, logger: AbstractLogger | None = None):

    use_case = use_case_cls(repository, importer)

    try:
        total, insert_generator = use_case.execute()
        if not total:
            if logger:
                logger.info(f"No need to import {description}")
            return

        with TqdmProgressBar(total=total, desc=description, unit="records", colour="green") as progress:
            progress.run(insert_generator)
    
    except Exception as e:
        if logger:
            logger.error(f"Error during {description}: {e}")
        return

    
