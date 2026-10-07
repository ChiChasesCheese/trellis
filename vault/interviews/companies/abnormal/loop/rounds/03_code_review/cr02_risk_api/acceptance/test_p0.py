"""P0 findings: each test fails on the starter and passes on the fixed repo."""
import json
import pickle

import pytest
from riskapi_helpers import ACME_KEY, FLAG, GLOBEX_KEY, Evil, World

pytestmark = pytest.mark.core


def test_cr01_key_of_one_tenant_cannot_read_another_tenants_user():
    """CR-01 (IDOR): the path tenant must equal the tenant of the API key."""
    w = World()
    status, body = w.client.get("/tenants/globex/users/u1/risk", ACME_KEY)
    assert status in (403, 404)
    assert "Zed" not in json.dumps(body) and "off_hours" not in json.dumps(body)


def test_cr01_key_of_one_tenant_cannot_list_another_tenants_users():
    w = World()
    status, body = w.client.get("/tenants/globex/users", ACME_KEY)
    assert status in (403, 404)
    assert "Zed" not in json.dumps(body)


@pytest.mark.parametrize(
    "sort",
    ["email", "(SELECT 1)", "CASE WHEN (SELECT COUNT(*) FROM api_keys) > 0 THEN name ELSE user_id END", "name; DROP TABLE users", "name--"],
)
def test_cr02_sort_is_validated_against_a_whitelist(sort):
    """CR-02: `sort` is data, never SQL. Anything but the documented columns is a 400."""
    w = World()
    status, _body = w.client.get("/tenants/acme/users", ACME_KEY, sort=sort)
    assert status == 400
    assert w.db.query("SELECT COUNT(*) FROM users")[0][0] == 6  # nothing was dropped


def test_cr03_poisoned_cache_entry_is_never_unpickled():
    """CR-03: whoever can write to the cache must not get code execution in the API."""
    w = World()
    assert w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)[0] == 200
    for key in w.cache.keys():
        w.cache.set(key, pickle.dumps(Evil()), 60)
    FLAG.clear()
    status, body = w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert FLAG == []
    assert status == 200 and body["score"] == 70  # a corrupt entry is just a cache miss


def test_cr04_cached_score_of_one_tenant_is_not_served_to_another():
    """CR-04: user ids repeat across tenants, so the cache key must include the tenant."""
    w = World()
    s1, acme = w.client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    s2, globex = w.client.get("/tenants/globex/users/u1/risk", GLOBEX_KEY)
    assert (s1, s2) == (200, 200)
    assert acme["score"] == 70 and acme["name"] == "Ann"
    assert globex["score"] == 10 and globex["name"] == "Zed" and globex["tenant_id"] == "globex"
