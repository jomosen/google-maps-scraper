class BaseScraper:
    def __init__(self, results_storage, driver):
        self.results_storage = results_storage
        self.driver = driver

    def scrape(self):
        raise NotImplementedError("Subclasses should implement this method")