# Contributing

* Python 3.11+, standard library only (plus pytest for tests). Type-annotate public functions.
* **Schema changes** are new numbered files in `insiderwatch/migrations/`. Never edit an applied
  migration. Stores take an open `sqlite3.Connection`; they never open files themselves.
* **Sources** are `Connector` subclasses registered with `@register_connector` and imported in
  `connectors/__init__.py`. Count what you drop with `self.drop("<reason>")`; never swallow records silently.
* **Detection** is `Signal` subclasses registered with `@signal("name")` and imported in
  `signals/__init__.py`. A signal returns findings with a 0..1 `strength`; it never decides whether
  to alert. Weights and thresholds belong in `config.py`, not in the signal.
* **Time**: events are UTC-aware. Parse vendor timestamps with `timeutil.parse_ts`; never compare
  naive datetimes. Business hours are evaluated in the employee's own timezone.
* **Users** are lower-cased email addresses. Use `events.normalize_user` / `events.is_external`.
* Log with `logging.getLogger(__name__)`; no `print` outside `cli.py` and notifiers.
* `legacy/` is frozen. Do not extend it or import from it (INSIDER-212).
* Tests mirror the package (`tests/test_<area>.py`). Every new signal, connector and CLI command
  needs a test. Tests must stay fast (the whole suite runs in a few seconds) and may not touch the network.
* Feature flags live in `Config.feature_flags`; read them with `config.flag("name")`.
