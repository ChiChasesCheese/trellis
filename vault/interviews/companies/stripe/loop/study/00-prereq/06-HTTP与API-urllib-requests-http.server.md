# 06 · HTTP 与 API：写客户端、写服务端、处理失败

> Stripe 的 **Integration 轮**（onsite）就是这个：给你一份 API 文档 + 一个跑着的服务，让你写客户端完成任务（分页拉数据、聚合、重试、幂等）。有时反过来：让你实现一个小服务端。本章用**纯标准库**（`urllib` / `http.server`），因为面试环境不一定能装 `requests`；`requests` 的写法也给出来，会一个另一个 5 分钟就懂。

## 1. HTTP 十句话

1. 一次请求 = **方法** + **URL** + **头（headers）** + **体（body）**。
2. 方法：`GET` 读、`POST` 创建、`PUT/PATCH` 改、`DELETE` 删。
3. URL：`https://api.example.com/v1/charges?limit=10&starting_after=ch_9` —— `?` 后面是查询参数。
4. 响应 = **状态码** + 头 + 体（通常 JSON）。
5. 状态码：`2xx` 成功；`400` 参数错；`401` 没认证；`403` 没权限；`404` 没这东西；`409` 冲突；`429` 请求太频繁（限流）；`5xx` 服务端挂了。
6. **4xx 是你的错，重试没用；5xx 和 429 是他们的问题，可以重试。**（`429` 看 `Retry-After` 头。）
7. 认证：`Authorization: Bearer sk_test_xxx` 头。
8. 发 JSON：`Content-Type: application/json`，body 是 `json.dumps(obj).encode()`。
9. 幂等：同一个操作重复发不会重复生效。POST 默认不幂等 → 用 `Idempotency-Key` 头。
10. 超时：网络会卡，每个请求都设 `timeout`。

## 2. 客户端：`urllib`（标准库）

```python
import json
import urllib.request
import urllib.error
import urllib.parse


def http(method: str, url: str, *, body: dict | None = None, headers: dict | None = None,
         params: dict | None = None, timeout: float = 5.0) -> tuple[int, dict, dict]:
    """返回 (status, headers, json_body)。4xx/5xx 不抛异常，也返回。"""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            return resp.status, dict(resp.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:            # 4xx / 5xx 走这里
        raw = e.read().decode()
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return e.code, dict(e.headers), parsed
```

用法：
```python
status, hdrs, body = http("GET", "http://localhost:8000/v1/charges", params={"limit": 10})
status, hdrs, body = http("POST", "http://localhost:8000/v1/charges",
                          body={"amount": 100}, headers={"Idempotency-Key": "k1"})
```

`requests` 版（如果能装）：
```python
import requests
r = requests.get(url, params={"limit": 10}, timeout=5)
r.status_code; r.headers; r.json()
r = requests.post(url, json={"amount": 100}, headers={"Idempotency-Key": "k1"}, timeout=5)
```

## 3. 三个必会模式

### 3.1 分页（cursor 式，Stripe 风格）

```python
def list_all(base: str, path: str, limit: int = 100) -> list[dict]:
    out, cursor = [], None
    while True:
        params = {"limit": limit}
        if cursor:
            params["starting_after"] = cursor
        status, _, body = http("GET", base + path, params=params)
        if status != 200:
            raise RuntimeError(f"{status}: {body}")
        out.extend(body["data"])
        if not body.get("has_more") or not body["data"]:
            return out
        cursor = body["data"][-1]["id"]
```

要点：终止条件两个（`has_more` 假 **或** 本页为空，防死循环）；游标是最后一条的 id。
页码式（`page=1,2,3`）就是 `page += 1` 直到返回空。

### 3.2 重试 + 退避（只对 429/5xx/网络错）

