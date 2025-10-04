from app.domain.scraping.repositories.scraping_repository import ScrapingRepository
from app.application.scraping.services.task_generator import TaskGenerator
from app.domain.scraping.entities.scraping import Scraping
from app.domain.scraping.value_objects.status_vo import StatusVO
from app.application.scraping.services.gmaps_scraper import GMapsScraper

def run_scraper(scraper: GMapsScraper):
    if scraper.scraping is None:
        raise ValueError(f"Scraping with not found")

    scraper.run()
    return scraper
