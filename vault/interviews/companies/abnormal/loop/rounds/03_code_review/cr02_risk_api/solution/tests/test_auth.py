from conftest import ACME_KEY

from riskapi.auth import authenticate


def test_valid_key(world):
    db, _cache, _client = world
    p = authenticate(db, {"X-API-Key": ACME_KEY})
    assert p is not None and p.tenant_id == "acme"


def test_wrong_secret_and_malformed_keys(world):
    db, _cache, _client = world
    assert authenticate(db, {"X-API-Key": "k_acme.nope"}) is None
    assert authenticate(db, {"X-API-Key": "no-dot"}) is None
    assert authenticate(db, {}) is None
