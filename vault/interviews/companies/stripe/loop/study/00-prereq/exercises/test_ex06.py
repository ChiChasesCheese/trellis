"""ex06 测试。运行：python -m pytest test_ex06.py -q

用真的本地 http.server（127.0.0.1，端口传 0 让系统分配）——不打桩、不联网。
理由：分页和退避这两条考的是"多次真实往返之间的状态变化"（游标推进、连续失败后恢复），
打桩 urlopen 只能验证"调用了几次"，验证不出请求真的按预期的参数打到了服务端、
服务端真的按状态推进返回了不同的响应。退避测试把 sleep 换成一个只记录参数、不真的
等待的假函数（with_retry 本身把 sleep 设计成参数，方便这样测），所以整个文件跑起来是毫秒级的，
不会因为端口占用或时序而偶发失败。
"""
from __future__ import annotations

import json
import threading
import time
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import pytest

CHARGES = [{"id": f"ch_{i:03d}", "amount": i * 10} for i in range(1, 26)]  # 25 条


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_a):  # 别污染测试输出
        pass

    def _send_json(self, status: int, obj: dict, extra: dict | None = None) -> None:
        raw = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _send_bytes(self, status: int, raw: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}

        if u.path == "/text":
            return self._send_bytes(200, b"hello world", "text/plain")

        if u.path == "/binary":
            return self._send_bytes(200, bytes([0, 1, 2, 3, 255, 254]), "application/octet-stream")

        if u.path == "/missing":
            return self._send_json(404, {"error": {"type": "invalid_request_error", "code": "resource_missing"}})

        if u.path == "/slow":
            time.sleep(0.3)
            return self._send_json(200, {"ok": True})

        if u.path == "/always-500":
            return self._send_json(500, {"error": {"type": "api_error", "message": "boom"}})

        if u.path == "/v1/charges":
            ids = [c["id"] for c in CHARGES]
            try:
                limit = int(q.get("limit", "10"))
            except ValueError:
                return self._send_json(400, {"error": "bad limit"})
            start = ids.index(q["starting_after"]) + 1 if "starting_after" in q else 0
            page = CHARGES[start : start + limit]
            return self._send_json(
                200, {"object": "list", "data": page, "has_more": start + limit < len(ids)}
            )

        if u.path == "/flaky-recover":
            with self.server.lock:
                self.server.counters["flaky-recover"] += 1
                n = self.server.counters["flaky-recover"]
            if n == 1:
                return self._send_json(429, {"error": "slow down"}, extra={"Retry-After": "0.001"})
            if n == 2:
                return self._send_json(500, {"error": "hiccup"})
            return self._send_json(200, {"ok": True, "attempt": n})

        if u.path == "/retry-after-once":
            with self.server.lock:
                self.server.counters["retry-after-once"] += 1
                n = self.server.counters["retry-after-once"]
            if n == 1:
                return self._send_json(429, {"error": "slow down"}, extra={"Retry-After": "0.001"})
            return self._send_json(200, {"ok": True})

        return self._send_json(404, {"error": {"type": "invalid_request_error"}})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return self._send_json(400, {"error": "bad json"})

        if self.path == "/echo":
            return self._send_json(200, {"received": body, "content_type": self.headers.get("Content-Type")})

        if self.path == "/v1/charges":
            idem = self.headers.get("Idempotency-Key")
            with self.server.lock:
                if idem and idem in self.server.idem_store:
                    return self._send_json(200, self.server.idem_store[idem])
                if "amount" not in body:
                    return self._send_json(400, {"error": {"type": "invalid_request_error", "param": "amount"}})
                cid = f"ch_new_{len(self.server.idem_store) + 1}"
                result = {"id": cid, "amount": body["amount"], "status": "succeeded"}
                if idem:
                    self.server.idem_store[idem] = result
            return self._send_json(201, result)

        return self._send_json(404, {"error": {"type": "invalid_request_error"}})


@pytest.fixture(scope="module")
def server():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    srv.lock = threading.Lock()
    srv.counters: dict[str, int] = {"flaky-recover": 0, "retry-after-once": 0}
    srv.idem_store: dict[str, dict] = {}
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


# ---------------------------------------------------------------- build_query_url


def test_build_query_url_encodes_params(ex):
    got = ex.build_query_url("http://x/v1/charges", {"limit": 10, "starting_after": "ch_9"})
    assert got == "http://x/v1/charges?limit=10&starting_after=ch_9"


def test_build_query_url_empty_params_returns_url_unchanged(ex):
    assert ex.build_query_url("http://x/v1/charges", {}) == "http://x/v1/charges"
    assert ex.build_query_url("http://x/v1/charges", None) == "http://x/v1/charges"


# ---------------------------------------------------------------- fetch_text / fetch_to_file


