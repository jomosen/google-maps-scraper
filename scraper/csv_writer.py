import os
import csv
from scraper.repository import Repository

class CSVWriter(Repository):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.results = set()
        self.fieldnames = None
        self.get_all()

    def get_all(self):
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.fieldnames = reader.fieldnames
            for row in reader:
                if row and "place_id" in row:
                    self.results.add(row["place_id"])

    def add(self, item):
        key = item["place_id"]
        if key in self.results:
            return False

        if self.fieldnames is None:
            self.fieldnames = list(item.keys())

        write_header = not os.path.exists(self.file_path)

        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(item)

        self.results.add(key)
        return True

