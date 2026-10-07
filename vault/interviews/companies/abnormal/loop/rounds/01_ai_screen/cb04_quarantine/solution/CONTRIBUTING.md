# Contributing to Quarantine

- **Everything is tenant-scoped.** Every repository method and every SQL statement that touches
  tenant data takes `tenant_id`. API handlers use `request.tenant` (from the bearer token), never a
  tenant named in the request body.
- **Schema changes are migrations.** Add `quarantine/store/migrations/NNNN_description.sql` with the next
  number. Never edit an applied migration. Tables carry `tenant_id` and an index that starts with it.
- **Config over constants.** Thresholds and switches live in `config/default.toml` and are read through
  `Settings`; a tenant overrides them in `config/tenants/<tenant>.toml`. Validate new keys in
  `quarantine/config.py` (unknown keys are errors).
- **New signals are `Analyzer` subclasses** in `quarantine/analyzers/`, registered with
  `@register_analyzer`. Analyzers get lookups through `AnalysisContext`; they never read intel files.
- **Every state change leaves a trail.** Anything that acts on a mailbox goes through `ActionService`,
  which writes a row to `action_log` (`ActionLogRepository`). Do not call the `Mailbox` directly.
- **Errors**: services raise subclasses of `QuarantineError` (`quarantine/errors.py`). In the API raise a
  subclass of `ApiError` (`quarantine/api/framework.py`); handlers never build error bodies by hand.
- **Counters**: count anything that is skipped or swallowed with `quarantine.metrics.incr(...)`, and log
  it. Silent drops are bugs.
- **Time**: datetimes are timezone-aware and compared in UTC; use `quarantine/timeutil.py`.
- **Do not touch `quarantine/legacy/`.** It is frozen.
- **Tests**: every new module gets tests in the matching file: `tests/test_intake.py` (parsing, intake),
  `tests/test_analyzers.py` (analyzers, decision), `tests/test_actions.py` (mailbox, actions),
  `tests/test_store.py` (db, repositories), `tests/test_api.py`, `tests/test_cli.py`; add a new
  `tests/test_<area>.py` for a new area. API behaviour is tested through
  `quarantine.api.testing.TestClient`, not by calling handlers directly. Keep the suite fast
  (the whole thing runs in a few seconds, in-memory sqlite).
- Python 3.11+, type annotations on public functions, standard library only.
