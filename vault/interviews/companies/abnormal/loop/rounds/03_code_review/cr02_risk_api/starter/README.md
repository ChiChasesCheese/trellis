# riskapi

Read-only HTTP API over per-user insider-risk scores.

    GET /tenants/<tenant>/users/<user>/risk
    GET /tenants/<tenant>/users?sort=&cursor=&limit=

Requests carry `X-API-Key: <key_id>.<secret>`.

    python -m riskapi         # dev server (RISKAPI_DB, RISKAPI_PORT, RISKAPI_CACHE_TTL)
    python -m pytest          # unit tests
