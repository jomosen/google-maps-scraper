import argparse
from scraper.results_storage import ResultsStorage
from scraper.csv_writer import CSVWriter
from scraper.selenium_driver import SeleniumDriver
from scraper.google_maps import GoogleMapsScraper

def main():
    parser = argparse.ArgumentParser(description="Run Google Maps scraper.")
    parser.add_argument("--query", required=True, help="Query to search (e.g. 'physiotherapist in javea')")
    parser.add_argument("--lang", default="en", help="Language (default: en)")

    args = parser.parse_args()

    file_path = f"results/{args.query.lower().replace(' ', '_')}.csv"

    repository = CSVWriter(file_path)
    results_storage = ResultsStorage(repository)
    selenium_driver = SeleniumDriver()

    scrapers = [
        GoogleMapsScraper(lang=args.lang, query=args.query, results_storage=results_storage, driver=selenium_driver)
    ]

    for scraper in scrapers:
        scraper.scrape()
    
    results_storage.save()

if __name__ == "__main__":
    main()