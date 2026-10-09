from typing import Any
from models import Sample
from config import SourceConfig

class Validator:
    def __init__(self, cfg: SourceConfig):
        self.cfg = cfg

    def is_valid(self, sample: Sample) -> tuple[bool, str]:
        v = sample.value
        # 1. None / отсутствие
        if v is None:
            return False, "value is None"
        # 2. Тип
        if not isinstance(v, self.cfg.value_type):
            # bool — подкласс int, поэтому проверяем строго
            if self.cfg.value_type is bool and isinstance(v, bool):
                pass
            elif self.cfg.value_type is int and isinstance(v, bool):
                return False, "expected int, got bool"
            elif not isinstance(v, self.cfg.value_type):
                return False, f"type mismatch: {type(v).__name__}"
        # 3. Диапазон
        if self.cfg.valid_range is not None:
            lo, hi = self.cfg.valid_range
            if not (lo <= v <= hi):
                return False, f"out of range [{lo},{hi}]: {v}"
        return True, ""