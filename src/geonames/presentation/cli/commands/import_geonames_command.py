from typing import Any, Type
from shared.application.ports.logger_port import LoggerPort
from geonames.application.ports.geonames_unit_of_work_port import GeoNamesUnitOfWorkPort
from shared.application.use_case import UseCase
from geonames.application.use_cases.import_geonames_use_case import ImportGeoNamesUseCase
from shared.infrastructure.adapters.tqdm_progress_bar import TqdmProgressBar
from geonames.presentation.cli.commands.build_geonames_import_tasks import build_geonames_import_tasks


def import_geonames_command(uow_factory: GeoNamesUnitOfWorkPort, logger: LoggerPort | None = None):

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

def _run_import(repository: Any, importer: Any, use_case_cls: Type[UseCase], description: str, logger: LoggerPort | None = None):

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

    
