ALTER TABLE alerts ADD COLUMN event_count INTEGER NOT NULL DEFAULT 1;
ALTER TABLE alerts ADD COLUMN last_seen TEXT;
ALTER TABLE alerts ADD COLUMN dedup_key TEXT NOT NULL DEFAULT '';
UPDATE alerts SET last_seen = created_at;
CREATE INDEX idx_alerts_dedup ON alerts (tenant_id, dedup_key, status, last_seen);
