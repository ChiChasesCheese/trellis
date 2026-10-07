from fanout.dedup import DedupCache


def test_seen_after_add_until_ttl():
    t = [0.0]
    c = DedupCache(ttl_s=10, clock=lambda: t[0])
    assert not c.seen("k")
    c.add("k")
    assert c.seen("k")
    t[0] = 11
    assert not c.seen("k")


def test_add_evicts_expired_entries():
    t = [0.0]
    c = DedupCache(ttl_s=10, clock=lambda: t[0])
    c.add("old")
    t[0] = 20
    c.add("new")
    assert not c.seen("old") and c.seen("new")
