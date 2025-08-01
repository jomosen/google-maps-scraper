from dataclasses import dataclass

@dataclass(frozen=True)
class StatusVO:
    value: str

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

    VALID_STATUSES = {PENDING, IN_PROGRESS, COMPLETED, FAILED}

    def __post_init__(self):
        if self.value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid scraping status: '{self.value}'. Must be one of {self.VALID_STATUSES}")
        
    @classmethod
    def pending(cls) -> "StatusVO":
        return cls(cls.PENDING)

    @classmethod
    def in_progress(cls) -> "StatusVO":
        return cls(cls.IN_PROGRESS)

    @classmethod
    def completed(cls) -> "StatusVO":
        return cls(cls.COMPLETED)

    @classmethod
    def failed(cls) -> "StatusVO":
        return cls(cls.FAILED)
