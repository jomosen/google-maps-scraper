class ResultsStorage():
    def __init__(self, repository):
        self.results = []
        self.repository = repository

    def add(self, item):
        self.results.append(item)

    def get_all(self):
        return self.results

    def is_empty(self):
        return len(self.results) == 0
    
    def save(self):
        if self.is_empty():
            print("No results to save.")
        else:
            self.repository.save(self.results)