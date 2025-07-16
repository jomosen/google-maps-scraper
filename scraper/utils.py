import random

from urllib.parse import urlparse

class Utils:

    @staticmethod
    def extract_domain_from_url(url):
        if url == "":
            return ""
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception:
            return ""

    @staticmethod
    def randomize_list_order(list):
        shuffled_list = list.copy()
        random.shuffle(shuffled_list)
        return shuffled_list

    @staticmethod
    def sanitize_filename(query):
        return query.lower().replace(',', '').replace(' ', '_')