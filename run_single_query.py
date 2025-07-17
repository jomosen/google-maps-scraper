import argparse

from scraper.results_storage import ResultsStorage
from scraper.csv_writer import CSVWriter
from scraper.selenium_driver import SeleniumDriver
from scraper.google_maps import GoogleMapsScraper
from scraper.utils import Utils

def main():
    parser = argparse.ArgumentParser(description="Run Google Maps scraper.")
    parser.add_argument("--query", required=True, help="Query to search (e.g. 'boat rental in javea')")
    parser.add_argument("--lang", default="en", help="Language (default: en)")
    parser.add_argument("--max_reviews", action="store_true", help="Scrape up to 50 reviews per place")

    args = parser.parse_args()

    if args.max_reviews:
        reviews_limit = 50
    else:
        reviews_limit = None

    file_path = f"results/{Utils.sanitize_filename(args.query)}.csv"
    repository = CSVWriter(file_path)
    selenium_driver = SeleniumDriver()

    scrapers = [
        GoogleMapsScraper(lang=args.lang, queries=[args.query], repository=repository, driver=selenium_driver, max_reviews=reviews_limit)
    ]

    for scraper in scrapers:
        scraper.scrape()
    
if __name__ == "__main__":
    main()