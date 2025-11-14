from typing import List, Any
from src.infrastructure.services.mappers.abstract_file_row_mapper import AbstractFileRowMapper
from src.domain.alternatename import AlternateName 


class AlternateNameFileRowMapper(AbstractFileRowMapper[AlternateName]):

    def to_entity(self, row: List[Any]) -> AlternateName:
        
        return AlternateName(
            alternate_name_id=int(row[0]),
            geoname_id=int(row[1]),
            alternate_name=row[3],
            iso_language=row[2],
            is_preferred_name=row[4] == "1" if len(row) > 4 else False,
            is_short_name=row[5] == "1" if len(row) > 5 else False,
            is_colloquial=row[6] == "1" if len(row) > 6 else False,
            is_historic=row[7] == "1" if len(row) > 7 else False,
        )