def test_fetch_text_reads_body(ex, server):
    assert ex.fetch_text(server + "/text") == "hello world"


def test_fetch_text_404_raises_httperror_with_code_and_readable_body(ex, server):
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        ex.fetch_text(server + "/missing")
    e = exc_info.value
    assert e.code == 404
    parsed = json.loads(e.read().decode())
    assert parsed["error"]["code"] == "resource_missing"


def test_fetch_to_file_writes_exact_bytes(ex, server, tmp_path):
    dest = tmp_path / "out.bin"
    n = ex.fetch_to_file(server + "/binary", str(dest))
    assert n == 6
    assert dest.read_bytes() == bytes([0, 1, 2, 3, 255, 254])


# ---------------------------------------------------------------- http()


def test_http_get_with_params_returns_status_and_json(ex, server):
    status, _, body = ex.http("GET", server + "/v1/charges", params={"limit": 2})
    assert status == 200
    assert body["object"] == "list"
    assert len(body["data"]) == 2


def test_http_post_json_sets_content_type_and_encodes_body(ex, server):
    status, _, body = ex.http("POST", server + "/echo", body={"amount": 100})
    assert status == 200
    assert body["received"] == {"amount": 100}
    assert body["content_type"] == "application/json"


def test_http_4xx_returns_tuple_instead_of_raising(ex, server):
    status, _, body = ex.http("GET", server + "/missing")
    assert status == 404
    assert body["error"]["code"] == "resource_missing"


def test_http_timeout_raises(ex, server):
    with pytest.raises((TimeoutError, urllib.error.URLError)):
        ex.http("GET", server + "/slow", timeout=0.05)


# ---------------------------------------------------------------- list_all（真服务器，分页语义）


def test_list_all_paginates_across_multiple_pages(ex, server):
    got = ex.list_all(server, "/v1/charges", limit=10)
    assert [c["id"] for c in got] == [c["id"] for c in CHARGES]
    assert len(got) == 25


def test_list_all_single_page_when_limit_covers_everything(ex, server):
    got = ex.list_all(server, "/v1/charges", limit=100)
    assert len(got) == 25
    assert got[0]["id"] == "ch_001"
    assert got[-1]["id"] == "ch_025"


# ---------------------------------------------------------------- with_retry（真服务器）


def test_with_retry_does_not_retry_4xx(ex, server):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        return ex.http("GET", server + "/missing")

    status, _, _ = ex.with_retry(fn, attempts=5, base=0.001, sleep=lambda _d: None)
    assert status == 404
    assert calls["n"] == 1  # 4xx 不该重试


def test_with_retry_exhausts_attempts_on_persistent_5xx(ex, server):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        return ex.http("GET", server + "/always-500")

    status, _, _ = ex.with_retry(fn, attempts=3, base=0.001, sleep=lambda _d: None)
    assert status == 500
    assert calls["n"] == 3  # 用光了 attempts


def test_with_retry_backoff_is_exponential_with_jitter(ex, server):
    delays: list[float] = []

    def fn():
        return ex.http("GET", server + "/always-500")

    ex.with_retry(fn, attempts=4, base=0.01, sleep=delays.append)
    assert len(delays) == 3  # attempts=4 只重试 3 次（最后一次不再 sleep）
    for i, d in enumerate(delays):
        lo, hi = 0.01 * (2**i), 0.01 * (2**i) + 0.01
        assert lo <= d < hi, f"第 {i} 次退避延迟 {d} 不在 [{lo}, {hi}) 范围内"


def test_with_retry_recovers_via_real_server(ex, server):
    def fn():
        return ex.http("GET", server + "/flaky-recover")

    status, _, body = ex.with_retry(fn, attempts=5, base=0.001, sleep=time.sleep)
    assert status == 200
    assert body == {"ok": True, "attempt": 3}


def test_with_retry_honors_retry_after_header(ex, server):
    recorded: list[float] = []

    def fn():
        return ex.http("GET", server + "/retry-after-once")

    status, _, _ = ex.with_retry(fn, attempts=3, base=5.0, sleep=recorded.append)
    assert status == 200
    assert recorded == [0.001]  # 用了 Retry-After，而不是 base 算出来的退避


# ---------------------------------------------------------------- create_charge_idempotent


def test_create_charge_idempotent_creates_a_charge(ex, server):
    body = ex.create_charge_idempotent(server, 500, key="idem-key-a")
    assert body["amount"] == 500
    assert body["status"] == "succeeded"
    assert body["id"].startswith("ch_new_")


def test_create_charge_idempotent_same_key_returns_same_charge(ex, server):
    first = ex.create_charge_idempotent(server, 700, key="idem-key-b")
    second = ex.create_charge_idempotent(server, 700, key="idem-key-b")
    assert first["id"] == second["id"]
