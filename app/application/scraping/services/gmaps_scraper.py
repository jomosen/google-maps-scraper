import time
import random
from app.domain.scraping.interfaces.browser_driver import BrowserDriver
from app.domain.scraping.entities.task import Task
from app.domain.scraping.entities.scraping import Scraping
from app.domain.place.entities.place import Place
from app.domain.scraping.repositories.scraping_repository import ScrapingRepository
from app.domain.place.repositories.place_repository import PlaceRepository
from app.infrastructure.scraping.gmaps import selectors
from app.application.scraping.mappers.task_mapper import TaskMapper
from app.application.place.services.places_extractor import PlacesExtractor

class GMapsScraper:
    def __init__(
        self,
        scraping: Scraping,
        browser_driver: BrowserDriver,
        scraping_repository: ScrapingRepository,
        place_repository: PlaceRepository,
    ):
        self.scraping = scraping
        self.browser_driver = browser_driver
        self.scraping_repository = scraping_repository
        self.place_repository = place_repository

    def _open_gmaps(self):
        gmaps_url = f"https://www.google.com/maps?hl={self.scraping.options.language}"
        self.browser_driver.go_to(gmaps_url)

    def _run_task(self, task: Task) -> list[Place]:
        places = []

        if task.is_completed():
            return places
    
        self._perform_task_search(task)

        self._scroll_until_end()

        places_extractor = PlacesExtractor(self.browser_driver, self.place_repository, self.scraping.options.max_reviews)
        places = places_extractor.extract_places(task.id)

        return places
    
    def _close_cookies_dialog(self):
        self.browser_driver.click(selectors.ACCEPT_COOKIES_BTN_SELECTOR)

    def _perform_task_search(self, task):
        query = TaskMapper.to_gmaps_query(task)
        self.browser_driver.send_keys(selectors.SEARCH_BOX_SELECTOR, query)

    def _scroll_until_end(self):
        self.browser_driver.scroll(selectors.SIDEBAR_CONTAINER_SELECTOR)

    def run(self):
        if self.scraping.is_completed():
            return
        
        self._open_gmaps()

        self._close_cookies_dialog()

        i = 0
        number_of_tasks_until_next_long_wait = random.randint(2, 6)

        for task in self.scraping.tasks:
            if task.status.pending():
                places = self._run_task(task)

                for place in places:
                    self.place_repository.save(place)

                task.mark_completed()

                i += 1
                if i >= number_of_tasks_until_next_long_wait:
                    time.sleep(random.randint(60, 120))

        self.scraping.mark_completed()
        self.scraping_repository.save(self.scraping)

        self.browser_driver.close()
