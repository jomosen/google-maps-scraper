import re
import time
import json
import html
import unicodedata
import logging
from typing import Dict, List, Any, Optional

from app.infrastructure.scraping.gmaps import selectors
from app.application.shared.utils import Utils
from app.infrastructure.logging.logger import logger
from app.domain.place.entities.place import Place

class PlacesExtractor:
    """Servicio encargado de extraer información de los lugares listados en Google Maps."""

    def __init__(self, browser_driver, place_repository, max_reviews: int = 3):
        self.driver = browser_driver
        self.repository = place_repository
        self.max_reviews = max_reviews

    def extract_places(self, task_id: str) -> None:
        places = []
        listings = self._get_listings()
        for i, listing in enumerate(listings):
            try:
                place = self._extract_place(listing)
                if place:
                    place.task_id = task_id
                    places.append(place)
            except Exception as e:
                logger.warning(f"Failed to process listing {i+1}: {e}", exc_info=True)
                continue
        return places

    def _get_listings(self):
        listings = self.driver.get_parents_of_elements(
            selectors.LISTING_ITEM_CHILD_SELECTOR
        )
        return Utils.randomize_list_order(listings)

    def _extract_place(self, listing) -> Place:
        self.driver.scroll_until_element_into_view(listing)
        detail_url = self.driver.get_element_attribute_within_parent(listing, "a", "href")
        listing.click()
        time.sleep(0.5)

        detail_panel = self.driver.get_element(selectors.DETAIL_PANEL_SELECTOR)

        place_name = self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_NAME_SELECTOR)

        data = {
            "place_id": self._get_place_id_from_listing_detail_url(detail_url),
            "name": place_name,
            "address": self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_ADDRESS_SELECTOR),
            "num_reviews": self._parse_num_reviews(
                self.driver.get_element_text_within_parent(listing, selectors.BUSINESS_NUM_REVIEWS_SELECTOR)
            ),
            "rating": self.driver.get_element_text_within_parent(listing, selectors.BUSINESS_RATING_SELECTOR),
            "latitude": None,
            "longitude": None,
            "phone": self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_PHONE_SELECTOR),
            "category": self.driver.get_element_text_within_parent(detail_panel, selectors.BUSINESS_CATEGORY_SELECTOR),
            "website_url": self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_WEBSITE_SELECTOR, "href"),
            "booking_url": self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_BOOKING_LINK_SELECTOR, "href"),
            "main_image": self.driver.get_element_attribute_within_parent(detail_panel, selectors.BUSINESS_MAIN_IMAGE_SELECTOR, "src"),
            "attributes": self._get_attributes(detail_panel),
            "description": self._get_info(detail_panel),
            "hours": self._get_hours(detail_panel),
            "reviews": self._get_reviews(detail_panel, place_name),
            "domain": None
        }

        # Coordinates
        coordinates = self._extract_coordinates_from_maps_url(detail_url)
        data["latitude"] = coordinates.get("latitude")
        data["longitude"] = coordinates.get("longitude")

        # Domain
        data["domain"] = Utils.extract_domain_from_url(data["website_url"])

        return Place(**data)

    # Helpers
    def _parse_num_reviews(self, text: Optional[str]) -> Optional[str]:
        return text.strip("()") if text else None

    def _get_place_id_from_listing_detail_url(self, detail_url: str) -> str:
        match = re.search(r"19s([a-zA-Z0-9_-]+)(?=\?|$)", detail_url)
        if not match:
            raise ValueError("No place_id found in detail_url")
        return match.group(1)

    def _extract_coordinates_from_maps_url(self, url: str) -> Dict[str, Optional[float]]:
        match = re.search(r"!3d([-0-9.]+)!4d([-0-9.]+)", url)
        if match:
            return {"latitude": float(match.group(1)), "longitude": float(match.group(2))}
        return {"latitude": None, "longitude": None}

    def _get_hours(self, detail_panel) -> str:
        hours = {}
        weekdays = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_HOURS_ITEM_SELECTOR)
        for weekday in weekdays:
            data_value = weekday.get_attribute("data-value")
            cleaned_text = unicodedata.normalize("NFKC", data_value).replace("\xa0", " ").strip()
            text_chunks = cleaned_text.split(", ")
            if len(text_chunks) >= 2:
                day, time_value = text_chunks[0], ", ".join(text_chunks[1:])
                hours[day] = time_value
        return json.dumps(hours)

    def _get_attributes(self, detail_panel) -> str:
        attributes = []
        items = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_ATTRIBUTES_SELECTOR)
        for item in items:
            try:
                attributes.append(item.get_attribute("aria-label"))
            except Exception:
                continue
        return json.dumps(attributes)

    def _get_info(self, detail_panel) -> str:
        divs = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_METADATA_SELECTOR)
        for div in divs:
            if not self.driver.get_elements_within_parent(div, "div"):
                return div.text
        return ""

    def _get_reviews(self, detail_panel, place_name) -> str:
        if self.max_reviews > 3:
            reviews = self._get_reviews_from_reviews_tab(detail_panel, place_name)
        else:
            reviews = self._get_reviews_from_overview_tab(detail_panel)

        print(f"Extracted {len(reviews)} reviews")

        if len(reviews) == 0:
            return ""

        return json.dumps(reviews)

    def _get_reviews_from_overview_tab(self, detail_panel) -> List[Dict[str, Any]]:
        wrappers = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_REVIEWS_SELECTOR)
        return self._extract_reviews_from_wrappers(wrappers)

    def _get_reviews_from_reviews_tab(self, detail_panel, place_name) -> List[Dict[str, Any]]:
        self.driver.click_element_when_present(selectors.DETAIL_PANEL_REVIEWS_TAB_SELECTOR)
        time.sleep(3)
        self.driver.scroll_element(selectors.DETAIL_PANEL_REVIEWS_SCROLLABLE_SELECTOR.format(place_name=place_name), self.max_reviews)

        detail_panel = self.driver.get_element(selectors.DETAIL_PANEL_SELECTOR)
        wrappers = self.driver.get_elements_within_parent(detail_panel, selectors.BUSINESS_REVIEWS_SELECTOR)

        return self._extract_reviews_from_wrappers(wrappers)

    def _extract_reviews_from_wrappers(self, wrappers) -> List[Dict[str, Any]]:
        reviews = []
        for wrapper in wrappers:
            try:
                review = self._extract_review_from_wrapper(wrapper)
                reviews.append(review)
                if self.max_reviews and len(reviews) >= self.max_reviews:
                    break
            except Exception as e:
                print(f"Error extracting review from wrapper: {e}")
                continue
        return reviews

    def _extract_review_from_wrapper(self, wrapper) -> Dict[str, Any]:
        review_id = wrapper.get_attribute("data-review-id")
        self._view_full_review(wrapper)
        return {
            "id": review_id,
            "rating": self._get_review_rating(wrapper),
            "author": self._get_review_author(wrapper),
            "text": self.driver.get_element_text_within_parent(wrapper, f"#{review_id}"),
            "lang": self.driver.get_element_attribute_within_parent(wrapper, f"#{review_id}", "lang"),
            "photos": self._get_review_photos(wrapper),
        }

    def _view_full_review(self, wrapper) -> None:
        view_more = self.driver.get_element_within_parent(wrapper, selectors.BUSINESS_REVIEW_VIEW_MORE_SELECTOR)
        if view_more:
            self.driver.scroll_until_element_into_view(view_more)
            time.sleep(0.5)
            view_more.click()
            time.sleep(0.5)

    def _get_review_rating(self, wrapper) -> float:
        container = self.driver.get_element_within_parent(wrapper, selectors.BUSINESS_REVIEW_CONTAINER_CHILD_SELECTOR)
        stars = self.driver.get_element_within_parent(container, selectors.BUSINESS_REVIEW_RATING_SELECTOR).get_attribute("aria-label")
        match = re.search(r"\d+(?:\.\d+)?", stars)
        if not match:
            raise ValueError("No rating found in review")
        return float(match.group())

    def _get_review_author(self, wrapper) -> str:
        container = self.driver.get_element_within_parent(wrapper, selectors.BUSINESS_REVIEWER_CONTAINER_CHILD_SELECTOR)
        if container:
            return container.text_content().strip()
        raise ValueError("No reviewer found in review")

    def _get_review_photos(self, wrapper) -> List[str]:
        urls = []
        containers = self.driver.get_elements_within_parent(wrapper, selectors.BUSINESS_REVIEW_PHOTO_SELECTOR)
        for container in containers:
            style = container.get_attribute("style")
            url = self._clean_review_photo_url(style)
            if url:
                urls.append(url)
        return urls

    def _clean_review_photo_url(self, style: str) -> Optional[str]:
        match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
        return html.unescape(match.group(1)) if match else None
