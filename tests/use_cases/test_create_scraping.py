import pytest
from unittest.mock import Mock
from datetime import datetime
from app.application.scraping.use_cases.create_scraping import create_scraping
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO
from app.domain.scraping.value_objects.status_vo import StatusVO

def test_create_scraping():
    mock_repo = Mock()
    options = ScrapingOptionsVO(
        keywords=["boat rental", "jet ski rental"],
        locations=["Jávea", "Dénia"],
        language="en",
        max_reviews=50
    )

    scraping = create_scraping(options, mock_repo)

    assert scraping.options == options
    assert scraping.status == StatusVO.pending()
    assert scraping.id
    assert isinstance(scraping.created_at, datetime)
    mock_repo.save.assert_called_once_with(scraping)
