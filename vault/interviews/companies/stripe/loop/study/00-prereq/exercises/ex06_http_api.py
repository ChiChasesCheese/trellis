"""ex06 · HTTP 与 API —— 你的作答文件。纯标准库 urllib，不要 requests。
运行：python -m pytest test_ex06.py -q
"""
from __future__ import annotations

import time
from typing import Callable

# 你会用到：urllib.request（Request/urlopen）、urllib.error（HTTPError/URLError）、
# urllib.parse（urlencode）、json、random（抖动）—— 自己按需 import。

RETRYABLE = {429, 500, 502, 503, 504}


def build_query_url(url: str, params: dict) -> str:
    """把 params 拼到 url 的查询串上（urllib.parse.urlencode）；params 为空/None 时原样返回 url。"""
    # TODO
    return url + "?_todo_"


def fetch_text(url: str, *, timeout: float = 5.0) -> str:
    """裸 GET 读文本。注意：4xx/5xx 这里不吞——urlopen 会抛 urllib.error.HTTPError，
    不是返回一个"失败状态码"，调用方必须自己 try/except。一定要设 timeout。"""
    # TODO
    return ""


def fetch_to_file(url: str, dest_path: str, *, timeout: float = 5.0) -> int:
    """下载二进制内容写盘，返回写入的字节数。落盘要用 "wb"（二进制），不是 "w"。"""
    # TODO
    return 0


def http(
    method: str,
    url: str,
    *,
    body: dict | None = None,
    headers: dict | None = None,
    params: dict | None = None,
    timeout: float = 5.0,
) -> tuple[int, dict, dict]:
    """薄封装：发一次请求，返回 (status, headers, json_body)。
    和 fetch_text 不同——这里 4xx/5xx 要捕获 HTTPError 后当作普通返回值给回去（方便分页/重试
    这类调用方直接看 status，不用到处 try/except）。POST JSON 要设 Content-Type 头，
    body 用 json.dumps(...).encode()。timeout 必须传给 urlopen。"""
    # TODO
    return 0, {}, {}


def list_all(base: str, path: str, *, limit: int = 100) -> list[dict]:
    """游标分页拉全部数据：读 body["data"]，游标是最后一条的 id（starting_after）。
    终止条件要写两个：has_more 为假 或者 本页为空（防止死循环）。"""
    # TODO
    return []


def with_retry(
    fn: Callable[[], tuple[int, dict, dict]],
    *,
    attempts: int = 5,
    base: float = 0.2,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[int, dict, dict]:
    """对 429/5xx 做指数退避 + 抖动重试；4xx（400/401/403/404 等）直接返回，不重试。
    优先用 Retry-After 头决定等多久，没有的话用 base * 2**i + 抖动。最后一次尝试后
    不管结果如何都要返回。"""
    # TODO
    return 0, {}, {}


def create_charge_idempotent(base: str, amount: int, key: str) -> dict:
    """POST /v1/charges 创建一笔 charge，带 Idempotency-Key，外面套 with_retry。
    成功（2xx）返回 body；失败抛 RuntimeError(f"{status}: {body}")。"""
    # TODO
    return {}
