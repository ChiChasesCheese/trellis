"""Consistency checks between the database and the blob store (``python -m filevault fsck``)."""
from __future__ import annotations

from dataclasses import dataclass, field

from filevault.storage import BlobStore
from filevault.store import FileRepository


@dataclass
class FsckReport:
    missing: list[str] = field(default_factory=list)  # referenced by a record, absent from the store
    orphaned: list[str] = field(default_factory=list)  # in the store, referenced by nothing

    @property
    def clean(self) -> bool:
        return not self.missing and not self.orphaned


def fsck(files: FileRepository, store: BlobStore) -> FsckReport:
    referenced = files.all_blob_paths()
    stored = set(store.paths())
    return FsckReport(
        missing=sorted(referenced - stored),
        orphaned=sorted(stored - referenced),
    )
