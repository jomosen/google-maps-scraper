from shared.application.contracts.abstract_logger import AbstractLogger
from shared.application.contracts.abstract_file_downloader import AbstractFileDownloader
from geonames.infrastructure.services.mappers.abstract_file_row_mapper import AbstractFileRowMapper
from geonames.application.contracts.abstract_geonames_importer import AbstractGeoNamesImporter
from geonames.infrastructure.services.abstract_geonames_file_importer import AbstractGeoNamesFileImporter
from geonames.domain.geoname import GeoName


class CityGeoNamesFileImporter(AbstractGeoNamesFileImporter, AbstractGeoNamesImporter[GeoName]):

    FILE_URL = "https://download.geonames.org/export/dump/cities500.zip"

    def __init__(self, file_downloader: AbstractFileDownloader, mapper: AbstractFileRowMapper[GeoName], logger: AbstractLogger | None = None):
        super().__init__(download_url=self.FILE_URL, file_downloader=file_downloader, mapper=mapper, logger=logger)