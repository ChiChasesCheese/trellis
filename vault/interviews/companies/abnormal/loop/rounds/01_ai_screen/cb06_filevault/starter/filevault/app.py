"""Composition root: wire settings, database, blob store, service and the WSGI app together."""
from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from filevault.api.app import ApiApp
from filevault.api.framework import ApiContext
from filevault.config import Settings, load_settings
from filevault.service import FileService
from filevault.storage import BlobStore, LocalDiskStore
from filevault.store import Database, FileRepository
from filevault.timeutil import Clock, utcnow


@dataclass
class App:
    settings: Settings
    db: Database
    store: BlobStore
    service: FileService
    wsgi: ApiApp

    def close(self) -> None:
        self.db.close()


def create_app(
    data_dir: Path | str | None = None,
    *,
    settings: Settings | None = None,
    store: BlobStore | None = None,
    clock: Clock = utcnow,
    env: Mapping[str, str] | None = None,
) -> App:
    """Build an app rooted at ``data_dir`` (``data/`` by default).

    ``env`` defaults to ``os.environ``; ``store`` defaults to ``<data_dir>/blobs`` on local disk.
    """
    settings = settings or load_settings(os.environ if env is None else env)
    root = Path(data_dir or settings.data_dir)
    root.mkdir(parents=True, exist_ok=True)
    db = Database(root / "filevault.db")
    db.migrate()
    store = store or LocalDiskStore(root / "blobs")
    service = FileService(db, FileRepository(db), store, settings, clock)
    wsgi = ApiApp(ApiContext(service=service, settings=settings))
    return App(settings, db, store, service, wsgi)
