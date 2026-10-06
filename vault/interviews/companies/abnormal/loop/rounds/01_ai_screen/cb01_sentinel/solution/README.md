# Sentinel

Security event pipeline for multi-tenant customers. Sentinel ingests events from identity,
endpoint and SaaS audit sources, enriches them, runs detection rules, rolls the hits up into
a threat level and a score, raises alerts, and serves them over a small HTTP API.

```
 collectors ──▶ enrichment ──▶ rules ──▶ threat ──▶ alerts ──▶ sqlite
 (auth_log,      (geo, history,   (registry)  (LOW..       (repository)  ▲
  endpoint,       threat intel)                CRITICAL)                 │
  saas_audit)                                                     api/ (WSGI) ◀── analysts
                         legacy/static_rules  (rule DSL v1)
```

## Layout

| Path | What |
|---|---|
| `sentinel/collectors/` | one `Collector` per source, registered with `@register_collector` |
| `sentinel/enrichment/` | enrichers are pluggable: drop a class into this package and it is picked up automatically |
| `sentinel/rules/` | one `Rule` per detection, registered with `@register_rule` |
| `sentinel/scoring.py` | hits -> ThreatLevel; alert score (severity x asset criticality x decay) |
| `sentinel/alerts/` | `Alert`, `AlertService`, `AlertRepository` |
| `sentinel/db/` | sqlite connection, migrations (`db/migrations/NNNN_*.sql`), event repository |
| `sentinel/api/` | stdlib WSGI mini framework; handlers live in `api/routes/` |
| `sentinel/config.py` + `config/` | typed settings; `config/default.toml` plus `config/tenants/<tenant>.toml` |
| `sentinel/legacy/` | v1 rule DSL, still evaluated for tenants that have `static_rules` set |
| `fixtures/` | sample events, intel feeds, asset criticality, API tokens |

## Running it

```bash
python -m sentinel ingest fixtures/events --tenant acme --db /tmp/s.db
python -m sentinel alerts --tenant acme --db /tmp/s.db
python -m sentinel rules
python -m sentinel serve --db /tmp/s.db     # then: curl -H 'Authorization: Bearer tok-acme-analyst' localhost:8080/alerts
python -m sentinel run fixtures/events      # one-shot ingest + print, no database
pytest
```

See `CONTRIBUTING.md` before adding code.
