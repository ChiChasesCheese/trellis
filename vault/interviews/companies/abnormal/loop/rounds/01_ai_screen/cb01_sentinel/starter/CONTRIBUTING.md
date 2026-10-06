# Contributing to Sentinel

- **Everything is tenant-scoped.** Every repository method and every SQL statement that touches
  tenant data takes `tenant_id`. API handlers use `request.tenant` (from the bearer token), never a
  tenant named in the request body.
- **Schema changes are migrations.** Add `sentinel/db/migrations/NNNN_description.sql` with the next
  number. Never edit an applied migration. Tables carry `tenant_id` and an index that starts with it.
- **Config over constants.** Thresholds and switches live in `config/default.toml` and are read through
  `Settings`; a tenant overrides them in `config/tenants/<tenant>.toml`. Validate new keys in
  `sentinel/config/loader.py` (unknown keys are errors).
- **New detections are `Rule` subclasses** in `sentinel/rules/`, registered with `@register_rule`.
  Rules read enrichment through `self.enrichment(event, "<name>")` and never query intel files directly.
- **New enrichment data is an `Enricher`** (`sentinel/enrichment/base.py`); results are plain dicts.
- **Errors**: raise `ConfigError` for bad configuration. In the API raise a subclass of `ApiError`
  (`sentinel/api/errors.py`); handlers never build error bodies by hand.
- **Counters**: count anything that is skipped or swallowed with `sentinel.metrics.incr(...)`, and log
  it. Silent drops are bugs.
- **Do not touch `sentinel/legacy/`.** It is frozen.
- **Tests**: every new module gets a test under the matching `tests/<area>/` directory. API behaviour is
  tested through `sentinel.api.testing.TestClient`, not by calling handlers directly. Keep the suite fast
  (the whole thing runs in a few seconds, in-memory sqlite).
- Python 3.11+, type annotations on public functions, standard library only.
