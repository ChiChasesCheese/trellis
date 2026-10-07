# Add per-user risk score endpoint with caching

**Author:** Priya Raman (@praman) · **Reviewers:** you · **Size:** +290 / -4 (13 files, tests included)

## Why

The Insider Risk console needs to show a risk score and its top factors for a user, and the customer
success team wants to export the user list sorted by risk. Computing the score from raw signals takes
a few queries, and the console polls the same users repeatedly, so I added a cache in front of it.

## What changed

- `riskapi/app.py`: a small WSGI app with two routes
  - `GET /tenants/<tenant>/users/<user>/risk`
  - `GET /tenants/<tenant>/users?sort=&cursor=&limit=` (keyset pagination, `sort` is any column you want to order by)
- `riskapi/auth.py`: `X-API-Key: <key_id>.<secret>` authentication against the `api_keys` table.
- `riskapi/service.py`: read-through cache for the risk payload. Values are serialised with `pickle`
  so we can cache the dict as-is (we can put richer objects in later).
- `riskapi/cache.py`: in-memory TTL cache with a Redis-like interface (bytes in, bytes out), to be swapped for Redis.
- `riskapi/repo.py`: SQL for the endpoints.
- `riskapi/server.py`: `python -m riskapi` dev server.

## Notes

- API keys are validated on every request; any valid key may call the API (keys are per tenant, and the
  tenant is part of the URL).
- Cache TTL is 5 minutes (`RISKAPI_CACHE_TTL`). I log each lookup with the user so we can debug score disputes.
- Pagination returns a `next_cursor` whenever the page is full.

## Tested locally

- `python -m pytest` is green (17 tests).
- Hit both endpoints with curl against a seeded sqlite file; sorting by `name` and `risk_score` works.
- Not load tested.
