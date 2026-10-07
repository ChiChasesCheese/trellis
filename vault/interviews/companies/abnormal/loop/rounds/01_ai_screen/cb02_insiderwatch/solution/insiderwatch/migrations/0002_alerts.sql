CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    signal TEXT NOT NULL,
    score REAL NOT NULL,
    ts TEXT NOT NULL,
    reasons TEXT NOT NULL,
    evidence TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_alerts_user_ts ON alerts (user, ts);
