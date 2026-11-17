"""短链服务练习骨架。公开 API 与 `solution.py` 一致；`URLShortener` 与异常类可以原样放进真实工作区的 `shortener.py`，
`Api` 的各个方法就是 `app.py` 里各条 Flask 路由的函数体（工作区里用的是 `db.get_db()` 的共享连接，这里自己开一条 SQLite 连接）。

产品规则（逐条都有测试）：
 1. 创建 `create(long_url, custom_code=None, ttl_seconds=None)` 返回 `Link`；同一个网址可以缩多次，每次都是一条独立的链接，
    各有各的短码与 `owner_token`。`owner_token` 以 `tok_` 开头，至少 16 个字符，是随机的。
 2. `long_url` 必须是字符串；先去掉首尾空白，再要求：不含任何 ASCII 空白或控制字符（码点 ≤ 32 或 127）、协议是 `http` 或 `https`、
    主机名非空（端口若写了必须合法）。违反 → `ValidationError`。存的是去空白后的网址。
 3. `custom_code` 缺省或为 `None` 表示自动生成；否则必须完整匹配 `[A-Za-z0-9_-]{3,32}`（结尾多一个换行也不行），
    不是字符串（含 `True`、数字）或为空串都违反 → `ValidationError`。大小写敏感：`Abc` 与 `abc` 是两个短码。
 4. 自定义短码已被占用 → `ConflictError`；`links` 与 `stats` 两个词和路由重名，也按已占用处理。
 5. `ttl_seconds` 缺省或 `None` 表示永不过期；否则必须是不含 bool 的 int 或 float，有限且大于 0
    （NaN、±inf、0、负数、字符串、`True`、大到转不成浮点数的整数都违反 → `ValidationError`）。`expires_at = created_at + ttl_seconds`。
 6. 自动短码必须完整匹配 `[A-Za-z0-9]{6,10}`；每次创建最多调用五次 `_generate_code(long_url)`，每个自动短码恰好来自一次调用，
    都撞了现有短码 → `CodeGenerationError`；生成器返回了格式不合法的码 → 同样 `CodeGenerationError`。失败的创建不留任何记录。
 7. 过期的判断是 `expires_at` 非空且 `当前时间 >= expires_at`（恰好等于就算过期）。`Link.is_expired` 按这条快照被读出的时刻算。
 8. `get(short_code)`：不存在返回 `None`；过期的链接照样返回（`is_expired` 为真）。`Link.to_dict()` 只有六个键：
    `short_code, long_url, created_at, expires_at, hit_count, is_expired`，没有 `owner_token`。
 9. `resolve_redirect(short_code)`：不存在 → `NotFoundError`；过期 → `ExpiredLinkError`，且 `hit_count` 不变；
    否则恰好加一并返回原网址。并发的 100 次跳转，`hit_count` 恰好是 100；查过期与计数不能被别的请求插进来。
10. `increment_hits(short_code)`：不存在 → `NotFoundError`；存在就加一（不看过期）。
11. `delete(short_code, owner_token)`：令牌缺失、不是字符串或为空 → `ValidationError`（先于查短码）；短码不存在返回 `False`；
    令牌不对 → `PermissionDeniedError`，链接原样保留；令牌对 → 删除并返回 `True`。删除后 `get` 得到 `None`、不再计入统计，
    同一个自定义短码可以被重新创建，旧令牌对新链接无效。
12. `get_stats()`：`total_links`（未删除的链接数，过期的也算）、`total_hits`（点击总和，没有链接时是 0）、
    `top_5_links`（`short_code, long_url, hit_count`；先按 `hit_count` 降序，再按 `short_code` 升序，至多五条，没有链接时是空列表）。
13. HTTP：`POST /links` 成功 201，返回 `to_dict()` 的六个键加 `short_url`（请求的主机名 + `/` + 短码）与 `owner_token`；
    `GET /<code>` 成功 302 加 `Location`，过期 410，不存在 404；`GET /links/<code>` 返回六个键的元数据（不含 `owner_token`），不存在 404；
    `DELETE /links/<code>` 的请求体是 `{"owner_token": ...}`，成功 200 `{"deleted": code}`；`GET /stats` 200。
14. 状态码对应：`ValidationError` 400、`PermissionDeniedError` 403、`NotFoundError` 404、`ConflictError` 409、
    `ExpiredLinkError` 410、`CodeGenerationError` 500。请求体不是合法 JSON、或不是 JSON 对象 → 400；`DELETE` 没有请求体等同于没有令牌 → 400。
15. 每个错误响应都是 JSON，且只有一个键：`{"error": "<说明>"}`。路径存在但方法不对 → 405；路径不存在 → 404；末尾的 `/` 可有可无。
    `/stats` 和 `/links/<code>` 排在 `/<code>` 之前匹配。
16. 失败的操作什么都不留；同一个实例上的所有方法并发调用是安全的；两个实例（相当于两个进程）打开同一个数据库文件时计数也不丢。
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

MAX_GENERATION_ATTEMPTS = 5
AUTO_CODE_PATTERN_TEXT = r"[A-Za-z0-9]{6,10}"
CUSTOM_CODE_PATTERN_TEXT = r"[0-9A-Za-z_-]{3,32}"


class ShortenerError(Exception):
    pass


class ValidationError(ShortenerError):
    pass


class NotFoundError(ShortenerError):
    pass


class ConflictError(ShortenerError):
    pass


class ExpiredLinkError(ShortenerError):
    pass


class PermissionDeniedError(ShortenerError):
    pass


class CodeGenerationError(ShortenerError):
    pass


@dataclass(frozen=True)
class Link:
    short_code: str
    long_url: str
    created_at: float
    expires_at: float | None
    hit_count: int
    owner_token: str
    read_at: float | None = None  # 读出这份快照的时刻；缺省时 is_expired 用当前时间

    @property
    def is_expired(self) -> bool:
        raise NotImplementedError("expired when expires_at is not None and now >= expires_at")

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError("the six public keys, never owner_token")


class URLShortener:
    def __init__(self, db_path: str | None = None, *, clock: Callable[[], float] = time.time) -> None:
        self._db_path = db_path
        self._clock = clock
        self._init_db()

    def _init_db(self) -> None:
        raise NotImplementedError("open one shared connection and create the links table")

    def _generate_code(self, long_url: str) -> str:
        raise NotImplementedError("a random code matching [A-Za-z0-9]{6,10}")

    def _generate_owner_token(self) -> str:
        raise NotImplementedError("tok_ plus a random secret")

    def create(self, long_url: str, custom_code: str | None = None,
               ttl_seconds: float | None = None) -> Link:
        raise NotImplementedError("validate, insert once, retry automatic codes at most five times")

    def get(self, short_code: str) -> Link | None:
        raise NotImplementedError

    def resolve_redirect(self, short_code: str) -> str:
        raise NotImplementedError("count one hit only while the link is not expired, in one atomic step")

    def increment_hits(self, short_code: str) -> None:
        raise NotImplementedError

    def delete(self, short_code: str, owner_token: str) -> bool:
        raise NotImplementedError

    def get_stats(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True)
class Reply:
    status: int
    body: dict[str, Any]
    location: str | None = None


class Api:
    def __init__(self, service: URLShortener, base_url: str = "http://localhost:8080") -> None:
        self._service, self._base_url = service, base_url

    def create_link(self, body: object, base_url: str | None = None) -> Reply:
        raise NotImplementedError

    def redirect(self, short_code: str) -> Reply:
        raise NotImplementedError

    def get_link(self, short_code: str) -> Reply:
        raise NotImplementedError

    def delete_link(self, short_code: str, body: object) -> Reply:
        raise NotImplementedError

    def stats(self) -> Reply:
        raise NotImplementedError

    def handle(self, method: str, path: str, raw_body: bytes = b"") -> Reply:
        raise NotImplementedError("route table: static paths before /<code>; 405 vs 404")
