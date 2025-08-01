from app.domain.scraping.interfaces.browser_driver import BrowserDriver
from app.domain.scraping.entities.task import Task
from app.domain.scraping.entities.scraping import Scraping
from app.domain.place.entities.place import Place
from app.domain.scraping.repositories.scraping_repository import ScrapingRepository
from app.domain.place.repositories.place_repository import PlaceRepository
from app.infrastructure.scraping.gmaps import selectors
from app.application.scraping.mappers.task_mapper import TaskMapper

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

        self._close_cookies_dialog()

        if task.is_completed():
            return places
    
        self._perform_task_search(task)

        self._scroll_until_end()

        # Extract places

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

        for task in self.scraping.tasks:
            if task.status.pending():
                places = self._run_task(task)

                for place in places:
                    self.place_repository.save(place)

                task.mark_completed()

        self.scraping.mark_completed()
        self.scraping_repository.save(self.scraping)

        self.browser_driver.close()
