from sqlalchemy.orm import Session
from app.domain.scraping.entities.scraping import Scraping
from app.domain.scraping.repositories.scraping_repository import ScrapingRepository
from app.infrastructure.persistence.models.scraping_model import ScrapingModel
from app.application.scraping.mappers.scraping_mapper import ScrapingMapper

class SQLAlchemyScrapingRepository(ScrapingRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, scraping: Scraping) -> None:
        model = ScrapingMapper.to_model(scraping)
        self.session.merge(model)
        self.session.commit()

    def find_by_id(self, scraping_id: str) -> Scraping | None:
        model = self.session.query(ScrapingModel).filter_by(id=scraping_id).first()
        if model:
            return ScrapingMapper.to_entity(model)
        return None
