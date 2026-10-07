"""All SQL for the ``files`` table lives here."""
from __future__ import annotations

import sqlite3

from filevault.models import FileRecord
from filevault.store.db import Database
from filevault.store.pagination import Page, encode_cursor
from filevault.store.query import Where
from filevault.timeutil import parse_iso, to_iso

_COLUMNS = "id, owner, filename, content_type, size, created_at, blob_path"


def _record(row: sqlite3.Row) -> FileRecord:
    return FileRecord(
        id=row["id"],
        owner=row["owner"],
        filename=row["filename"],
        content_type=row["content_type"],
        size=row["size"],
        created_at=parse_iso(row["created_at"]),
        blob_path=row["blob_path"],
    )


class FileRepository:
    """Every method takes the owner: a user can only ever reach their own rows."""

    def __init__(self, db: Database):
        self._db = db

    def add(self, record: FileRecord) -> None:
        self._db.conn.execute(
            f"INSERT INTO files ({_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                record.id,
                record.owner,
                record.filename,
                record.content_type,
                record.size,
                to_iso(record.created_at),
                record.blob_path,
            ),
        )

    def get(self, file_id: str, owner: str) -> FileRecord | None:
        where, params = Where().eq("id", file_id).eq("owner", owner).build()
        row = self._db.conn.execute(f"SELECT {_COLUMNS} FROM files {where}", params).fetchone()
        return _record(row) if row else None

    def list_for_owner(self, owner: str, page: Page) -> tuple[list[FileRecord], str | None]:
        """Newest first. Returns the page and the cursor for the next one (``None`` at the end)."""
        where = Where().eq("owner", owner)
        if page.after is not None:
            where.row_compare(("created_at", "id"), "<", page.after)
        sql, params = where.build()
        rows = self._db.conn.execute(
            f"SELECT {_COLUMNS} FROM files {sql} ORDER BY created_at DESC, id DESC LIMIT ?",
            (*params, page.limit + 1),
        ).fetchall()
        records = [_record(r) for r in rows[: page.limit]]
        more = len(rows) > page.limit
        return records, encode_cursor(to_iso(records[-1].created_at), records[-1].id) if more else None

    def all_blob_paths(self) -> set[str]:
        """Every blob path some record points at (used by ``fsck``)."""
        rows = self._db.conn.execute("SELECT DISTINCT blob_path FROM files")
        return {row["blob_path"] for row in rows}

    def delete(self, file_id: str, owner: str) -> bool:
        where, params = Where().eq("id", file_id).eq("owner", owner).build()
        cursor = self._db.conn.execute(f"DELETE FROM files {where}", params)
        return cursor.rowcount > 0