```python
import random
import time

RETRYABLE = {429, 500, 502, 503, 504}

def with_retry(fn, *, attempts: int = 5, base: float = 0.2, sleep=time.sleep):
    """fn() 返回 (status, headers, body)。可重试的状态码指数退避 + 抖动；4xx 直接返回。"""
    for i in range(attempts):
        try:
            status, headers, body = fn()
        except (urllib.error.URLError, TimeoutError) as e:      # 网络错也重试
            status, headers, body = 599, {}, {"error": str(e)}
        if status not in RETRYABLE or i == attempts - 1:
            return status, headers, body
        retry_after = headers.get("Retry-After")
        delay = float(retry_after) if retry_after else base * (2 ** i) + random.uniform(0, base)
        sleep(delay)
    return status, headers, body   # 不会到这
```

- **指数退避**：0.2 → 0.4 → 0.8 → 1.6s；**抖动**（jitter）防止大家同时重试。
- `sleep` 作为参数传进来 → 测试里传一个假的，不用真等。
- **只能对幂等操作重试**：GET 天然幂等；POST 必须带 `Idempotency-Key` 才能重试。

### 3.3 幂等键

```python
import uuid
key = str(uuid.uuid4())          # 一次业务操作生成一次，重试时**复用同一个**
status, _, body = with_retry(lambda: http("POST", url, body={"amount": 100},
                                          headers={"Idempotency-Key": key}))
```

服务端语义（Stripe）：同 key + 同参数 → 返回第一次的结果；同 key + 不同参数 → `400 idempotency_error`；key 24 小时后过期。

## 4. 服务端：`http.server`（标准库，面试 mock 用）

```python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

STORE: dict[str, dict] = {}          # id -> charge

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, obj: dict, extra: dict | None = None) -> None:
        raw = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urlparse(self.path)                 # path + query
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == "/v1/charges":
            ids = sorted(STORE)
            start = ids.index(q["starting_after"]) + 1 if "starting_after" in q else 0
            limit = int(q.get("limit", 10))
            page = ids[start:start + limit]
            return self._send(200, {"object": "list", "data": [STORE[i] for i in page],
                                    "has_more": start + limit < len(ids)})
        return self._send(404, {"error": {"type": "invalid_request_error", "code": "resource_missing"}})

    def do_POST(self):
        if self.path == "/v1/charges":
            body = self._body()
            if "amount" not in body:
                return self._send(400, {"error": {"type": "invalid_request_error", "param": "amount"}})
            cid = f"ch_{len(STORE) + 1}"
            STORE[cid] = {"id": cid, "amount": body["amount"], "status": "succeeded"}
            return self._send(201, STORE[cid])
        return self._send(404, {"error": {"type": "invalid_request_error"}})

    def log_message(self, *a):        # 关掉访问日志，别污染 stdout
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

测试里启动它：`threading.Thread(target=server.serve_forever, daemon=True).start()`，端口用 `0` 让系统分配，再从 `server.server_address[1]` 拿。

## 5. Integration 轮的做题顺序

1. **读文档 5 分钟**：列出端点、参数、响应结构、错误码、分页方式、限流规则。
2. 先写 `http()` 这一层薄封装（§2），**跑通一次最简单的 GET**。
3. 再写业务：分页 → 聚合 → 输出。
4. 再加健壮性：重试、超时、幂等键、错误分类。
5. 每一步都打印一条 stderr 日志（status、耗时），面试官在看你怎么调试。
6. 最后：把"我做了什么假设"（比如 has_more 的语义、429 的处理）说出来。

## 6. 练习

`exercises/ex06_http.py`（测试自带一个内存 mock server，不用联网）：
1. `http(method, url, body=None, headers=None, params=None, timeout=5.0)`（§2）。
2. `list_all(base, path, limit)`（§3.1）。
3. `with_retry(fn, attempts, base, sleep)`（§3.2）：429/5xx 重试，4xx 不重试，`Retry-After` 优先。
4. `create_charge_idempotent(base, amount, key)`：POST 带幂等键，用 `with_retry` 包起来，返回 body。

`python -m pytest test_ex06.py -q`

## 7. 自查

- [ ] 4xx 不重试，429/5xx 重试，重试要退避 + 抖动
- [ ] POST 重试前必须有幂等键，且重试复用同一个 key
- [ ] 分页终止条件写两个
- [ ] 每个请求有 timeout
- [ ] 能徒手写出 `urllib.request.Request` + `urlopen` + `HTTPError` 三件套
