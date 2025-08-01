from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.infrastructure.persistence.base import Base

class PlaceModel(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    place_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    address = Column(String)
    num_reviews = Column(Integer)
    rating = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String)
    category = Column(String)
    website_url = Column(String)
    booking_url = Column(String)
    main_image = Column(String)
    domain = Column(String)
    meta_data = Column(JSON)
    description = Column(JSON)
    hours = Column(JSON)
    reviews = Column(JSON)