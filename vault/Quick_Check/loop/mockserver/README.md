# loop/mockserver

Two zero-dependency (stdlib-only) local HTTP servers backing the Integration round
problems (`int01` BikeMap, `int02` payments reconciliation). Both use
`http.server.ThreadingHTTPServer`; PNGs are encoded by hand in `_png.py` (no PIL).

Start one with `python3 loop/mock.py serve <int-id>` (reads `<!-- mockserver: NAME -->`
from the problem's `problem.md`), or run/import a module directly — see below.

## `maps.py` — GeoJSON points → PNG (backs int01 BikeMap)

Run: `python3 -m loop.mockserver.maps --port 0` (0 = OS-assigned port; the server prints
`listening on http://127.0.0.1:<port>`, flushed, then blocks until Ctrl-C/SIGTERM).
Import: `from loop.mockserver.maps import serve, start_in_thread` — both return
`(server, thread)`, server already running in a daemon thread.

| Method & path | Behavior |
|---|---|
| `GET /health` | `200 {"ok": true}` |
| `POST /render` | body `{"points": [[lat,lng],...], "width"?, "height"?, "markers"?: [[lat,lng,"label"],...]}` → `200 image/png`: points projected into a `width`×`height` (default 400×300) canvas and connected with a polyline; markers drawn as small dots. Errors: non-JSON/non-object body → `400 invalid_request_error`; `points` missing or `< 2` entries → `400`; `> 10000` points → `413`. |

```
curl -s -X POST http://127.0.0.1:$PORT/render \
  -H 'Content-Type: application/json' \
  -d '{"points":[[52.5,13.4],[52.51,13.41]],"markers":[[52.505,13.405,"landmark"]]}' \
  -o ride.png
```

No `docs.stripe.com` page corresponds to this one — it mocks the private BikeMap
render backend described in `loop/raw/github_repos.md` §3.1, not a real Stripe API.

## `payments.py` — Stripe-flavored charges/refunds/webhooks (backs int02)

Run: `python3 -m loop.mockserver.payments --port 0 [--seed 0] [--n 250] [--rate 5] [--fail-every 0]`.
`--seed`/`--n` control the deterministic fixture dataset of charges; `--rate` is the
per-client requests/second before `429`; `--fail-every N` makes every Nth request (that
passed rate limiting) come back `500` (0 = disabled). Import:
`from loop.mockserver.payments import serve, start_in_thread, sign, verify`.

Every `/v1/*` request runs, in order: (1) per-client sliding-window rate limit, (2) the
`--fail-every` counter, (3) `Authorization: Bearer sk_test_...` check, (4) route
dispatch. Every response carries a `Request-Id: req_<hex>` header
(docs.stripe.com/api/request_ids).

| Method & path | Behavior | docs.stripe.com |
|---|---|---|
| `GET /v1/charges?limit=&starting_after=&ending_before=` | Cursor pagination over a seeded, reverse-chronological charge list. `limit` 1–100 (default 10); `starting_after`/`ending_before` are mutually exclusive charge ids. `{"object":"list","data":[...],"has_more":bool,"url":"/v1/charges"}`. Invalid cursor / bad limit / both cursors → `400 invalid_request_error`. | `/api/pagination` |
| `GET /v1/charges/{id}` | One charge, or `404 {"error":{"type":"invalid_request_error","code":"resource_missing"}}`. | `/api/errors` |
| `POST /v1/refunds` | JSON or form body `{charge, amount?}` (amount defaults to the full unrefunded balance). With an `Idempotency-Key` header: same key + same body replays the cached response verbatim (same refund `id`); same key + different body → `400 idempotency_error`. No key → always creates a new refund. Already-fully-refunded charge → `400 charge_already_refunded`; amount over the remaining balance → `400 amount_too_large`. | `/api/idempotent_requests` |
| `POST /v1/webhook_endpoints/test` | body `{"url": "..."}`. Server builds a `charge.refunded` event (wrapping the most recent refund, or a synthetic one), signs it (`Stripe-Signature: t=<unix>,v1=<hmac_sha256 hex>`, secret `whsec_test_secret`), POSTs it to `url`, and reports `{"delivered": bool, "response_status": int|null, "event": {...}}`. | `/webhooks` |
| any `/v1/*` over the rate limit | `429 {"error":{"type":"rate_limit_error",...}}` + `Retry-After: 1`. | `/rate-limits` |
| missing/malformed `Authorization` | `401 {"error":{"type":"authentication_error",...}}`. | `/api/errors` |

`sign(payload: bytes, secret: str, t: int) -> str` and
`verify(payload: bytes, header: str, secret: str, tolerance: int = 300) -> bool` are
plain functions (HMAC-SHA256 over `f"{t}.{payload}"`, constant-time compare, default
5-minute tolerance) — a problem's `solution.py` can import and reuse them to implement
(or test) its own webhook verification, mirroring `docs.stripe.com/webhooks`.

```
# list + paginate
curl -s -H "Authorization: Bearer sk_test_x" "http://127.0.0.1:$PORT/v1/charges?limit=5"

# idempotent refund
curl -s -X POST http://127.0.0.1:$PORT/v1/refunds \
  -H "Authorization: Bearer sk_test_x" -H "Idempotency-Key: $(uuidgen)" \
  -d "charge=ch_...&amount=100"

# deliver a signed test webhook to a local receiver
curl -s -X POST http://127.0.0.1:$PORT/v1/webhook_endpoints/test \
  -H "Authorization: Bearer sk_test_x" -H 'Content-Type: application/json' \
  -d '{"url":"http://127.0.0.1:9000/hook"}'
```

## Tests

`rtk proxy python3 -m pytest loop/mockserver/tests -q` (run from the repo root) — 40
tests across `test_png.py` (PNG encoder internals), `test_maps.py` (render/health over
real HTTP), `test_payments.py` (pagination, rate limiting, idempotent refunds, webhook
signing/delivery, auth, `--fail-every`), each starting the real server on port 0 via
`serve()`/`start_in_thread()` and driving it with `urllib`.

## Known gaps (not blocking, listed for whoever writes int01/int02)

- `maps.py` markers ignore the `"label"` text (no font rendering in the hand-rolled PNG
  encoder) — the dot is drawn, the label string is accepted but not rendered.
- `payments.py` rate limiting and the idempotency cache are in-process only (no
  persistence across restarts) — fine for a per-round mock server.
- Amounts/limits are intentionally permissive compared to the real Stripe API (e.g. no
  per-currency zero-decimal handling) since int02's problem is about the client-side
  pagination/retry/idempotency/webhook logic, not currency edge cases (those are covered
  separately per `loop/raw/stripe_official_and_api.md` §3.10).
