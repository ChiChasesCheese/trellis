"""A tiny SQS-style queue on top of sqlite.

Semantics follow SQS standard queues: at-least-once delivery, a received message is hidden for
`visibility_timeout` seconds, and must be deleted by the consumer or it becomes visible again.
"""
from __future__ import annotations

import sqlite3
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Message:
    id: int
    body: str
    receipt: str
    receive_count: int


class Queue:
    def __init__(self, path: str = ":memory:", clock: Callable[[], float] = time.time):
        self._clock = clock
        self._lock = threading.RLock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " body TEXT NOT NULL,"
            " visible_at REAL NOT NULL,"
            " receive_count INTEGER NOT NULL DEFAULT 0,"
            " receipt TEXT)"
        )
        self._db.commit()

    def send(self, body: str, delay: float = 0.0) -> int:
        with self._lock:
            cur = self._db.execute(
                "INSERT INTO messages (body, visible_at) VALUES (?, ?)", (body, self._clock() + delay)
            )
            self._db.commit()
            return int(cur.lastrowid)

    def receive(self, max_messages: int = 10, visibility_timeout: float = 30.0) -> list[Message]:
        """Return up to `max_messages` visible messages and hide them for `visibility_timeout` seconds."""
        with self._lock:
            now = self._clock()
            rows = self._db.execute(
                "SELECT id, body, receive_count FROM messages WHERE visible_at <= ? ORDER BY id LIMIT ?",
                (now, max_messages),
            ).fetchall()
            out = []
            for mid, body, count in rows:
                receipt = uuid.uuid4().hex  # one receipt per delivery, as in SQS
                self._db.execute(
                    "UPDATE messages SET visible_at = ?, receive_count = ?, receipt = ? WHERE id = ?",
                    (now + visibility_timeout, count + 1, receipt, mid),
                )
                out.append(Message(id=mid, body=body, receipt=receipt, receive_count=count + 1))
            self._db.commit()
            return out

    def delete(self, receipt: str) -> bool:
        with self._lock:
            cur = self._db.execute("DELETE FROM messages WHERE receipt = ?", (receipt,))
            self._db.commit()
            return cur.rowcount == 1

    def change_visibility(self, receipt: str, timeout: float) -> bool:
        with self._lock:
            cur = self._db.execute(
                "UPDATE messages SET visible_at = ? WHERE receipt = ?", (self._clock() + timeout, receipt)
            )
            self._db.commit()
            return cur.rowcount == 1

    def stats(self) -> dict[str, int]:
        with self._lock:
            now = self._clock()
            total = self._db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
            visible = self._db.execute(
                "SELECT COUNT(*) FROM messages WHERE visible_at <= ?", (now,)
            ).fetchone()[0]
            return {"total": total, "visible": visible, "in_flight": total - visible}

    def bodies(self) -> list[str]:
        with self._lock:
            return [r[0] for r in self._db.execute("SELECT body FROM messages ORDER BY id")]
