from fanout.dedup import DedupCache


def test_second_claim_fails_until_ttl():
    t = [0.0]
    c = DedupCache(ttl_s=10, clock=lambda: t[0])
    assert c.claim("k") is True
    assert c.claim("k") is False
    t[0] = 11
    assert c.claim("k") is True


def test_release_allows_a_retry():
    c = DedupCache()
    assert c.claim("k")
    c.release("k")
    assert c.claim("k")
