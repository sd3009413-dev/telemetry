import random, time
from config import TREND_IDS
from models import TrendSample

class TrendEngine:
    """Вычисляет 20 трендов из окна WOL или принимает из своего источника."""

    def compute(self, wol_snapshot) -> list[TrendSample]:
        ts = time.time()
        # Пример: если данных нет — генерим.
        return [TrendSample(tid, random.uniform(0, 100), ts) for tid in TREND_IDS]