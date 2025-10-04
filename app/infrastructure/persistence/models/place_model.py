from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.infrastructure.persistence.base import Base

class PlaceModel(Base):
    __tablename__ = "places"

    place_id = Column(String, primary_key=True, nullable=False)
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
    attributes = Column(JSON)
    description = Column(JSON)
    hours = Column(JSON)
    reviews = Column(JSON)
    task_id = Column(String(36), nullable=False)  # Foreign key to TaskModel.id