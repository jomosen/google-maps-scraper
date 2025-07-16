import os
import pytest

from scraper.google_maps import GoogleMapsScraper
from scraper.utils import Utils
from scraper.csv_writer import CSVWriter
from scraper.results_storage import ResultsStorage
from scraper.selenium_driver import SeleniumDriver

@pytest.fixture
def scraper_instance():
    
    test_file = "results/test_output.csv"
    repository = CSVWriter(test_file)
    results_storage = ResultsStorage(repository)

    selenium_driver = SeleniumDriver()

    return GoogleMapsScraper(lang="es", query="physiotherapist in javea", results_storage=results_storage, driver=selenium_driver)

def test_scraper_runs(scraper_instance):

    scraper_instance.scrape()

    results_storage = scraper_instance.results_storage
    results_storage.save()

    repository = results_storage.repository
    assert os.path.exists(repository.file_path), f"Expected output CSV not found: {repository.file_path}"

    os.remove(repository.file_path)