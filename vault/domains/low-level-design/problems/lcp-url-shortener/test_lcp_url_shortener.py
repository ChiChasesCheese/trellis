"""短链服务的测试：README 的每条规则与示例、边界、错误优先级、并发（真线程 + 屏障）、两个连接同时写。"""

import importlib
import json
import math
import os
import re
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class Clock:
    """可手动拨动的时钟：过期测试不用 sleep。"""

    def __init__(self, now: float = 1_760_000_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def svc(clock):
    return impl.URLShortener(":memory:", clock=clock)


@pytest.fixture
def api(svc):
    return impl.Api(svc, "http://localhost:8080")


def post(api, body):
    return api.handle("POST", "/links", json.dumps(body).encode())


def only_error_key(reply) -> bool:
    return set(reply.body) == {"error"} and isinstance(reply.body["error"], str)


# ---------- 创建与校验 ----------

def test_create_returns_public_fields_and_a_secret_token(svc):
    link = svc.create("https://example.com/path")
    assert re.fullmatch(r"[A-Za-z0-9]{6,10}", link.short_code)
    assert link.long_url == "https://example.com/path"
    assert link.expires_at is None and link.hit_count == 0
    assert link.owner_token.startswith("tok_") and len(link.owner_token) >= 16
    assert set(link.to_dict()) == {"short_code", "long_url", "created_at", "expires_at", "hit_count", "is_expired"}


def test_same_url_twice_makes_two_independent_links(svc):
    first, second = svc.create("https://example.com"), svc.create("https://example.com")
    assert first.short_code != second.short_code and first.owner_token != second.owner_token
    assert svc.get_stats()["total_links"] == 2


@pytest.mark.parametrize("url", [
    "https://example.com", "http://example.com/a?b=c#d", "https://127.0.0.1:8080/x", "https://[::1]/x",
    "HTTP://EXAMPLE.com", "  https://example.com/a  "])
def test_valid_urls(svc, url):
    assert svc.create(url).long_url == url.strip()


@pytest.mark.parametrize("url", [
    None, 123, ["https://a.example"], "", "   ", "example.com", "ftp://example.com", "javascript:alert(1)",
    "https://", "http://", "https:///path", "https://user@/p", "https:example.com", "https://bad host/path",
    "https://exa\tmple.com", "https://example.com/a\nb", "https://example.com/\x7f", "https://host:99999/",
    "https://host:abc/", "http://[::1/"])
def test_invalid_urls(svc, url):
    with pytest.raises(impl.ValidationError):
        svc.create(url)
    assert svc.get_stats()["total_links"] == 0


@pytest.mark.parametrize("code", ["abc", "x" * 32, "Ab9_-Z", "docs_2026"])
def test_valid_custom_codes(svc, code):
    assert svc.create("https://example.com", custom_code=code).short_code == code


@pytest.mark.parametrize("code", ["", "ab", "x" * 33, "has space", "bad/code", "bad.code", "bad@code",
                                  "abc\n", "abc\x00", "日本語abc", 123, True, ["abc"]])
def test_invalid_custom_codes(svc, code):
    with pytest.raises(impl.ValidationError):
        svc.create("https://example.com", custom_code=code)


def test_custom_code_conflicts_and_is_case_sensitive(svc):
    svc.create("https://a.example", custom_code="same-code")
    with pytest.raises(impl.ConflictError):
        svc.create("https://b.example", custom_code="same-code")
    assert svc.create("https://b.example", custom_code="Same-Code").short_code == "Same-Code"
    assert svc.get("same-code").long_url == "https://a.example"  # 冲突的创建没有覆盖原来的链接


@pytest.mark.parametrize("code", ["stats", "links"])
def test_codes_that_collide_with_routes_are_refused(svc, code):
    with pytest.raises(impl.ConflictError):
        svc.create("https://example.com", custom_code=code)


@pytest.mark.parametrize("ttl", [1, 0.5, 3600, 1e300, 10**308, None])
def test_valid_ttl(svc, ttl):
    link = svc.create("https://example.com", ttl_seconds=ttl)
    assert (link.expires_at is None) == (ttl is None)


@pytest.mark.parametrize("ttl", [0, 0.0, -1, -0.5, "10", "", True, False, math.nan, math.inf, -math.inf,
                                 10**400, [1], {"s": 1}])
def test_invalid_ttl(svc, ttl):
    with pytest.raises(impl.ValidationError):
        svc.create("https://example.com", ttl_seconds=ttl)


# ---------- 自动短码 ----------

def test_five_collisions_raise_after_exactly_five_calls(svc):
    svc.create("https://taken.example", custom_code="ABCDEF")
    calls = []
    svc._generate_code = lambda url: calls.append(url) or "ABCDEF"
    with pytest.raises(impl.CodeGenerationError):
        svc.create("https://new.example")
    assert len(calls) == 5 and svc.get_stats()["total_links"] == 1


def test_collision_then_success_uses_one_call_per_code(svc):
    svc.create("https://taken.example", custom_code="ABCDEF")
    queue = iter(["ABCDEF", "ABCDEF", "fresh01"])
    svc._generate_code = lambda url: next(queue)
    assert svc.create("https://new.example").short_code == "fresh01"


@pytest.mark.parametrize("bad", ["bad/code", "abc", "x" * 11, "abcdef\n", "ab_def1", ""])
def test_generator_returning_invalid_code_is_an_error(svc, bad):
    svc._generate_code = lambda url: bad
    with pytest.raises(impl.CodeGenerationError):
        svc.create("https://new.example")
    assert svc.get_stats()["total_links"] == 0


def test_custom_code_and_auto_code_share_one_namespace(svc):
    svc.create("https://a.example", custom_code="Zz9Zz9")
    svc._generate_code = lambda url: "Zz9Zz9"
    with pytest.raises(impl.CodeGenerationError):
        svc.create("https://b.example")


# ---------- 过期、跳转、计数 ----------

def test_expiry_boundary_is_inclusive(svc, clock):
    link = svc.create("https://example.com", custom_code="ttl01", ttl_seconds=60)
    assert link.expires_at == clock.now + 60
    clock.now += 59.999
    assert not svc.get("ttl01").is_expired
    clock.now += 0.001
    assert svc.get("ttl01").is_expired  # 恰好等于 expires_at 就是过期


def test_expired_redirect_is_gone_and_counts_nothing(svc, clock):
    svc.create("https://example.com", custom_code="ttl01", ttl_seconds=10)
    assert svc.resolve_redirect("ttl01") == "https://example.com"
    clock.now += 10
    with pytest.raises(impl.ExpiredLinkError):
        svc.resolve_redirect("ttl01")
    assert svc.get("ttl01").hit_count == 1  # 过期的那次没有加


def test_redirect_missing_and_increment_missing(svc):
    with pytest.raises(impl.NotFoundError):
        svc.resolve_redirect("missing")
    with pytest.raises(impl.NotFoundError):
        svc.increment_hits("missing")


def test_increment_hits_counts_even_when_expired(svc, clock):
    svc.create("https://example.com", custom_code="ttl01", ttl_seconds=1)
    clock.now += 5
    svc.increment_hits("ttl01")
    assert svc.get("ttl01").hit_count == 1


def test_get_unknown_and_non_string_code_is_none(svc):
    assert svc.get("nope") is None and svc.get(None) is None and svc.get(["x"]) is None


def test_link_is_a_snapshot(svc):
    link = svc.create("https://example.com", custom_code="snap1")
    svc.resolve_redirect("snap1")
    assert link.hit_count == 0 and svc.get("snap1").hit_count == 1
    with pytest.raises(Exception):
        link.hit_count = 5


# ---------- 删除 ----------

def test_delete_error_precedence_and_effects(svc):
    link = svc.create("https://example.com", custom_code="gone1")
    svc.resolve_redirect("gone1")
    for token in ("", None, 123):
        with pytest.raises(impl.ValidationError):
            svc.delete("gone1", token)
    with pytest.raises(impl.ValidationError):
        svc.delete("no-such-code", "")  # 缺令牌先于查短码
    with pytest.raises(impl.PermissionDeniedError):
        svc.delete("gone1", "wrong")
    assert svc.get("gone1") is not None
    assert svc.delete("no-such-code", "tok_x") is False
    assert svc.delete("gone1", link.owner_token) is True
    assert svc.get("gone1") is None
    assert svc.delete("gone1", link.owner_token) is False
    assert svc.get_stats() == {"total_links": 0, "total_hits": 0, "top_5_links": []}


def test_deleted_code_can_be_reused_with_a_new_token(svc):
    old = svc.create("https://a.example", custom_code="reuse1")
    svc.delete("reuse1", old.owner_token)
    new = svc.create("https://b.example", custom_code="reuse1")
    with pytest.raises(impl.PermissionDeniedError):
        svc.delete("reuse1", old.owner_token)
    assert svc.delete("reuse1", new.owner_token) is True


def test_token_of_one_link_cannot_delete_another(svc):
    svc.create("https://a.example", custom_code="aaa")
    other = svc.create("https://b.example", custom_code="bbb")
    with pytest.raises(impl.PermissionDeniedError):
        svc.delete("aaa", other.owner_token)


# ---------- 统计 ----------

def test_stats_order_limit_and_expired_included(svc, clock):
    for i in range(6):
        svc.create(f"https://example.com/{i}", custom_code=f"code{i}", ttl_seconds=100 if i == 5 else None)
        for _ in range(i):
            svc.resolve_redirect(f"code{i}")
    clock.now += 1000  # code5 已过期，但仍然计入
    stats = svc.get_stats()
    assert (stats["total_links"], stats["total_hits"]) == (6, 15)
    assert [row["short_code"] for row in stats["top_5_links"]] == ["code5", "code4", "code3", "code2", "code1"]
    assert set(stats["top_5_links"][0]) == {"short_code", "long_url", "hit_count"}


def test_stats_ties_break_by_short_code_ascending(svc):
    for code in ("beta", "Zulu", "alpha", "Alpha", "zulu7", "m1m1m1"):
        svc.create("https://example.com", custom_code=code)
    assert [r["short_code"] for r in svc.get_stats()["top_5_links"]] == ["Alpha", "Zulu", "alpha", "beta", "m1m1m1"]


def test_stats_with_no_links(svc):
    assert svc.get_stats() == {"total_links": 0, "total_hits": 0, "top_5_links": []}


# ---------- 持久化与并发 ----------

def test_data_survives_reopening_the_file(tmp_path):
    path = str(tmp_path / "s.db")
    first = impl.URLShortener(path)
    first.create("https://example.com", custom_code="keep1")
    first.resolve_redirect("keep1")
    second = impl.URLShortener(path)
    assert second.get("keep1").hit_count == 1


def run_threads(count, target):
    barrier, errors, results = threading.Barrier(count), [], [None] * count

    def worker(i):
        try:
            barrier.wait()
            results[i] = target(i)
        except Exception as exc:  # 收集：线程里的异常不会让测试失败，要自己带回来
            results[i] = exc
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def test_concurrent_redirects_count_exactly(svc):
    svc.create("https://example.com", custom_code="hot01")
    results = run_threads(100, lambda i: svc.resolve_redirect("hot01"))
    assert results == ["https://example.com"] * 100
    assert svc.get("hot01").hit_count == 100


def test_concurrent_increment_hits_count_exactly(svc):
    svc.create("https://example.com", custom_code="hot01")
    run_threads(100, lambda i: svc.increment_hits("hot01"))
    assert svc.get("hot01").hit_count == 100


def test_concurrent_same_custom_code_has_exactly_one_winner(svc):
    results = run_threads(32, lambda i: svc.create(f"https://example.com/{i}", custom_code="race01"))
    winners = [r for r in results if isinstance(r, impl.Link)]
    assert len(winners) == 1
    assert sum(isinstance(r, impl.ConflictError) for r in results) == 31
    assert svc.get("race01").long_url == winners[0].long_url


def test_concurrent_auto_creates_get_distinct_codes(svc):
    results = run_threads(100, lambda i: svc.create(f"https://example.com/{i}"))
    assert len({r.short_code for r in results}) == 100 and svc.get_stats()["total_links"] == 100


def test_concurrent_delete_has_one_winner(svc):
    link = svc.create("https://example.com", custom_code="del01")
    results = run_threads(20, lambda i: svc.delete("del01", link.owner_token))
    assert results.count(True) == 1 and results.count(False) == 19


def test_redirects_racing_with_expiry_never_count_after_it(svc, clock):
    svc.create("https://example.com", custom_code="race02", ttl_seconds=5)
    clock.now += 5  # 已经到点：无论哪个线程先进，都必须是 410

    def hit(i):
        try:
            return svc.resolve_redirect("race02")
        except impl.ExpiredLinkError:
            return "gone"
    assert set(run_threads(40, hit)) == {"gone"} and svc.get("race02").hit_count == 0


def test_two_connections_on_one_file_do_not_lose_hits(tmp_path):
    path = str(tmp_path / "shared.db")
    a, b = impl.URLShortener(path), impl.URLShortener(path)  # 相当于两个 worker 进程
    a.create("https://example.com", custom_code="multi1")
    run_threads(40, lambda i: (a if i % 2 else b).resolve_redirect("multi1"))
    assert a.get("multi1").hit_count == 40


def test_stats_total_matches_sum_while_writing(svc):
    for i in range(5):
        svc.create("https://example.com", custom_code=f"code{i}")

    def work(i):
        if i % 2:
            svc.resolve_redirect(f"code{i % 5}")
            return None
        stats = svc.get_stats()
        return stats["total_hits"] == sum(r["hit_count"] for r in stats["top_5_links"])  # 五条链接全在榜上
    assert all(r in (None, True) for r in run_threads(60, work))


# ---------- HTTP 合同 ----------

def test_readme_create_example(api, clock):
    reply = post(api, {"long_url": "https://example.com/a/very/long/page", "custom_code": "docs_2026", "ttl_seconds": 3600})
    body = dict(reply.body)
    assert re.fullmatch(r"tok_[A-Za-z0-9_-]{16,}", body.pop("owner_token"))
    assert reply.status == 201 and body == {
        "short_code": "docs_2026", "short_url": "http://localhost:8080/docs_2026",
        "long_url": "https://example.com/a/very/long/page", "created_at": 1760000000.0,
        "expires_at": 1760003600.0, "hit_count": 0, "is_expired": False}


def test_short_url_follows_the_request_host(svc):
    reply = impl.Api(svc).create_link({"long_url": "https://example.com"}, "https://sho.rt/")
    assert reply.body["short_url"] == f"https://sho.rt/{reply.body['short_code']}"


def test_redirect_metadata_and_delete_flow(api):
    made = post(api, {"long_url": "https://example.com/a", "custom_code": "flow01", "ttl_seconds": 30}).body
    reply = api.handle("GET", "/flow01")
    assert (reply.status, reply.location) == (302, "https://example.com/a")
    meta = api.handle("GET", "/links/flow01")
    assert meta.status == 200 and "owner_token" not in meta.body and "short_url" not in meta.body
    assert meta.body["hit_count"] == 1 and set(meta.body) == {
        "short_code", "long_url", "created_at", "expires_at", "hit_count", "is_expired"}
    deleted = api.handle("DELETE", "/links/flow01", json.dumps({"owner_token": made["owner_token"]}).encode())
    assert (deleted.status, deleted.body) == (200, {"deleted": "flow01"})
    assert api.handle("GET", "/links/flow01/").status == 404  # 末尾斜杠可有可无
    assert api.handle("GET", "/flow01").status == 404


def test_expired_link_http_statuses(api, clock):
    post(api, {"long_url": "https://example.com", "custom_code": "ttl02", "ttl_seconds": 5})
    clock.now += 5
    gone = api.handle("GET", "/ttl02")
    assert gone.status == 410 and only_error_key(gone) and gone.location is None
    meta = api.handle("GET", "/links/ttl02")
    assert meta.status == 200 and meta.body["is_expired"] is True and meta.body["hit_count"] == 0


@pytest.mark.parametrize("raw", [b"", b"not-json", b"{bad", b"[1, 2]", b'"text"', b"null", b"\xff\xfe"])
def test_bad_create_bodies_are_400_json(api, raw):
    reply = api.handle("POST", "/links", raw)
    assert reply.status == 400 and only_error_key(reply)


@pytest.mark.parametrize("body, status", [
    ({}, 400), ({"long_url": "ftp://x"}, 400), ({"long_url": "https://x.example", "custom_code": "ab"}, 400),
    ({"long_url": "https://x.example", "ttl_seconds": True}, 400),
    ({"long_url": "https://x.example", "ttl_seconds": "5"}, 400),
    ({"long_url": "https://x.example", "custom_code": None, "ttl_seconds": None}, 201),
    ({"long_url": "https://x.example", "extra": 1}, 201)])
def test_create_status_codes(api, body, status):
    reply = post(api, body)
    assert reply.status == status and (status == 201 or only_error_key(reply))


def test_nan_and_infinity_literals_in_json_are_400(api):
    for literal in (b"NaN", b"Infinity", b"-Infinity", b"1e999"):
        raw = b'{"long_url": "https://x.example", "ttl_seconds": ' + literal + b"}"
        assert api.handle("POST", "/links", raw).status == 400


def test_http_conflict_and_generation_failure(api, svc):
    post(api, {"long_url": "https://a.example", "custom_code": "dup01"})
    reply = post(api, {"long_url": "https://b.example", "custom_code": "dup01"})
    assert reply.status == 409 and only_error_key(reply)
    svc._generate_code = lambda url: "dup01x"
    post(api, {"long_url": "https://a.example", "custom_code": "dup01x"})
    reply = post(api, {"long_url": "https://c.example"})
    assert reply.status == 500 and only_error_key(reply)


def test_http_delete_statuses(api):
    token = post(api, {"long_url": "https://a.example", "custom_code": "del02"}).body["owner_token"]

    def delete(code, body):
        return api.handle("DELETE", f"/links/{code}", b"" if body is None else json.dumps(body).encode())
    assert delete("del02", None).status == 400
    assert delete("del02", {}).status == 400
    assert delete("del02", {"owner_token": ""}).status == 400
    assert api.handle("DELETE", "/links/del02", b"{bad").status == 400
    assert delete("del02", ["x"]).status == 400
    assert delete("del02", {"owner_token": "wrong"}).status == 403
    assert delete("missing", {"owner_token": token}).status == 404
    assert delete("del02", {"owner_token": token}).status == 200


@pytest.mark.parametrize("method, path, status", [
    ("PUT", "/links", 405), ("GET", "/links", 404), ("POST", "/stats", 405), ("DELETE", "/stats", 405),
    ("DELETE", "/abc123", 405), ("POST", "/links/abc123", 405), ("PATCH", "/links/abc123", 405),
    ("GET", "/a/b/c", 404), ("GET", "/links/a/b", 404), ("GET", "/missing-code", 404)])
def test_routing_statuses_are_json(api, method, path, status):
    reply = api.handle(method, path, b"{}")
    assert reply.status == status and only_error_key(reply)


def test_stats_http_shape_and_static_route_wins(api):
    post(api, {"long_url": "https://a.example", "custom_code": "abc"})
    api.handle("GET", "/abc")
    reply = api.handle("GET", "/stats/")
    assert reply.status == 200 and reply.body == {
        "total_links": 1, "total_hits": 1,
        "top_5_links": [{"short_code": "abc", "long_url": "https://a.example", "hit_count": 1}]}
