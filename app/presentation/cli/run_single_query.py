from app.application.scraping.use_cases.create_scraping import create_scraping
from app.application.scraping.use_cases.run_scraper import run_scraper
from app.application.scraping.services.gmaps_scraper import GMapsScraper
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO
from app.application.scraping.services.task_generator import TaskGenerator
from app.domain.scraping.value_objects.browser_config_vo import BrowserConfigVO
from app.infrastructure.scraping.browser.selenium_driver import SeleniumDriver
from app.infrastructure.scraping.browser.playwright_driver import PlaywrightDriver
from app.infrastructure.persistence.repositories.sqlalchemy_scraping_repository import SQLAlchemyScrapingRepository
from app.infrastructure.persistence.repositories.sqlalchemy_place_repository import SQLAlchemyPlaceRepository
from app.infrastructure.persistence.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def main():
    keywords = ["boat rental"]
    locations = ["javea"]
    language = "en"
    max_reviews = 3

    scraping_options = ScrapingOptionsVO(
        keywords=keywords,
        locations=locations,
        language=language,
        max_reviews=max_reviews
    )

    engine = create_engine("sqlite:///scraping.db")
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        scraping_repository = SQLAlchemyScrapingRepository(session)
        task_generator = TaskGenerator()
        scraping = create_scraping(scraping_options, scraping_repository, task_generator)

        browser_config = BrowserConfigVO()
        browser_driver = PlaywrightDriver(browser_config)
        
        place_repository = SQLAlchemyPlaceRepository(session)
        scraper = GMapsScraper(scraping=scraping, browser_driver=browser_driver, scraping_repository=scraping_repository, place_repository=place_repository)
        scraper = run_scraper(scraper)

    finally:
        session.close()

if __name__ == "__main__":
    main()