"""The use cases. The API and the CLI both call this; neither touches storage or SQL directly."""
from __future__ import annotations

import logging
import uuid

from filevault import metrics
from filevault.config import Settings
from filevault.errors import BlobNotFound, FileNotFound, FileTooLarge
from filevault.models import FileRecord
from filevault.storage import BlobStore
from filevault.store import Database, FileRepository, paginate
from filevault.timeutil import Clock
from filevault.validation import clean_content_type, clean_filename

log = logging.getLogger(__name__)


class FileService:
    def __init__(
        self, db: Database, files: FileRepository, store: BlobStore, settings: Settings, clock: Clock
    ):
        self.db = db
        self.files = files
        self.store = store
        self.settings = settings
        self.clock = clock

    def upload(self, owner: str, filename: str, content_type: str, data: bytes) -> FileRecord:
        filename = clean_filename(filename)
        content_type = clean_content_type(content_type)
        if len(data) > self.settings.max_upload_bytes:
            raise FileTooLarge(len(data), self.settings.max_upload_bytes)
        file_id = uuid.uuid4().hex
        record = FileRecord(
            id=file_id,
            owner=owner,
            filename=filename,
            content_type=content_type,
            size=len(data),
            created_at=self.clock(),
            blob_path=file_id,
        )
        self.store.put(record.blob_path, data)
        self.files.add(record)
        metrics.incr("uploads_total")
        log.info("uploaded %s (%d bytes) for %s", record.id, record.size, owner)
        return record

    def get(self, owner: str, file_id: str) -> FileRecord:
        record = self.files.get(file_id, owner)
        if record is None:
            raise FileNotFound(file_id)
        return record

    def read(self, owner: str, file_id: str) -> tuple[FileRecord, bytes]:
        record = self.get(owner, file_id)
        try:
            return record, self.store.get(record.blob_path)
        except BlobNotFound:
            log.error("blob missing for file %s (%s)", record.id, record.blob_path)
            raise

    def list_files(
        self, owner: str, cursor: str | None = None, limit: int | None = None
    ) -> tuple[list[FileRecord], str | None]:
        page = paginate(
            cursor, limit or self.settings.default_page_size, self.settings.max_page_size
        )
        return self.files.list_for_owner(owner, page)

    def delete(self, owner: str, file_id: str) -> None:
        record = self.get(owner, file_id)
        self.files.delete(record.id, owner)
        self.store.delete(record.blob_path)
        metrics.incr("deletes_total")
