from typing import List, Dict, Any
from extraction.application.ports.geoname_query_port import GeoNameQueryPort
from extraction.domain.enums.extraction_job_depth_level import ExtractionJobDepthLevel
from extraction.domain.enums.extraction_job_scope import ExtractionJobScope
from extraction.domain.value_objects.geoname import GeoName
from extraction.domain.value_objects.geoname_selection_params_for_extraction_job import GeoNameSelectionParamsForExtractionJob


class GeoNameSelectionService():

    def __init__(self, geoname_query_service: GeoNameQueryPort):
        self.geoname_query_service = geoname_query_service

    def select(self, params: GeoNameSelectionParamsForExtractionJob) -> List[GeoName]:

        geonames: List[GeoName] = []

        try:
            filters: Dict[str, Any] = {}

            if params.scope == ExtractionJobScope.COUNTRY and params.scope_geoname_id is not None:

                country = self.geoname_query_service.find_country_by_id(params.scope_geoname_id)
                if not country:
                    raise ValueError(f"Country with geoname ID {params.scope_geoname_id} not found.")
                
                filters["countryCode"] = country.iso_alpha2

                if params.depth_level == ExtractionJobDepthLevel.ADMIN1:
                    filters["featureCode"] = "ADM1"
                elif params.depth_level == ExtractionJobDepthLevel.ADMIN2:
                    filters["featureCode"] = "ADM2"
                elif params.depth_level == ExtractionJobDepthLevel.ADMIN3:
                    filters["featureCode"] = "ADM3"
                else:
                    if params.min_population is not None:
                        filters["minPopulation"] = params.min_population

            if filters:
                if params.depth_level in {ExtractionJobDepthLevel.ADMIN1, ExtractionJobDepthLevel.ADMIN2, ExtractionJobDepthLevel.ADMIN3}:
                    geonames = self.geoname_query_service.find_admin_geonames(filters)
                else:
                    geonames = self.geoname_query_service.find_city_geonames(filters)

        except Exception as e:
            raise e
        
        return geonames
        
