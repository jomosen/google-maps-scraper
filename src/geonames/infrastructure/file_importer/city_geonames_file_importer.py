from shared.application.ports.logger_port import LoggerPort
from shared.application.ports.file_downloader_port import FileDownloaderPort
from geonames.infrastructure.file_importer.mappers.abstract_file_row_mapper import AbstractFileRowMapper
from geonames.application.ports.geonames_importer_port import GeoNamesImporterPort
from geonames.infrastructure.file_importer.abstract_geonames_file_importer import AbstractGeoNamesFileImporter
from geonames.domain.geoname import GeoName


class CityGeoNamesFileImporter(AbstractGeoNamesFileImporter, GeoNamesImporterPort[GeoName]):

    FILE_URL = "https://download.geonames.org/export/dump/cities500.zip"

    def __init__(self, file_downloader: FileDownloaderPort, mapper: AbstractFileRowMapper[GeoName], logger: LoggerPort | None = None):
        super().__init__(download_url=self.FILE_URL, file_downloader=file_downloader, mapper=mapper, logger=logger)