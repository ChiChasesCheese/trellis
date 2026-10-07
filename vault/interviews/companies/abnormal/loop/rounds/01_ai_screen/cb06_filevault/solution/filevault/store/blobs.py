"""Reference counting for content-addressed blobs. Call inside ``Database.transaction()``."""
from __future__ import annotations

from filevault.store.db import Database


class BlobRepository:
    def __init__(self, db: Database):
        self._db = db

    def acquire(self, sha256: str, blob_path: str, size: int) -> bool:
        """Add one reference. Returns True when this created the blob (the caller stores the bytes)."""
        row = self._db.conn.execute(
            "INSERT INTO blobs (sha256, blob_path, size, ref_count) VALUES (?, ?, ?, 1) "
            "ON CONFLICT (sha256) DO UPDATE SET ref_count = ref_count + 1 RETURNING ref_count",
            (sha256, blob_path, size),
        ).fetchone()
        return row["ref_count"] == 1

    def total_size(self) -> int:
        """Bytes physically held in shared blobs."""
        return self._db.conn.execute("SELECT COALESCE(SUM(size), 0) FROM blobs").fetchone()[0]

    def release(self, sha256: str) -> str | None:
        """Drop one reference. Returns the blob path once nothing references it any more."""
        row = self._db.conn.execute(
            "UPDATE blobs SET ref_count = ref_count - 1 WHERE sha256 = ? "
            "RETURNING ref_count, blob_path",
            (sha256,),
        ).fetchone()
        if row is None or row["ref_count"] > 0:
            return None
        self._db.conn.execute("DELETE FROM blobs WHERE sha256 = ?", (sha256,))
        return row["blob_path"]
