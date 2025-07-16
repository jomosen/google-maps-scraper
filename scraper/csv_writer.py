import pandas as pd

from scraper.repository import Repository

class CSVWriter(Repository):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def save(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.file_path, index=False)
