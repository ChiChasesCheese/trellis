CREATE TABLE events (
    tenant_id TEXT NOT NULL,
    id        TEXT NOT NULL,
    kind      TEXT NOT NULL,
    ts        TEXT NOT NULL,
    actor     TEXT NOT NULL,
    payload   TEXT NOT NULL,
    PRIMARY KEY (tenant_id, id)
);
CREATE INDEX idx_events_actor ON events (tenant_id, kind, actor, ts);

CREATE TABLE signals (
    tenant_id TEXT NOT NULL,
    event_id  TEXT NOT NULL,
    detector  TEXT NOT NULL,
    severity  TEXT NOT NULL,
    summary   TEXT NOT NULL,
    evidence  TEXT NOT NULL,
    PRIMARY KEY (tenant_id, event_id, detector)
);

-- Who emailed whom: one row per directed pair, with the first and the most recent contact.
CREATE TABLE comm_edges (
    tenant_id TEXT NOT NULL,
    src       TEXT NOT NULL,
    dst       TEXT NOT NULL,
    first_ts  TEXT NOT NULL,
    last_ts   TEXT NOT NULL,
    count     INTEGER NOT NULL,
    PRIMARY KEY (tenant_id, src, dst)
);
CREATE INDEX idx_comm_edges_dst ON comm_edges (tenant_id, dst);
