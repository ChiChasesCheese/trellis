"""P1/P2 findings: fail on the starter, pass on the fixed repo (not required for a v1 review pass)."""
import hashlib
import hmac
import json
import logging

import pytest
from riskapi_helpers import ACME_KEY, World, run_concurrently

from riskapi import db as dbmod
from riskapi.auth import authenticate
from riskapi.cache import Cache
from riskapi.db import Database

pytestmark = pytest.mark.stretch


def test_cr05_api_key_secret_is_not_stored_in_plaintext_or_md5():
    db = Database()
    dbmod.create_api_key(db, "acme", "k1", "super-secret-value")
    stored = " ".join(str(v) for row in db.query("SELECT * FROM api_keys") for v in row)
    assert "super-secret-value" not in stored
    assert hashlib.md5(b"super-secret-value").hexdigest() not in stored
    assert authenticate(db, {"X-API-Key": "k1.super-secret-value"}).tenant_id == "acme"
    assert authenticate(db, {"X-API-Key": "k1.wrong"}) is None


def test_cr05_api_key_digest_is_compared_in_constant_time(monkeypatch):
    calls = []
    real = hmac.compare_digest
    monkeypatch.setattr(hmac, "compare_digest", lambda a, b: calls.append(1) or real(a, b))
    w = World()
    authenticate(w.db, {"X-API-Key": ACME_KEY})
    assert calls


def test_cr06_concurrent_cold_requests_hit_the_database_once():
    """CR-06: single-flight. A hot key expiring must not send every waiting request to the database."""
    import time

    class SlowDB(Database):
        loads = 0

        def query(self, sql, params=()):
            if "FROM signals" in sql:
                SlowDB.loads += 1
                time.sleep(0.2)
            return super().query(sql, params)

    w = World(db_cls=SlowDB)
    results = run_concurrently(8, lambda: w.client.get("/tenants/acme/users/u1/risk", ACME_KEY))
    assert all(r[0] == 200 and r[1]["score"] == 70 for r in results)
    assert SlowDB.loads == 1


def test_cr07_cursor_pagination_has_no_duplicates_or_gaps():
    w = World()
    seen, cursor = [], None
    for _ in range(10):
        extra = {"cursor": cursor} if cursor else {}
        status, body = w.client.get("/tenants/acme/users", ACME_KEY, limit=2, **extra)
        assert status == 200
        seen += [i["user_id"] for i in body["items"]]
        cursor = body["next_cursor"]
        if not cursor:
            break
    assert seen == ["u1", "u2", "u3", "u4", "u5"]


def test_cr07_pagination_by_a_non_unique_sort_key_is_stable():
    w = World()
    seen, cursor = [], None
    for _ in range(10):
        extra = {"cursor": cursor} if cursor else {}
        _status, body = w.client.get("/tenants/acme/users", ACME_KEY, sort="risk_score", limit=2, **extra)
        seen += [i["user_id"] for i in body["items"]]
        cursor = body["next_cursor"]
        if not cursor:
            break
    assert sorted(seen) == ["u1", "u2", "u3", "u4", "u5"] and len(seen) == 5


def test_cr08_limit_is_bounded():
    w = World(extra_acme_users=300)
    status, body = w.client.get("/tenants/acme/users", ACME_KEY, limit=100000)
    assert status == 200 and len(body["items"]) <= 200
    for bad in ("0", "-1", "abc"):
        assert w.client.get("/tenants/acme/users", ACME_KEY, limit=bad)[0] == 400


def test_cr09_email_is_not_logged(caplog):
    caplog.set_level(logging.DEBUG)
    w = World()
    w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert "ann@acme.example.com" not in caplog.text


def test_cr11_errors_share_one_shape():
    w = World()
    cases = [
        w.client.get("/tenants/acme/users/u1/risk"),
        w.client.get("/tenants/acme/users/nobody/risk", ACME_KEY),
        w.client.get("/nope", ACME_KEY),
        w.client.get("/tenants/acme/users", ACME_KEY, limit="abc"),
    ]
    for status, body in cases:
        assert status >= 400
        assert set(body) == {"error"} and {"code", "message"} <= set(body["error"])


def test_cr11_unexpected_errors_do_not_leak_internals():
    class Boom(Database):
        def query(self, sql, params=()):
            if "FROM users" in sql:
                raise RuntimeError("no such column: secret_internal_column")
            return super().query(sql, params)

    w = World(db_cls=Boom)
    status, body = w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert status == 500 and "secret_internal_column" not in json.dumps(body)


def test_cr12_cache_has_a_size_bound():
    t = [0.0]
    cache = Cache(clock=lambda: t[0], max_entries=10)
    for i in range(100):
        cache.set(f"k{i}", b"v", ttl=1000)
    assert len(cache.keys()) <= 10
