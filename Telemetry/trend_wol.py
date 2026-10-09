from collections import deque
from threading import Lock
from typing import Iterable

class WOL:
    """Write-Once Log с фиксированным окном видимости.
    Хранит последние N элементов. Потокобезопасен."""

    def __init__(self, window: int = 3600):
        self._window = window
        self._buf: deque = deque(maxlen=window)
        self._lock = Lock()

    def append(self, item):
        with self._lock:
            self._buf.append(item)

    def extend(self, items: Iterable):
        with self._lock:
            self._buf.extend(items)

    def snapshot(self) -> list:
        """Снимок окна (копия, безопасно отдавать наружу)."""
        with self._lock:
            return list(self._buf)

    def __len__(self):
        return len(self._buf)

    @property
    def window(self) -> int:
        return self._window