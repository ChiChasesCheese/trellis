CREATE TABLE files (
    id           TEXT PRIMARY KEY,
    owner        TEXT NOT NULL,
    filename     TEXT NOT NULL,
    content_type TEXT NOT NULL,
    size         INTEGER NOT NULL CHECK (size >= 0),
    created_at   TEXT NOT NULL,
    blob_path    TEXT NOT NULL
);

CREATE INDEX idx_files_owner_created ON files (owner, created_at, id);
