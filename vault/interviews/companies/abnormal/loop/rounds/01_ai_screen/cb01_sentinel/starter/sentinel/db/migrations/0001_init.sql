-- Events are keyed per tenant: two tenants may reuse the same source event id.
CREATE TABLE events (
    tenant_id   TEXT NOT NULL,
    id          TEXT NOT NULL,
    ts          TEXT NOT NULL,
    source      TEXT NOT NULL,
    kind        TEXT NOT NULL,
    user        TEXT,
    src_ip      TEXT,
    attrs       TEXT NOT NULL DEFAULT '{}',
    enrichment  TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY (tenant_id, id)
);
CREATE INDEX idx_events_user ON events (tenant_id, user, ts);
CREATE INDEX idx_events_ip ON events (tenant_id, src_ip, ts);

CREATE TABLE alerts (
    id           TEXT PRIMARY KEY,
    tenant_id    TEXT NOT NULL,
    title        TEXT NOT NULL,
    rule_ids     TEXT NOT NULL,
    threat_level INTEGER NOT NULL,
    score        REAL NOT NULL,
    status       TEXT NOT NULL DEFAULT 'OPEN',
    created_at   TEXT NOT NULL,
    event_ids    TEXT NOT NULL
);
CREATE INDEX idx_alerts_tenant ON alerts (tenant_id, status, score DESC);
