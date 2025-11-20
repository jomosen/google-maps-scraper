from extraction.domain.extracted_place_review import ExtractedPlaceReview
from extraction.infrastructure.persistence.models.extracted_place_review_model import ExtractedPlaceReviewModel


class ExtractedPlaceReviewPersistenceMapper:
    """Maps Review domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: ExtractedPlaceReviewModel) -> ExtractedPlaceReview:
        """Converts a ReviewModel to a Review entity."""

        return ExtractedPlaceReview(
            id=model.id,
            place_id=model.place_id,
            rating=model.rating,
            author=model.author,
            text=model.text,
            lang=model.lang,
            photos=model.photos,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: ExtractedPlaceReview) -> ExtractedPlaceReviewModel:
        """Converts a Review entity to a ReviewModel."""

        return ExtractedPlaceReviewModel(
            id=entity.id,
            place_id=entity.place_id,
            rating=entity.rating,
            author=entity.author,
            text=entity.text,
            lang=entity.lang,
            photos=entity.photos,
            created_at=entity.created_at
        )
