from app.domain.place.entities.place import Place
from app.infrastructure.persistence.models.place_model import PlaceModel

class PlaceMapper:
    @staticmethod
    def to_entity(model: PlaceModel) -> Place:
        return Place(
            place_id=model.place_id,
            name=model.name,
            address=model.address,
            num_reviews=model.num_reviews,
            rating=model.rating,
            latitude=model.latitude,
            longitude=model.longitude,
            phone=model.phone,
            category=model.category,
            website_url=model.website_url,
            booking_url=model.booking_url,
            main_image=model.main_image,
            domain=model.domain,
            metadata=model.meta_data,
            description=model.description,
            hours=model.hours,
            reviews=model.reviews
        )

    @staticmethod
    def to_model(entity: Place) -> PlaceModel:
        return PlaceModel(
            place_id=entity.place_id,
            name=entity.name,
            address=entity.address,
            num_reviews=entity.num_reviews,
            rating=entity.rating,
            latitude=entity.latitude,
            longitude=entity.longitude,
            phone=entity.phone,
            category=entity.category,
            website_url=entity.website_url,
            booking_url=entity.booking_url,
            main_image=entity.main_image,
            domain=entity.domain,
            meta_data=entity.meta_data,
            description=entity.description,
            hours=entity.hours,
            reviews=entity.reviews
        )
