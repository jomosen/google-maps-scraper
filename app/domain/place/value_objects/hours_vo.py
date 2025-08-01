from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class BusinessHour:
    day: str  # e.g. 'Monday'
    open: str  # e.g. '09:00'
    close: str  # e.g. '17:00'


@dataclass(frozen=True)
class HoursVO:
    hours: List[BusinessHour] = field(default_factory=list)
