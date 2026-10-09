from dataclasses import dataclass, field
from typing import Any

@dataclass
class SourceConfig:
    name: str
    object_count: int          # 100..600
    value_type: type           # bool | int | float
    valid_range: tuple | None = None   # (min, max) для числовых

SOURCES = [
    SourceConfig("source_1", 100, bool),
    SourceConfig("source_2", 250, int, (0, 1000)),
    SourceConfig("source_3", 400, float, (-50.0, 150.0)),
    SourceConfig("source_4", 600, bool),
]

TREND_IDS = [f"trend_{i:02d}" for i in range(1, 21)]   # 20 трендов
WOL_WINDOW = 3600
CYCLE_HZ = 1
DB_PATH = "telemetry.db"
LOG_PATH = "invalid.log"