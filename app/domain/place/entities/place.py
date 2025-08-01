from dataclasses import dataclass, field
from typing import Optional, List, Type

from app.domain.place.value_objects.metadata_vo import MetadataVO
from app.domain.place.value_objects.hours_vo import HoursVO
from app.domain.place.value_objects.reviews_vo import ReviewsVO
#from app.domain.place.interfaces.place_enrichment import PlaceEnrichment


@dataclass
class Place:
    place_id: str
    name: Optional[str] = None
    address: Optional[str] = None
    num_reviews: Optional[str] = None
    rating: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    website_url: Optional[str] = None
    booking_url: Optional[str] = None
    domain: Optional[str] = None
    main_image: Optional[str] = None
    meta_data: Optional[MetadataVO] = None
    description: Optional[str] = None
    hours: Optional[HoursVO] = None
    reviews: Optional[ReviewsVO] = None

    # enrichments: List[PlaceEnrichment] = field(default_factory=list)

    # def add_enrichment(self, enrichment: PlaceEnrichment) -> None:
    #     self.enrichments.append(enrichment)

    # def get_enrichment(self, enrichment_class: Type[PlaceEnrichment]) -> Optional[PlaceEnrichment]:
    #     for enrichment in self.enrichments:
    #         if isinstance(enrichment, enrichment_class):
    #             return enrichment
    #     return None
