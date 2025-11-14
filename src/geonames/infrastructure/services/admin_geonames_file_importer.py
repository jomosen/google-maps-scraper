import os
import mmap
from typing import Generator
from src.geonames.application.contracts.abstract_logger import AbstractLogger
from src.geonames.application.contracts.abstract_file_downloader import AbstractFileDownloader
from src.geonames.infrastructure.services.mappers.abstract_file_row_mapper import AbstractFileRowMapper
from src.geonames.application.contracts.abstract_geonames_importer import AbstractGeoNamesImporter
from src.geonames.infrastructure.services.abstract_geonames_file_importer import AbstractGeoNamesFileImporter
from src.geonames.domain.geoname import GeoName


class AdminGeoNamesFileImporter(AbstractGeoNamesFileImporter, AbstractGeoNamesImporter[GeoName]):

    FILE_URL = "https://download.geonames.org/export/dump/allCountries.zip"

    def __init__(self, file_downloader: AbstractFileDownloader, mapper: AbstractFileRowMapper[GeoName], logger: AbstractLogger | None = None):
        super().__init__(download_url=self.FILE_URL, file_downloader=file_downloader, mapper=mapper, logger=logger)

    def count_total_records(self) -> int:

        file_path = self.read_target_path

        if not file_path.exists() or os.path.getsize(file_path) == 0:
            return 0

        valid_codes = {b"ADM1", b"ADM2", b"ADM3", b"ADM4"}

        try:
            with open(file_path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    count = 0
                    for line in iter(mm.readline, b""):
                        # feature code is in column 7 (index 6 or 7 depending on tab-split)
                        parts = line.split(b"\t")
                        if len(parts) > 7 and parts[7] in valid_codes:
                            count += 1
                    return count

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading file with mmap: {e}. Returning 0 records.")
            return 0


    def load_entities(self) -> Generator[GeoName, None, None]:
        for raw_row in self.read_raw_data():
            try:
                if raw_row[7] not in ('ADM1', 'ADM2', 'ADM3', 'ADM4'):
                    raise ValueError(
                        f"Unsupported GeoName for mapping. Filtering: "
                        f"Feature Code '{raw_row[7]}' must be one of ('ADM1', 'ADM2', 'ADM3', 'ADM4')."
                    )
                yield self.mapper.to_entity(raw_row)
            except ValueError:
                continue
            except Exception as e:
                print(f"Error processing row {raw_row}: {e}")