import os
import requests
from dotenv import load_dotenv
from typing import Generator, List, Dict, Any
from functools import cached_property
from src.application.contracts.abstract_geonames_importer import AbstractGeoNamesImporter
from src.domain.country import Country
from src.infrastructure.services.mappers.country_api_mapper import CountryApiMapper


class CountriesApiImporter(AbstractGeoNamesImporter[Country]):

    ENDPOINT_URL = "http://api.geonames.org/countryInfoJSON"

    def __init__(self, mapper: CountryApiMapper):

        self.mapper = mapper

        load_dotenv() 
        
        self._username = os.getenv("GEONAMES_USERNAME")
        if not self._username:
            raise ValueError("GEONAMES_USERNAME environment variable not set in configuration.")
    
    def ensure_data_is_available(self):
        if not self._fetch_api_data:
            raise RuntimeError("GeoNames API returned no data or invalid response.")
    
    def count_total_records(self) -> int:
        return len(self._fetch_api_data)

    
    def load_entities(self) -> Generator[Country, None, None]:

        country_data_list = self._fetch_api_data

        for country_data in country_data_list:
            country = self.mapper.from_api(country_data)
            yield country

    def cleanup(self):
        pass

    @cached_property
    def _fetch_api_data(self) -> List[Dict[str, Any]]:

        api_url = f"{self.ENDPOINT_URL}?username={self._username}"
        
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch data from GeoNames API: {e}")

        data = response.json()
        geonames = data.get("geonames")
        if not isinstance(geonames, list):
            raise ValueError("Unexpected response format from GeoNames API.")
        return geonames