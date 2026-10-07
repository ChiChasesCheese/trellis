# vetting

Candidate identity vetting for a security team. We read job applications from an applicant
tracking system (ATS) and sign-in events from the identity provider (IdP), run a set of signals
over each applicant, and give a human security reviewer a ranked list with an evidence timeline.
It is a security-facing tool: it never makes or influences a hiring decision.

```
python -m vetting ingest fixtures --tenant acme     # load + review everyone in fixtures/
python -m vetting review greenhouse:40120 --tenant acme
python -m vetting serve                              # HTTP API on :8080, Bearer token per tenant
python -m pytest                                     # tests/, about a second
```

Use `--db PATH` (or `VETTING_DB`) to choose the SQLite file; the default is `var/vetting.db`.

## Architecture

```
 fixtures/greenhouse ─┐
 fixtures/idp ────────┤  sources/      Source subclasses, @register_source
                      ▼
              Identity + Observation ──► store/ (sqlite, migrations, repositories)
                                              │
 lookups/ (phone, ip, email, cached) ──┐      ▼
                                       └──► signals/   Signal subclasses, @register_signal
        blocklist (legacy/) ──────────────►    │          -> Finding(weight, summary, citations)
                                               ▼
                                          scoring.py  -> score -> Recommendation per tenant thresholds
                                               ▼
                                          timeline.py -> api/ (GET /reviews, /reviews/<id>, POST .../disposition)
```

* **Tenants.** Every row carries `tenant_id`; every repository method takes it first. Config is
  `config/default.toml` plus `config/tenants/<tenant>.toml`. Bearer tokens in `fixtures/tokens.json`
  map to tenants.
* **Weights.** Signal weights live in `vetting/weights.py` and are summed by `scoring.py`.
* **Observations** keep values as submitted; `normalize.py` is how values are compared.
* **Metrics.** `vetting/metrics.py` counters are printed after `ingest`.
* The API is a ~150-line WSGI mini framework (`vetting/api/router.py`); there is no web framework.
