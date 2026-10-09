import time, logging, signal, sys
from config import SOURCES, WOL_WINDOW, CYCLE_HZ, DB_PATH, LOG_PATH, TREND_IDS
from sourse import Source
from validator import Validator
from storege import Storage
from trend_wol import WOL
from trends import TrendEngine
from models import Sample

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("telemetry")

class App:
    def __init__(self):
        self.sources = [Source(c) for c in SOURCES]
        self.validators = {c.name: Validator(c) for c in SOURCES}
        self.storage = Storage(DB_PATH)
        self.trend_wol = WOL(WOL_WINDOW)
        self.sample_wol = WOL(WOL_WINDOW)
        self.trends = TrendEngine()
        self.running = True

    def tick(self):
        all_valid: list[Sample] = []
        ts_start = time.time()

        # 1. Сбор со всех источников
        for src in self.sources:
            batch = src.poll()
            v = self.validators[src.cfg.name]
            for s in batch:
                ok, reason = v.is_valid(s)
                if ok:
                    all_valid.append(s)
                else:
                    log.warning("INVALID src=%s obj=%s val=%r reason=%s",
                                s.source, s.object_id, s.value, reason)

        # 2. Запись валидных в SQLite
        self.storage.save_samples(all_valid)

        # 3. WOL по сэмплам (окно 3600)
        self.sample_wol.extend(all_valid)

        # 4. Тренды → WOL + SQLite
        trend_batch = self.trends.compute(self.sample_wol.snapshot())
        self.trend_wol.extend(trend_batch)
        self.storage.save_trends(trend_batch)

    def run(self):
        period = 1.0 / CYCLE_HZ
        next_t = time.monotonic()
        while self.running:
            next_t += period
            try:
                self.tick()
            except Exception:
                log.exception("tick failed")
            sleep = next_t - time.monotonic()
            if sleep > 0:
                time.sleep(sleep)
            else:
                # отстали — сбрасываем дрейф, чтобы не копить
                next_t = time.monotonic()

    def stop(self):
        self.running = False
        self.storage.close()


def main():
    app = App()

    def _sig(*_):
        app.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)

    app.run()


if __name__ == "__main__":
    main()