from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, JSON
from sqlalchemy.orm import relationship
from extraction.infrastructure.persistence.database.base import ExtractionBase as Base


class ExtractionPlaceModel(Base):
    __tablename__ = "extracted_places"

    place_id = Column(String(191), primary_key=True, nullable=False)
    name = Column(String(255))
    address = Column(String(255))
    num_reviews = Column(Integer)
    rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(50))
    plus_code = Column(String(100))
    category = Column(String(255))
    website_url = Column(String(255))
    booking_url = Column(String(255))
    main_image = Column(String(255))
    domain = Column(String(255))
    attributes = Column(JSON)
    description = Column(JSON)
    hours = Column(JSON)
    task_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    reviews = relationship(
        "ReviewModel",
        back_populates="place",
        cascade="all, delete-orphan"
    )
