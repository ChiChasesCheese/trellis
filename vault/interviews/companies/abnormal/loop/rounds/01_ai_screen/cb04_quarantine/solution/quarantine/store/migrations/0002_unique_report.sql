-- One report per (tenant, message): concurrent reports of the same message must collide here.
CREATE UNIQUE INDEX uq_reports_tenant_message ON reports (tenant_id, message_id);
DROP INDEX idx_reports_tenant_message;
