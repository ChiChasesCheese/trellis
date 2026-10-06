from riskapi.rescore import rescore_all, rescore_tenant


def test_rescore_updates_changed_rows_only(world):
    db, _cache, _client = world
    assert rescore_tenant(db, "acme") == 5  # u1 -> 70, u2..u5 -> 0 (no signals), all differ from seeds
    assert rescore_tenant(db, "acme") == 0  # idempotent
    assert db.query("SELECT risk_score FROM users WHERE tenant_id='acme' AND user_id='u1'") == [(70,)]


def test_rescore_all_covers_each_tenant(world):
    db, _cache, _client = world
    assert rescore_all(db) == {"acme": 5, "globex": 1}


def test_rescore_can_be_limited_to_one_tenant(world):
    db, _cache, _client = world
    assert list(rescore_all(db, only="globex")) == ["globex"]
