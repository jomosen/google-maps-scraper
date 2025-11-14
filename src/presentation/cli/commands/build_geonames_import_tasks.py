from src.infrastructure.services.tqdm_progress_bar import TqdmProgressBar
from src.infrastructure.services.file_downloader import FileDownloader
from src.infrastructure.services.mappers.country_file_row_mapper import CountryFileRowMapper
from src.infrastructure.services.mappers.geoname_file_row_importer import GeoNameFileRowMapper
from src.infrastructure.services.mappers.alternatename_file_row_mapper import AlternateNameFileRowMapper
from src.infrastructure.services.all_geonames_file_importer import AllGeoNamesFileImporter
from src.infrastructure.services.countries_file_importer import CountriesFileImporter
from src.infrastructure.services.admin_geonames_file_importer import AdminGeoNamesFileImporter
from src.infrastructure.services.city_geonames_file_importer import CityGeoNamesFileImporter
from src.infrastructure.services.alternatenames_file_importer import AlternateNamesFileImporter


def build_geonames_import_tasks(logger):
    """Factory that builds the import configuration with injected dependencies."""
    return [
        {
            "description": "Countries",
            "importer_cls": CountriesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=CountryFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "country_geoname_repo",
        },
        {
            "description": "Administrative Divisions",
            "importer_cls": AdminGeoNamesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeoNameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "admin_geoname_repo",
        },
        {
            "description": "Cities",
            "importer_cls": CityGeoNamesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeoNameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "city_geoname_repo",
        },
        {
            "description": "Alternate Names",
            "importer_cls": AlternateNamesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=AlternateNameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "geoname_alternatename_repo",
        },
        {
            "description": "All GeoNames",
            "importer_cls": AllGeoNamesFileImporter(
                file_downloader=FileDownloader(progress_bar_cls=TqdmProgressBar),
                mapper=GeoNameFileRowMapper(),
                logger=logger
            ),
            "repository_attr": "geoname_repo",
        },
    ]
