from shared.infrastructure.adapters.tqdm_progress_bar import TqdmProgressBar
from shared.infrastructure.adapters.file_downloader import FileDownloader
from geonames.infrastructure.file_importer.mappers.country_file_row_mapper import CountryFileRowMapper
from geonames.infrastructure.file_importer.mappers.geoname_file_row_importer import GeoNameFileRowMapper
from geonames.infrastructure.file_importer.mappers.alternatename_file_row_mapper import AlternateNameFileRowMapper
from geonames.infrastructure.file_importer.all_geonames_file_importer import AllGeoNamesFileImporter
from geonames.infrastructure.file_importer.countries_file_importer import CountriesFileImporter
from geonames.infrastructure.file_importer.admin_geonames_file_importer import AdminGeoNamesFileImporter
from geonames.infrastructure.file_importer.city_geonames_file_importer import CityGeoNamesFileImporter
from geonames.infrastructure.file_importer.alternatenames_file_importer import AlternateNamesFileImporter


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
