from riskapi.cache import Cache


def test_value_expires():
    t = [0.0]
    c = Cache(clock=lambda: t[0])
    c.set("k", b"v", ttl=10)
    assert c.get("k") == b"v"
    t[0] = 10
    assert c.get("k") is None


def test_delete_and_keys():
    c = Cache()
    c.set("a:1", b"x", 10)
    c.set("b:1", b"y", 10)
    assert c.keys("a:") == ["a:1"]
    c.delete("a:1")
    assert c.keys() == ["b:1"]
