CREATE TABLE identities (
    tenant_id    TEXT NOT NULL,
    id           TEXT NOT NULL,
    source       TEXT NOT NULL,
    external_id  TEXT NOT NULL,
    display_name TEXT NOT NULL,
    applied_at   TEXT NOT NULL,
    PRIMARY KEY (tenant_id, id)
);

CREATE TABLE observations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   TEXT NOT NULL,
    identity_id TEXT NOT NULL,
    kind        TEXT NOT NULL,
    value       TEXT NOT NULL,
    source      TEXT NOT NULL,
    ts          TEXT NOT NULL,
    raw_ref     TEXT NOT NULL,
    UNIQUE (tenant_id, identity_id, kind, value, raw_ref)
);
CREATE INDEX idx_observations_kind_value ON observations (tenant_id, kind, value);
CREATE INDEX idx_observations_identity ON observations (tenant_id, identity_id);

CREATE TABLE reviews (
    tenant_id      TEXT NOT NULL,
    identity_id    TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    score          INTEGER NOT NULL,
    findings_json  TEXT NOT NULL,
    evaluated_at   TEXT NOT NULL,
    PRIMARY KEY (tenant_id, identity_id)
);

-- Append-only: every reviewer decision is kept, the latest one is the current disposition.
CREATE TABLE dispositions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   TEXT NOT NULL,
    identity_id TEXT NOT NULL,
    decision    TEXT NOT NULL CHECK (decision IN ('cleared', 'escalated')),
    note        TEXT NOT NULL DEFAULT '',
    decided_at  TEXT NOT NULL
);
CREATE INDEX idx_dispositions_identity ON dispositions (tenant_id, identity_id);
