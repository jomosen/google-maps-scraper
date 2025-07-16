import argparse

from scraper.results_storage import ResultsStorage
from scraper.csv_writer import CSVWriter
from scraper.selenium_driver import SeleniumDriver
from scraper.google_maps import GoogleMapsScraper
from scraper.utils import Utils

def main():
    parser = argparse.ArgumentParser(description="Run Google Maps scraper.")
    parser.add_argument("--query", required=True, help="Query to search (e.g. 'physiotherapist in javea')")
    parser.add_argument("--lang", default="en", help="Language (default: en)")

    args = parser.parse_args()

    file_path = f"results/{Utils.sanitize_filename(args.query)}.csv"
    repository = CSVWriter(file_path)
    results_storage = ResultsStorage(repository)
    selenium_driver = SeleniumDriver()

    scrapers = [
        GoogleMapsScraper(lang=args.lang, queries=[args.query], results_storage=results_storage, driver=selenium_driver)
    ]

    for scraper in scrapers:
        scraper.scrape()
    
    results_storage.save()

if __name__ == "__main__":
    main()