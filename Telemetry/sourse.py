import random, time
from config import SOURCES
from models import Sample

class Source:
    """Эмулятор источника. В реальности — сокет/OPC-UA/MQTT клиент."""
    def __init__(self, cfg):
        self.cfg = cfg
        self.objects = [f"{cfg.name}:obj_{i:04d}" for i in range(cfg.object_count)]

    def poll(self) -> list[Sample]:
        ts = time.time()
        out = []
        for oid in self.objects:
            v = self._gen_value()
            out.append(Sample(self.cfg.name, oid, v, ts))
        return out

    def _gen_value(self):
        t = self.cfg.value_type
        # ~2% шума для проверки валидатора
        if random.random() < 0.02:
            return None
        if t is bool:
            return random.random() > 0.5
        if t is int:
            lo, hi = self.cfg.valid_range or (0, 100)
            # иногда выходим за диапазон
            if random.random() < 0.01:
                return hi + 100
            return random.randint(lo, hi)
        if t is float:
            lo, hi = self.cfg.valid_range or (0.0, 1.0)
            if random.random() < 0.01:
                return hi + 999.0
            return random.uniform(lo, hi)