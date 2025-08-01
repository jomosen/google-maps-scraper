import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.infrastructure.persistence.base import Base

from app.infrastructure.persistence.models.scraping_model import ScrapingModel
from app.infrastructure.persistence.models.task_model import TaskModel

@pytest.fixture(scope="function")
def sqlite_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    yield session

    session.close()
    Session.remove()
