# Quarantine

Quarantine handles the "Report phishing" button. A customer's employee reports a message from
their mail client; Quarantine analyses it, decides whether to pull it out of every mailbox in the
tenant, and tells the reporter what happened. Admins can release a message that was caught by mistake.

```
 POST /reports ──▶ intake ──▶ analyzers ──▶ decision ──▶ actions ──▶ mailbox
 (api/)            (parse,      (sender, link,  (QUARANTINE /  (quarantine,  (provider API;
                    dedupe)      attachment,     RELEASE /      release,      FakeMailbox
                                 display name)   NEEDS_REVIEW)  receipt)       in tests)
                       │                                          │
                       └──────────── sqlite (store/) ◀────────────┘
                 legacy/regex_filter  (pre-filter on subject lines)
```

## Layout

| Path | What |
|---|---|
| `quarantine/intake/` | `parse_report` (payload -> `Report`) and `IntakeService.submit` (dedupe by tenant + message id) |
| `quarantine/analyzers/` | one `Analyzer` per signal, registered with `@register_analyzer`; `AnalyzerRunner` runs them all |
| `quarantine/lookups/` | intel lookups behind small interfaces (`UrlLookup`, `SenderIntel`); fixtures-backed here |
| `quarantine/decision.py` | verdicts -> `Disposition`, thresholds from tenant config |
| `quarantine/actions/` | `Mailbox` interface + `FakeMailbox`, `ActionService` (quarantine / release), reporter receipts |
| `quarantine/store/` | sqlite connection, migrations (`store/migrations/NNNN_*.sql`), repositories |
| `quarantine/api/` | stdlib WSGI mini framework; handlers live in `api/routes/` |
| `quarantine/config.py` + `config/` | typed settings; `config/default.toml` plus `config/tenants/<tenant>.toml` |
| `quarantine/legacy/` | v1 regex filter, runs before the analyzers |
| `fixtures/` | sample reports, intel feeds, API tokens |

## Running it

```bash
python -m quarantine ingest fixtures/reports --tenant acme --db /tmp/q.db
python -m quarantine show <report-id> --tenant acme --db /tmp/q.db
python -m quarantine analyzers
python -m quarantine serve --db /tmp/q.db     # then: curl -H 'Authorization: Bearer tok-acme-analyst' localhost:8080/reports
pytest
```

See `CONTRIBUTING.md` before adding code.
