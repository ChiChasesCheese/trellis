-- Content-addressed blobs: one row per unique content, counted by the files that reference it.
-- Files uploaded before this migration keep sha256 NULL and their own private blob.
CREATE TABLE blobs (
    sha256    TEXT PRIMARY KEY,
    blob_path TEXT NOT NULL,
    size      INTEGER NOT NULL,
    ref_count INTEGER NOT NULL CHECK (ref_count >= 0)
);

ALTER TABLE files ADD COLUMN sha256 TEXT;
CREATE INDEX idx_files_sha256 ON files (sha256);
