import os
import pytest

from scraper.google_maps import GoogleMapsScraper
from scraper.csv_writer import CSVWriter
from scraper.selenium_driver import SeleniumDriver

@pytest.fixture
def scraper_instance():
    
    test_file = "results/test_output.csv"
    repository = CSVWriter(test_file)

    selenium_driver = SeleniumDriver()

    return GoogleMapsScraper(lang="en", query="boat rental in javea", repository=repository, driver=selenium_driver)

def test_single_query(scraper_instance):

    scraper_instance.scrape()

    file_path = scraper_instance.repository.file_path

    assert os.path.exists(file_path), f"Expected output CSV not found: {file_path}"

    os.remove(file_path)