import sqlite3
from contextlib import closing
from typing import Iterable
from models import Sample, TrendSample

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    source TEXT NOT NULL,
    object_id TEXT NOT NULL,
    value REAL
);
CREATE INDEX IF NOT EXISTS idx_samples_ts ON samples(ts);
CREATE INDEX IF NOT EXISTS idx_samples_obj ON samples(object_id, ts);

CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    trend_id TEXT NOT NULL,
    value REAL
);
CREATE INDEX IF NOT EXISTS idx_trends ON trends(trend_id, ts);
"""

class Storage:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def save_samples(self, samples: Iterable[Sample]):
        rows = [(s.ts, s.source, s.object_id, float(s.value) if s.value is not None else None)
                for s in samples]
        if not rows:
            return
        with self.conn:
            self.conn.executemany(
                "INSERT INTO samples(ts, source, object_id, value) VALUES (?,?,?,?)", rows)

    def save_trends(self, trends: Iterable[TrendSample]):
        rows = [(t.ts, t.trend_id, float(t.value) if t.value is not None else None)
                for t in trends]
        if not rows:
            return
        with self.conn:
            self.conn.executemany(
                "INSERT INTO trends(ts, trend_id, value) VALUES (?,?,?)", rows)

    def close(self):
        self.conn.close()