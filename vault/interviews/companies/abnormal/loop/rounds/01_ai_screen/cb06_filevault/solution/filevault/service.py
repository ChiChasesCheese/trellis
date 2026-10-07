"""The use cases. The API and the CLI both call this; neither touches storage or SQL directly."""
from __future__ import annotations

import hashlib
import logging
import uuid

from filevault import metrics
from filevault.config import Settings
from filevault.errors import BlobNotFound, FileNotFound, FileTooLarge, QuotaExceeded
from filevault.models import FileFilters, FileRecord
from filevault.storage import BlobStore
from filevault.store import BlobRepository, Database, FileRepository, paginate
from filevault.timeutil import Clock
from filevault.validation import clean_content_type, clean_filename

log = logging.getLogger(__name__)


class FileService:
    def __init__(
        self,
        db: Database,
        files: FileRepository,
        blobs: BlobRepository,
        store: BlobStore,
        settings: Settings,
        clock: Clock,
    ):
        self.db = db
        self.files = files
        self.blobs = blobs
        self.store = store
        self.settings = settings
        self.clock = clock

    def upload(self, owner: str, filename: str, content_type: str, data: bytes) -> FileRecord:
        filename = clean_filename(filename)
        content_type = clean_content_type(content_type)
        if len(data) > self.settings.max_upload_bytes:
            raise FileTooLarge(len(data), self.settings.max_upload_bytes)
        sha256 = hashlib.sha256(data).hexdigest()
        record = FileRecord(
            id=uuid.uuid4().hex,
            owner=owner,
            filename=filename,
            content_type=content_type,
            size=len(data),
            created_at=self.clock(),
            blob_path=f"{sha256[:2]}/{sha256}",
            sha256=sha256,
        )
        # One write transaction: the blob row (unique on sha256) decides who stores the bytes, so
        # two uploads of the same content cannot both create it, and a concurrent delete cannot
        # remove a blob this upload is about to reference.
        with self.db.transaction():
            # The quota check shares the write lock with the insert, so concurrent uploads by one
            # user cannot both pass it.
            used, _ = self.files.usage_for_owner(owner)
            if used + record.size > self.settings.quota_bytes_per_user:
                raise QuotaExceeded(used, self.settings.quota_bytes_per_user, record.size)
            created = self.blobs.acquire(sha256, record.blob_path, record.size)
            if created:
                self.store.put(record.blob_path, data)
            self.files.add(record)
        metrics.incr("uploads_total")
        if not created:
            metrics.incr("dedup_hits_total")
            metrics.incr("bytes_saved", record.size)
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
        self,
        owner: str,
        cursor: str | None = None,
        limit: int | None = None,
        filters: FileFilters | None = None,
    ) -> tuple[list[FileRecord], str | None]:
        page = paginate(
            cursor, limit or self.settings.default_page_size, self.settings.max_page_size
        )
        return self.files.list_for_owner(owner, page, filters)

    def delete(self, owner: str, file_id: str) -> None:
        record = self.get(owner, file_id)
        with self.db.transaction():
            if not self.files.delete(record.id, owner):
                raise FileNotFound(file_id)  # lost a race with another delete
            # Legacy rows (no sha256) own their blob; the rest drop one reference.
            orphan = record.blob_path if record.sha256 is None else self.blobs.release(record.sha256)
            if orphan is not None:
                self.store.delete(orphan)
        metrics.incr("deletes_total")

    def usage(self, owner: str) -> dict[str, int]:
        used, count = self.files.usage_for_owner(owner)
        quota = self.settings.quota_bytes_per_user
        return {
            "used_bytes": used,
            "quota_bytes": quota,
            "remaining_bytes": max(0, quota - used),
            "file_count": count,
        }

    def storage_stats(self) -> dict[str, int | float]:
        """What users think they store versus what is on disk, across all users."""
        logical, private, count = self.files.totals()
        physical = self.blobs.total_size() + private
        return {
            "logical_bytes": logical,
            "physical_bytes": physical,
            "saved_bytes": logical - physical,
            "savings_ratio": round((logical - physical) / logical, 4) if logical else 0.0,
            "file_count": count,
        }
