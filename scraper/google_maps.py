import time
import re
import json
import unicodedata

from scraper.base import BaseScraper
from scraper.utils import Utils
from . import selectors

class GoogleMapsScraper(BaseScraper):
    def __init__(self, lang, queries, results_storage, driver):
        super().__init__(results_storage, driver)
        self.lang = lang
        self.queries = queries

    def scrape(self):
        self.load_google_maps_url()
        self.accept_cookies()
        for query in self.queries:
            self.search(query)
            self.load_listings()
            self.extract_listings_data()

    def get_google_maps_url(self):
        return f"https://www.google.com/maps?hl={self.lang}"
    
    def load_google_maps_url(self):
        google_maps_url = self.get_google_maps_url()
        self.driver.load_url(google_maps_url)

    def accept_cookies(self):
        self.driver.click_element_when_present(selectors.ACCEPT_COOKIES_BTN_SELECTOR)

    def search(self, query):
        print(f"Searching for: {query}")
        self.driver.send_keys_after_waiting(selectors.SEARCH_BOX_SELECTOR, query)
        print("Search submitted.")

    def load_listings(self):
        print("Scrolling the sidebar to load all of the results...")
        self.driver.scroll_element_until_end(selectors.SIDEBAR_CONTAINER_SELECTOR)
        print("Finished scrolling.")
        
    def extract_listings_data(self):
        listings = self.get_listings()
        for i, listing in enumerate(listings):
            try:
                print(f"Clicking listing {i+1} of {len(listings)}")
                item = self.extract_listing_data(listing)
                self.results_storage.add(item)
                print(f"Listing {item['name']} processed successfully.")
            except Exception as e:
                print(f"Failed to process listing {i+1}: {e}")
    
    def get_listings(self):
        listings = self.driver.get_parents_of_elements(selectors.LISTING_ITEM_CHILD_SELECTOR)
        return Utils.randomize_list_order(listings)

    def extract_listing_data(self, listing):
        try:
            self.driver.scroll_until_element_into_view(listing)
            detail_url = self.driver.get_element_attribute_within_parent(listing, 'a', 'href')
            listing.click()
            time.sleep(0.5)

            item = {}
            item['place_id'] = self.get_place_id_from_listing_detail_url(detail_url)

            detail_panel = self.driver.get_element(selectors.DETAIL_PANEL_SELECTOR)
            item['name'] = self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_NAME_SELECTOR)
            item['address'] = self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_ADDRESS_SELECTOR)
            
            num_reviews = self.driver.get_element_text_within_parent(listing, selectors.BUSINESS_NUM_REVIEWS_SELECTOR)
            item['num_reviews'] = num_reviews.strip("()") if num_reviews else None
            item['rating'] = self.driver.get_element_text_within_parent(listing, selectors.BUSINESS_RATING_SELECTOR)

            coordinates = self.extract_coordinates_from_maps_url(detail_url)
            item['latitude'] = coordinates['latitude']
            item['longitude'] = coordinates['longitude']

            item['phone'] = self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_PHONE_SELECTOR)
            item['category'] = self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_CATEGORY_SELECTOR)
            item['website_url'] = self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_WEBSITE_SELECTOR, "href")
            item['booking_url'] = self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_BOOKING_LINK_SELECTOR, "href")
            item['main_image'] = self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_MAIN_IMAGE_SELECTOR, "src")
            
            item['attributes'] = self.get_attributes(detail_panel)
            item['info'] = self.get_info(detail_panel)
            item['hours'] = self.get_hours(detail_panel)
            item['reviews'] = self.get_reviews(detail_panel)

            item['domain'] = Utils.extract_domain_from_url(item['website_url'])
            
            return item

        except Exception as e:
            print(f"Failed to process listing: {e}")

    def get_place_id_from_listing_detail_url(self, detail_url):
        match = re.search(r'19s([a-zA-Z0-9_-]+)(?=\?|$)', detail_url)    
        place_id = ""

        if match:
            place_id = match.group(1)
            print("Place ID:", place_id)
        else:
            raise Exception("No place_id found.")
        return place_id
    
    def extract_coordinates_from_maps_url(self, url):
        coordinates = {
            "latitude": None,
            "longitude": None
        }
        match = re.search(r'!3d([-0-9.]+)!4d([-0-9.]+)', url)    
        if match:
            coordinates["latitude"] = float(match.group(1))
            coordinates["longitude"] = float(match.group(2))
        return coordinates

    def get_hours(self, detail_panel):
        hours = {}
        weekdays = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_HOURS_ITEM_SELECTOR)
        for weekday in weekdays:
            data_value = weekday.get_attribute('data-value')
            cleaned_text = unicodedata.normalize("NFKC", data_value).replace('\xa0', ' ').strip()
            text_chunks = cleaned_text.split(", ")
            if len(text_chunks) >= 2:
                day = text_chunks[0]
                time = ", ".join(text_chunks[1:])
                hours[day] = time
        return json.dumps(hours)

    def get_attributes(self, detail_panel):
        attributes = []
        items = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_ATTRIBUTES_SELECTOR)
        for item in items:
            try:
                attributes.append(item.get_attribute("aria-label"))
            except:
                None
        return json.dumps(attributes)

    def get_info(self, detail_panel):
        divs = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_METADATA_SELECTOR)
        for div in divs:
            if not self.driver.get_elements_within_parent(div, "div"):
                return div.text
        return ""

    def get_reviews(self, detail_panel):
        reviews = []
        reviews_wrappers = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_REVIEWS_SELECTOR)
        for review_wrapper in reviews_wrappers:
            try:
                review_id = review_wrapper.get_attribute("data-review-id")
                self.view_full_review(review_wrapper)
                review = {
                    "id": review_id,
                    "rating": self.get_review_rating(review_wrapper),
                    "author": self.get_review_author(review_wrapper),
                    "text": self.driver.get_element_text_within_parent(review_wrapper, f'#{review_id}'),
                    "lang": self.driver.get_element_attribute_within_parent(review_wrapper, f'#{review_id}', "lang"),
                }
                reviews.append(review)
            except:
                pass
        return json.dumps(reviews)
    
    def view_full_review(self, review_wrapper):
        view_more_action = self.driver.get_element_within_parent(review_wrapper, selectors.BUSINESS_REVIEW_VIEW_MORE_SELECTOR)
        if view_more_action:
            self.driver.scroll_until_element_into_view(view_more_action)
            time.sleep(0.5)
            view_more_action.click()
            time.sleep(0.5)

    def get_review_rating(self, review_wrapper):
        review_container = self.driver.get_element_within_parent(review_wrapper, selectors.BUSINESS_REVIEW_CONTAINER_CHILD_SELECTOR)
        stars = self.driver.get_element_within_parent(review_container, selectors.BUSINESS_REVIEW_RATING_SELECTOR).get_attribute("aria-label")
        match = re.search(r'\d+(?:\.\d+)?', stars)
        if match:
            return float(match.group())
        raise Exception("No rating found in review.")
    
    def get_review_author(self, review_wrapper):
        reviewer_container = self.driver.get_element_within_parent(review_wrapper, selectors.BUSINESS_REVIEWER_CONTAINER_CHILD_SELECTOR)
        if reviewer_container:
            return reviewer_container.text
        raise Exception("No reviewer found in review.")