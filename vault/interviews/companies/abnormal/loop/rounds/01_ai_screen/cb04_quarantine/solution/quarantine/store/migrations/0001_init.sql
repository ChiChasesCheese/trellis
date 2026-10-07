CREATE TABLE reports (
    id           TEXT PRIMARY KEY,
    tenant_id    TEXT NOT NULL,
    message_id   TEXT NOT NULL,
    reporter     TEXT NOT NULL,
    sender       TEXT NOT NULL,
    display_name TEXT NOT NULL DEFAULT '',
    subject      TEXT NOT NULL DEFAULT '',
    sent_at      TEXT NOT NULL,
    received_at  TEXT NOT NULL,
    links        TEXT NOT NULL DEFAULT '[]',
    attachments  TEXT NOT NULL DEFAULT '[]',
    verdicts     TEXT NOT NULL DEFAULT '[]',
    disposition  TEXT,
    status       TEXT
);

CREATE INDEX idx_reports_tenant_message ON reports (tenant_id, message_id);
CREATE INDEX idx_reports_tenant_sender  ON reports (tenant_id, sender, sent_at);
CREATE INDEX idx_reports_tenant_received ON reports (tenant_id, received_at);

CREATE TABLE action_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id  TEXT NOT NULL,
    report_id  TEXT NOT NULL REFERENCES reports (id),
    action     TEXT NOT NULL,
    detail     TEXT NOT NULL DEFAULT '',
    at         TEXT NOT NULL
);

CREATE INDEX idx_action_log_tenant_report ON action_log (tenant_id, report_id);
