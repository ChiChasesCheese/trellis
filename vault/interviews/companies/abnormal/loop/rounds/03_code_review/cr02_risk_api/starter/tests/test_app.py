from conftest import ACME_KEY


def test_risk_for_own_user(world):
    _db, _cache, client = world
    status, body = client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert status == 200
    assert body["score"] == 70 and body["level"] == "high"
    assert [f["kind"] for f in body["factors"]] == ["mass_download", "impossible_travel"]


def test_risk_is_cached(world):
    _db, cache, client = world
    client.get("/tenants/acme/users/u1/risk", ACME_KEY)
    assert len(cache.keys("risk:")) == 1


def test_missing_key_is_401(world):
    _db, _cache, client = world
    assert client.get("/tenants/acme/users/u1/risk")[0] == 401


def test_unknown_user_is_404(world):
    _db, _cache, client = world
    assert client.get("/tenants/acme/users/nobody/risk", ACME_KEY)[0] == 404


def test_list_sorted_by_user_id_by_default(world):
    _db, _cache, client = world
    status, body = client.get("/tenants/acme/users", ACME_KEY)
    assert status == 200
    assert [i["user_id"] for i in body["items"]] == ["u1", "u2", "u3", "u4", "u5"]
    assert body["next_cursor"] is None


def test_list_sorted_by_name(world):
    _db, _cache, client = world
    _status, body = client.get("/tenants/acme/users", ACME_KEY, "sort=name")
    assert [i["name"] for i in body["items"]] == ["Ann", "Bob", "Cy", "Di", "Eve"]


def test_first_page_has_cursor_when_full(world):
    _db, _cache, client = world
    _status, body = client.get("/tenants/acme/users", ACME_KEY, "limit=2")
    assert [i["user_id"] for i in body["items"]] == ["u1", "u2"]
    assert body["next_cursor"]
