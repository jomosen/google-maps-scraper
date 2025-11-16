from typing import Generator, Tuple, Iterator
from shared.application.ports.logger_port import LoggerPort
from geonames.application.ports.geonames_importer_port import GeoNamesImporterPort
from shared.application.use_case import UseCase
from geonames.domain.geoname import GeoName
from geonames.domain.repositories.geoname_repository import GeoNameRepository


class ImportGeoNamesUseCase(UseCase):

    def __init__(self, 
                 repository: GeoNameRepository, 
                 importer: GeoNamesImporterPort[GeoName],
                 logger: LoggerPort | None = None):
        
        self.repository = repository
        self.importer = importer
        self.logger = logger
        
    def execute(self) -> Tuple[int, Iterator[int]]: 

        self.importer.ensure_data_is_available()

        total_records = self.importer.count_total_records()
        if total_records == 0:
            raise Exception(f"File have no records to import.")
        
        count = self.repository.count_all()
        if count == total_records:
            return 0, iter([])
            
        self.repository.truncate()

        entities = self.importer.load_entities()

        return total_records, self._batch_insert_generator(entities)
    
    def _batch_insert_generator(self, entities: Generator[GeoName, None, None]) -> Iterator[int]:
            
        batch_size = 5000
        batch = []

        for entity in entities:
            batch.append(entity)
            
            if len(batch) >= batch_size:
                self.repository.bulk_insert(batch)
                
                yield batch_size 
                batch.clear()
        
        if batch:
            self.repository.bulk_insert(batch)
            yield len(batch)

        self.importer.cleanup()