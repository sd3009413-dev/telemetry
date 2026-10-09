from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class Sample:
    source: str
    object_id: str
    value: Any
    ts: float          # unix time

@dataclass(slots=True)
class TrendSample:
    trend_id: str
    value: Any
    ts: float