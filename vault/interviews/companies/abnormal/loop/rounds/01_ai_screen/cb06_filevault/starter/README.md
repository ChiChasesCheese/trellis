# FileVault

File storage for a multi-user product. Users upload files, list them, download them and delete them
over a small HTTP API; each user sees only their own files. Bytes live behind a blob-store interface,
metadata lives in sqlite.

```
 HTTP (X-User-Id) ──▶ api/ ──▶ service.py ──▶ store/ (sqlite: files)
                                    │
                                    └──────▶ storage/ (BlobStore: local disk | in memory)

 metrics.py   process-wide counters         ratelimit.py   token bucket
 config.py    config/default.toml + FILEVAULT_* env overrides
 legacy/hash_index.py   content hashing, used to deduplicate uploads on disk
```

## Layout

| Path | What |
|---|---|
| `filevault/api/` | stdlib WSGI mini framework (`framework.py`: `@route`, `ApiError`, `Request`, `Response`); handlers in `api/routes/` |
| `filevault/service.py` | `FileService`: upload / get / read / list / delete. The API and the CLI both go through it |
| `filevault/storage/` | `BlobStore` interface; `LocalDiskStore` (`data/blobs/`) and `InMemoryStore` (tests) |
| `filevault/store/` | `Database` (sqlite, migrations, `transaction()`), `FileRepository`, `Where` query builder, keyset `paginate` |
| `filevault/config.py`, `config/default.toml` | typed settings; every key can be overridden with `FILEVAULT_<KEY>` |
| `filevault/metrics.py`, `ratelimit.py` | counters; `TokenBucket` |
| `filevault/validation.py`, `maintenance.py` | input validation; `fsck` (database vs blob store) |
| `fixtures/` | sample uploads used by the tests |

## API

All requests carry `X-User-Id: <user>`. Errors are `{"error": {"code", "message", "details"?}}`.

| Request | Result |
|---|---|
| `POST /files` body `{"filename", "content_type"?, "content_base64"}` | `201` + file metadata |
| `GET /files?cursor=&limit=` | `{"items": [...], "next_cursor": ...}`, newest first |
| `GET /files/<id>` | metadata |
| `GET /health` | liveness (no `X-User-Id` needed) |
| `GET /files/<id>/content` | the bytes, with the stored content type |
| `DELETE /files/<id>` | `204` |

## Running it

```bash
python -m filevault serve --port 8000
python -m filevault upload ./report.pdf --user alice
python -m filevault ls --user alice
python -m filevault fsck
pytest
```

See `CONTRIBUTING.md` before adding code.
