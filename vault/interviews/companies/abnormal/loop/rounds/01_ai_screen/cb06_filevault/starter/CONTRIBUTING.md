# Contributing to FileVault

- **Everything is per user.** Repository methods take the owner and put it in the `WHERE`; handlers use
  `request.user` (from `X-User-Id`), never a user named in the body. Another user's file is a 404, not a 403.
- **Bytes go through `BlobStore`.** Never call `open()`/`pathlib` on blob paths outside `filevault/storage/`.
- **SQL lives in repositories** under `filevault/store/`. Build conditions with `Where` (bound parameters);
  never format user input into a SQL string. Paging uses `paginate()` and keyset cursors, not `OFFSET`.
- **Writes that must be atomic together use `Database.transaction()`.** Do not paper over races with
  Python locks: the service runs with several threads and, in production, several processes.
- **Schema changes are migrations**: `filevault/store/migrations/NNNN_description.sql`, next number, never edit
  an applied one.
- **Config over constants.** New knobs go in `config/default.toml`, are typed and validated in
  `filevault/config.py`, and are overridable as `FILEVAULT_<KEY>`.
- **Errors**: the service raises domain errors from `filevault/errors.py`; `api/app.py:translate` maps them to
  HTTP. Handlers raise `ApiError` subclasses (`api/framework.py`) and never build error bodies by hand.
- **Counters**: count what matters (`metrics.incr(...)`); skipped or swallowed things must be counted and logged.
- **Do not touch `filevault/legacy/`.** It is frozen.
- **Tests** sit next to the area they cover (`tests/test_api.py`, `test_store.py`, `test_service.py`, ...);
  API behaviour is tested through `filevault.api.testing.TestClient`. Keep the suite fast (a few seconds).
- Python 3.11+, type annotations on public functions, standard library only.
