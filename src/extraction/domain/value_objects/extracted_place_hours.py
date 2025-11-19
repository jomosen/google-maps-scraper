from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class PlaceHour:
    day: str  # e.g. 'Monday'
    open: str  # e.g. '09:00'
    close: str  # e.g. '17:00'


@dataclass(frozen=True)
class PlaceHours:
    hours: List[PlaceHour] = field(default_factory=list)
