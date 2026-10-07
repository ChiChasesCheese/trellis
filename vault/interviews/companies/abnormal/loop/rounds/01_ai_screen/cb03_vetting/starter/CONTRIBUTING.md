# Contributing

* Python 3.11+, standard library only (plus pytest for tests). Type annotations on public functions.
* **Signals** live one per file in `vetting/signals/`, subclass `Signal`, use `@register_signal`,
  and get their weight from `config/default.toml` through `ctx.settings`. Never hard-code a weight.
  Signals read the world through `SignalContext` (observations, lookups, settings, store), never from files.
* **Sources** live one per file in `vetting/sources/`, subclass `Source`, use `@register_source`, and
  import themselves in `sources/__init__.py`. Use `Source.observe()` so missing fields are counted.
  A record we cannot identify or date is a bad record: `Source.bad_record()`, then skip it.
* **Compare normalized values.** Stored values are as-submitted. Phone numbers, emails, names and IPs
  are compared through `vetting/normalize.py`; do not write another normalizer.
* **Times** are timezone-aware UTC. Parse with `timeutil.parse_ts`, store with `timeutil.to_iso`.
* **Config** is validated in `vetting/settings.py`: a new section or key needs a field there and an
  entry in `config/default.toml`. Tenant overrides are single keys.
* **Storage**: schema changes are a new numbered file in `vetting/store/migrations/`; never edit an
  applied one. Every query is tenant-scoped.
* **Errors**: raise the errors in `vetting/errors.py`; the API turns them into its one JSON error shape.
* **Tests**: mirror the module under `tests/`; each signal has a test class in `tests/test_signals.py`
  with one positive and one negative case. Build data through the helpers in `tests/conftest.py`.
* `vetting/legacy/` is deprecated. Do not add to it.
