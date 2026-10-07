CREATE TABLE suppressions (
    id         TEXT PRIMARY KEY,
    tenant_id  TEXT NOT NULL,
    rule_id    TEXT NOT NULL,
    match      TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
CREATE INDEX idx_suppressions_tenant ON suppressions (tenant_id, rule_id);

-- Audit trail: one row per rule hit that a suppression swallowed.
CREATE TABLE suppressed_hits (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id      TEXT NOT NULL,
    suppression_id TEXT NOT NULL,
    rule_id        TEXT NOT NULL,
    event_id       TEXT NOT NULL,
    suppressed_at  TEXT NOT NULL
);
CREATE INDEX idx_suppressed_hits ON suppressed_hits (tenant_id, suppression_id);
