# Rulelang

Detection engine for multi-tenant email security. Rulelang loads email and account events, runs a
set of detectors over each one, stores the resulting signals, tracks who emails whom, and serves
signals to analysts over a small HTTP API.

```
 events/*.jsonl ──▶ loader ──▶ detectors ──▶ signals ──▶ sqlite ◀── api/ (WSGI) ◀── analysts
 (email, login,     (bad rows   (registry;     (Signal)      ▲
  mailbox rule)      counted)    ctx.signals)                │
                         │                              graph/ (CommGraph: who emailed whom)
                         └──▶ intel (bad hosts, domain age, vendors)
                                     legacy/yaml_rules  (rule format v0)
```

## Layout

| Path | What |
|---|---|
| `rulelang/events/` | JSONL loader; one `Event` per row, bad rows counted and skipped |
| `rulelang/detectors/` | one `Detector` per detection, registered with `@register_detector`; detectors run in dependency order (see `Detector.requires`) |
| `rulelang/graph/` | `CommGraph`: directed per-tenant edges (first / last contact, count), persisted in sqlite |
| `rulelang/intel.py` | `IntelStore`: bad hosts, registered domain age, known vendors |
| `rulelang/store/` | sqlite connection, migrations (`store/migrations/NNNN_*.sql`), repositories |
| `rulelang/api/` | stdlib WSGI mini framework; handlers live in `api/routes/` |
| `rulelang/config.py` + `config/` | typed settings; `config/default.toml` plus `config/tenants/<tenant>.toml` |
| `rulelang/legacy/` | rule format v0, kept for reference |
| `fixtures/` | sample events, intel feeds, API tokens |

## Running it

```bash
python -m rulelang run fixtures/events --tenant acme --db /tmp/r.db
python -m rulelang signals a-010 --tenant acme --db /tmp/r.db
python -m rulelang detectors
python -m rulelang serve --db /tmp/r.db     # then: curl -H 'Authorization: Bearer tok-acme-analyst' 'localhost:8080/signals?event_id=a-010'
pytest
```

See `CONTRIBUTING.md` before adding code.
