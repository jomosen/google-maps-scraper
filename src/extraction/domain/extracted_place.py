from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from extraction.domain.value_objects.extracted_place_attributes import PlaceAttributes
from extraction.domain.value_objects.extracted_place_hours import PlaceHours
from extraction.domain.extracted_place_review import ExtractedPlaceReview


@dataclass
class ExtractedPlace:
    
    place_id: str
    name: Optional[str] = None
    address: Optional[str] = None
    num_reviews: Optional[int] = None
    rating: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    plus_code: Optional[str] = None
    category: Optional[str] = None
    website_url: Optional[str] = None
    booking_url: Optional[str] = None
    domain: Optional[str] = None
    main_image: Optional[str] = None
    attributes: Optional[PlaceAttributes] = None
    description: Optional[str] = None
    hours: Optional[PlaceHours] = None
    reviews: List[ExtractedPlaceReview] = field(default_factory=list)
    task_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None