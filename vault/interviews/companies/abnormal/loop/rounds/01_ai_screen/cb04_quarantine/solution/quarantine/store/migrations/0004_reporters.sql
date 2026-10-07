-- Everyone who reported a message, one row per person. reports.reporter stays the first reporter.
CREATE TABLE report_reporters (
    tenant_id   TEXT NOT NULL,
    report_id   TEXT NOT NULL REFERENCES reports (id),
    reporter    TEXT NOT NULL,
    reported_at TEXT NOT NULL,
    PRIMARY KEY (tenant_id, report_id, reporter)
);

INSERT INTO report_reporters (tenant_id, report_id, reporter, reported_at)
SELECT tenant_id, id, reporter, received_at FROM reports;
