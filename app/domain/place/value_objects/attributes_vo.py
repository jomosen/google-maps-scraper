from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(frozen=True)
class AttributesVO:
    attributes: Dict[str, str] = field(default_factory=dict)