# Contributing to Rulelang

- **Everything is tenant-scoped.** Every repository method and every SQL statement that touches
  tenant data takes `tenant_id`. API handlers use `request.tenant` (from the bearer token), never a
  tenant named in the request.
- **Schema changes are migrations.** Add `rulelang/store/migrations/NNNN_description.sql` with the
  next number. Never edit an applied migration. Tables carry `tenant_id` and an index that starts with it.
- **Config over constants.** Thresholds and switches live in `config/default.toml` and are read
  through `Settings`; a tenant overrides them in `config/tenants/<tenant>.toml`. Validate new keys in
  `rulelang/config.py` (unknown sections and keys are errors).
- **New detections are `Detector` subclasses** in `rulelang/detectors/`, registered with
  `@register_detector`, built with `self.signal(...)`. Detectors read intel through `ctx.intel` and the
  communication graph through `ctx.graph`; they never open feed files or run SQL themselves.
- **Errors**: raise a `RulelangError` subclass (`ConfigError` for bad configuration); the CLI prints it
  and exits 2. In the API raise a subclass of `ApiError` (`rulelang/api/framework.py`); handlers never
  build error bodies by hand.
- **Counters**: count anything that is skipped or swallowed with `rulelang.metrics.incr(...)`, and log
  it. Silent drops are bugs.
- **Do not touch `rulelang/legacy/`.** It is frozen.
- **Tests**: every new module gets tests in the matching file: `tests/test_events.py` (loader, config,
  store, pipeline), `tests/test_detectors.py` (detectors, runner), `tests/test_graph.py`,
  `tests/test_api.py` (through `rulelang.api.testing.TestClient`, not by calling handlers directly) or
  `tests/test_cli.py`; add a new `tests/test_<area>.py` for a new area. Keep the suite fast
  (in-memory sqlite, a few seconds for everything).
- Python 3.11+, type annotations on public functions, standard library only.
