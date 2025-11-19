from sqlalchemy import Column, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.persistence.db.base import Base
from datetime import datetime
import uuid

class ReviewModel(Base):
    __tablename__ = "reviews"

    # Identificador único de la review (UUID generado si no viene del scraping)
    id = Column(String(128), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Relación con la tabla places
    place_id = Column(String(191), ForeignKey("places.place_id"), nullable=False)

    # Campos de la review
    rating = Column(Float, nullable=True)
    author = Column(String(255), nullable=True)
    text = Column(Text, nullable=True)
    lang = Column(String(10), nullable=True)
    photos = Column(JSON, nullable=True)

    # Timestamp de creación en el scraper
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa con PlaceModel
    place = relationship("PlaceModel", back_populates="reviews")

    def __repr__(self):
        return (
            f"<Review(id='{self.id}', author='{self.author}', "
            f"rating={self.rating}, lang='{self.lang}')>"
        )
