import pytest
from app.application.scraping.use_cases.create_scraping import create_scraping
from app.application.scraping.use_cases.run_scraper import run_scraper
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO
from app.infrastructure.persistence.repositories.sqlalchemy_scraping_repository import SQLAlchemyScrapingRepository
from app.domain.scraping.entities.task import Task
from app.application.scraping.services.task_generator import TaskGenerator

@pytest.fixture
def repository_instance(sqlite_session):
    return SQLAlchemyScrapingRepository(sqlite_session)

@pytest.fixture
def scraper_instance(repository_instance):
    options = ScrapingOptionsVO(
        keywords=["tours"],
        locations=["Jávea"],
        language="en",
        max_reviews=10
    )

    scraping = create_scraping(options, repository_instance)
    return scraping

def test_scraping_is_saved_and_retrieved(scraper_instance):
    assert scraper_instance is not None
    assert scraper_instance.id == scraper_instance.id
    assert scraper_instance.options.language == "en"
    assert scraper_instance.options.max_reviews == 10

def test_run_scraping_generates_and_completes_tasks(scraper_instance, repository_instance):
    task1 = Task.build(scraping_id=scraper_instance.id, keyword="boat rental", location="javea")
    task2 = Task.build(scraping_id=scraper_instance.id, keyword="jet ski rental", location="javea")

    scraper_instance.tasks = [task1, task2]

    repository_instance.save(scraper_instance)

    task_generator = TaskGenerator()

    result = run_scraper(scraper_instance.id, repository_instance, task_generator)

    assert result.is_completed()
    assert all(task.is_completed() for task in result.tasks)
    assert len(result.tasks) == 2
    assert result.tasks != [task1, task2]
