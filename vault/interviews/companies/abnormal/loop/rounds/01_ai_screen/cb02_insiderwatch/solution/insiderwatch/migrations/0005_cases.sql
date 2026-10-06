CREATE TABLE cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    score REAL NOT NULL,
    opened_at TEXT NOT NULL,
    last_alert_at TEXT NOT NULL,
    closed_at TEXT
);
CREATE INDEX idx_cases_user_status ON cases (user, status);
CREATE TABLE case_alerts (
    alert_id INTEGER PRIMARY KEY REFERENCES alerts (id),
    case_id INTEGER NOT NULL REFERENCES cases (id)
);
CREATE INDEX idx_case_alerts_case ON case_alerts (case_id);
