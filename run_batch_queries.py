import argparse
import json

from scraper.results_storage import ResultsStorage
from scraper.csv_writer import CSVWriter
from scraper.selenium_driver import SeleniumDriver
from scraper.google_maps import GoogleMapsScraper
from scraper.utils import Utils
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Run batch Google Maps scrapes from JSON.")
    parser.add_argument("--json", required=True, help="Path to JSON file with queries and language")
    parser.add_argument("--lang", default="en", help="Language (default: en)")
    
    args = parser.parse_args()

    with open(args.json, 'r', encoding='utf-8') as f:
        queries = json.load(f)

    if not queries:
        print("No queries found in the JSON file.")
        return
    
    lang = args.lang

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"results/{timestamp}.csv"
    repository = CSVWriter(file_path)
    results_storage = ResultsStorage(repository)

    selenium_driver = SeleniumDriver()
    
    scraper = GoogleMapsScraper(
        lang=lang,
        queries=queries,
        results_storage=results_storage,
        driver=selenium_driver
    )

    scraper.scrape()
        
    results_storage.save()

if __name__ == "__main__":
    main()
