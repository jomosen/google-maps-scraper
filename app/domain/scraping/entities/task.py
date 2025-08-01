from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from app.domain.scraping.value_objects.status_vo import StatusVO

@dataclass
class Task:
    id: str
    scraping_id: str
    keyword: str
    location: str
    status: StatusVO = field(default_factory=lambda: StatusVO.pending())
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @classmethod
    def build(cls, scraping_id: str, keyword: str, location: str) -> "Task":
        return cls(
            id=str(uuid.uuid4()),
            scraping_id=scraping_id,
            keyword=keyword,
            location=location,
        )
    
    def is_completed(self) -> bool:
        return self.status == StatusVO.completed()

    def mark_completed(self):
        self.status = StatusVO.completed()
