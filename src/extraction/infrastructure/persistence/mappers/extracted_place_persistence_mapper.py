from extraction.infrastructure.persistence.mappers.extracted_place_review_persistence_mapper import ExtractedPlaceReviewPersistenceMapper
from extraction.infrastructure.persistence.models.extracted_place_model import ExtractedPlaceModel
from extraction.domain.extracted_place import ExtractedPlace


class ExtractionPlacePersistenceMapper:
    """Maps Place domain entities to and from persistence models."""

    @staticmethod
    def to_entity(model: ExtractedPlaceModel) -> ExtractedPlace:
        """Converts a ExtractionPlaceModel to a Place entity."""

        reviews = []
        if hasattr(model, "reviews") and model.reviews is not None:
            reviews = [ExtractedPlaceReviewPersistenceMapper.to_entity(r) for r in model.reviews]

        return ExtractedPlace(
            place_id=model.place_id,
            name=model.name,
            address=model.address,
            num_reviews=model.num_reviews,
            rating=model.rating,
            latitude=model.latitude,
            longitude=model.longitude,
            phone=model.phone,
            plus_code=model.plus_code,
            category=model.category,
            website_url=model.website_url,
            booking_url=model.booking_url,
            main_image=model.main_image,
            domain=model.domain,
            attributes=model.attributes,
            description=model.description,
            hours=model.hours,
            reviews=reviews,
            task_id=model.task_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: ExtractedPlace) -> ExtractedPlaceModel:
        """Converts a Place entity to a PlaceModel."""

        model = ExtractedPlaceModel(
            place_id=entity.place_id,
            name=entity.name,
            address=entity.address,
            num_reviews=entity.num_reviews,
            rating=entity.rating,
            latitude=entity.latitude,
            longitude=entity.longitude,
            phone=entity.phone,
            plus_code=entity.plus_code,
            category=entity.category,
            website_url=entity.website_url,
            booking_url=entity.booking_url,
            main_image=entity.main_image,
            domain=entity.domain,
            attributes=entity.attributes,
            description=entity.description,
            hours=entity.hours,
            task_id=entity.task_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

        if entity.reviews:
            model.reviews = [ExtractedPlaceReviewPersistenceMapper.to_model(r) for r in entity.reviews]

        return model
