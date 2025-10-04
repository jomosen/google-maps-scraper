import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
from app.domain.scraping.entities.task import Task
from app.domain.scraping.value_objects.status_vo import StatusVO
from app.domain.scraping.value_objects.scraping_options_vo import ScrapingOptionsVO

@dataclass
class Scraping:
    id: str
    options: ScrapingOptionsVO
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    status: StatusVO = field(default_factory=lambda: StatusVO.pending())
    tasks: List[Task] = field(default_factory=list)

    @classmethod
    def create(cls, options: ScrapingOptionsVO) -> "Scraping":
        return cls(
            id=str(uuid.uuid4()),
            options=options,
            created_at=datetime.utcnow(),
            status=StatusVO.pending()
        )

    def is_completed(self) -> bool:
        return self.status == StatusVO.completed()

    def mark_completed(self):
        self.status = StatusVO.completed()
        self.completed_at = datetime.utcnow()
