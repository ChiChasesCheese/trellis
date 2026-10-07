-- Receipts to reporters are queued here and delivered by `python -m quarantine drain-outbox`.
CREATE TABLE outbox (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id   TEXT NOT NULL,
    report_id   TEXT NOT NULL REFERENCES reports (id),
    recipient   TEXT NOT NULL,
    disposition TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'PENDING',
    attempts    INTEGER NOT NULL DEFAULT 0,
    last_error  TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL,
    sent_at     TEXT
);

CREATE INDEX idx_outbox_tenant_status ON outbox (tenant_id, status, id);
