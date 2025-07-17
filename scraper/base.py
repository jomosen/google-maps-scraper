class BaseScraper:
    def __init__(self, repository, driver):
        self.repository = repository
        self.driver = driver

    def scrape(self):
        raise NotImplementedError("Subclasses should implement this method")