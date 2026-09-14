"""ex06 参考答案。纯标准库 urllib。"""
from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable

RETRYABLE = {429, 500, 502, 503, 504}


def build_query_url(url: str, params: dict) -> str:
    if not params:
        return url
    return f"{url}?{urllib.parse.urlencode(params)}"


def fetch_text(url: str, *, timeout: float = 5.0) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def fetch_to_file(url: str, dest_path: str, *, timeout: float = 5.0) -> int:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = resp.read()
    with open(dest_path, "wb") as f:
        f.write(data)
    return len(data)


def http(
    method: str,
    url: str,
    *,
    body: dict | None = None,
    headers: dict | None = None,
    params: dict | None = None,
    timeout: float = 5.0,
) -> tuple[int, dict, dict]:
    if params:
        url = build_query_url(url, params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, dict(resp.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:  # 4xx/5xx：也是 response 对象，e.code / e.read() 能读
        raw = e.read().decode("utf-8")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return e.code, dict(e.headers), parsed


def list_all(base: str, path: str, *, limit: int = 100) -> list[dict]:
    out: list[dict] = []
    cursor: str | None = None
    while True:
        params = {"limit": limit}
        if cursor:
            params["starting_after"] = cursor
        status, _, body = http("GET", base + path, params=params)
        if status != 200:
            raise RuntimeError(f"{status}: {body}")
        data = body.get("data", [])
        out.extend(data)
        if not body.get("has_more") or not data:
            return out
        cursor = data[-1]["id"]


def with_retry(
    fn: Callable[[], tuple[int, dict, dict]],
    *,
    attempts: int = 5,
    base: float = 0.2,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[int, dict, dict]:
    status, headers, body = 0, {}, {}
    for i in range(attempts):
        try:
            status, headers, body = fn()
        except (urllib.error.URLError, TimeoutError) as e:  # 网络错/超时也当可重试处理
            status, headers, body = 599, {}, {"error": str(e)}
        if status not in RETRYABLE or i == attempts - 1:
            return status, headers, body
        retry_after = headers.get("Retry-After") if headers else None
        delay = float(retry_after) if retry_after else base * (2**i) + random.uniform(0, base)
        sleep(delay)
    return status, headers, body


def create_charge_idempotent(base: str, amount: int, key: str) -> dict:
    status, _, body = with_retry(
        lambda: http("POST", base + "/v1/charges", body={"amount": amount}, headers={"Idempotency-Key": key})
    )
    if status not in (200, 201):
        raise RuntimeError(f"{status}: {body}")
    return body
