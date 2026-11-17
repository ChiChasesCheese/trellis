"""短链服务（URL Shortener）：SQLite 存储，严格校验，一条带条件的 UPDATE 同时完成"查过期 + 计一次点击"。
设计：`URLShortener` 是服务层，唯一的真相在 `links` 表里（主键 `short_code` 负责唯一性，不先查再插）；
每个会改数据的操作都在 `_tx()` 里运行——同一把锁串行化共享的那条连接，`BEGIN IMMEDIATE` 再把多条语句并成一次提交；
`_clean_*` 三个函数是边界校验，先于任何数据库访问；`Link` 是只读快照，`is_expired` 按读取那一刻判断；
`Api` 把服务的异常翻成 HTTP 状态码与 `{"error": ...}`，`handle` 是一个只有五条路由的最小路由器（真实工作区里换成 Flask 路由）。
"""

from __future__ import annotations

import json
import math
import os
import re
import secrets
import sqlite3
import string
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import urlsplit

AUTO_CODE_PATTERN = re.compile(r"[A-Za-z0-9]{6,10}")  # 一律 fullmatch：`$` 会放过结尾的换行
CUSTOM_CODE_RE = re.compile(r"[0-9A-Za-z_-]{3,32}")
MAX_GENERATION_ATTEMPTS = 5
LOCK_WAIT_MS = 5000
CODE_LENGTH = 7
ALPHABET = string.ascii_letters + string.digits
RESERVED_CODES = frozenset({"links", "stats"})  # `stats` 被统计路由接走，永远跳转不到；`links` 其实能跳转，也保守地拒绝
COLUMNS = "short_code, long_url, created_at, expires_at, hit_count, owner_token"


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
    """一条短链在 `read_at` 那一刻的快照。`is_expired` 随快照走，不随调用 `is_expired` 的时间走。"""

    short_code: str
    long_url: str
    created_at: float
    expires_at: float | None
    hit_count: int
    owner_token: str
    read_at: float | None = None

    @property
    def is_expired(self) -> bool:
        now = time.time() if self.read_at is None else self.read_at
        return self.expires_at is not None and now >= self.expires_at

    def to_dict(self) -> dict[str, Any]:
        """公开的元数据：没有 owner_token，也没有 short_url（后者取决于请求的主机名，由 Api 加）。"""
        return {"short_code": self.short_code, "long_url": self.long_url, "created_at": self.created_at,
                "expires_at": self.expires_at, "hit_count": self.hit_count, "is_expired": self.is_expired}


def _clean_url(value: object) -> str:
    if not isinstance(value, str):
        raise ValidationError("long_url must be a string")
    url = value.strip()
    if any(ord(ch) <= 32 or ord(ch) == 127 for ch in url):  # 查原字符串：urlsplit 会悄悄删掉 \t \r \n，解析结果里查不到
        raise ValidationError("long_url must not contain whitespace or control characters")
    try:
        parts = urlsplit(url)
        parts.port  # 端口非法时这里才抛 ValueError
    except ValueError:
        raise ValidationError("long_url is not a valid URL") from None
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValidationError("long_url must be an http(s) URL with a host")
    return url


def _clean_code(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not CUSTOM_CODE_RE.fullmatch(value):
        raise ValidationError("custom_code must match [A-Za-z0-9_-]{3,32}")
    return value


def _clean_ttl(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):  # True 是 int，要显式排除
        raise ValidationError("ttl_seconds must be a number")
    try:
        ttl = float(value)
    except OverflowError:  # 10**400 这样的整数转不成 float
        raise ValidationError("ttl_seconds is too large") from None
    if not math.isfinite(ttl) or ttl <= 0:  # NaN 与 ±inf 不是"正的有限数"
        raise ValidationError("ttl_seconds must be a positive finite number")
    return ttl


class URLShortener:
    """SQLite 后端的短链服务。一个实例一条连接，连接在线程间共享，所以所有语句都在 `_tx()` 里串行执行。"""

    def __init__(self, db_path: str | None = None, *, clock: Callable[[], float] = time.time) -> None:
        self._db_path = db_path
        self._clock = clock
        self._lock = threading.RLock()
        self._conn = self._open()
        self._init_db()

    def _open(self) -> sqlite3.Connection:
        path = self._db_path or os.environ.get("URL_SHORTENER_DB_PATH") or "shortener.db"
        conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # 自己管事务
        settings = [f"busy_timeout = {LOCK_WAIT_MS}"]  # 另一个进程占着写锁时最多等这么久，不立刻报错
        if path != ":memory:":
            settings.append("journal_mode = WAL")  # 读不挡写
        for setting in settings:
            conn.execute("PRAGMA " + setting)
        return conn

    def _init_db(self) -> None:
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS links ("
            " short_code TEXT PRIMARY KEY,"  # 唯一性由数据库保证
            " long_url TEXT NOT NULL,"
            " created_at REAL NOT NULL,"
            " expires_at REAL,"
            " hit_count INTEGER NOT NULL DEFAULT 0 CHECK (hit_count >= 0),"
            " owner_token TEXT NOT NULL)")

    @contextmanager
    def _tx(self, write: bool = True) -> Iterator[sqlite3.Connection]:
        """锁住连接并开一个事务：正常退出就提交，抛异常就回滚，所以失败的操作不留痕。"""
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            try:
                yield self._conn
            except BaseException:
                self._conn.execute("ROLLBACK")
                raise
            self._conn.execute("COMMIT")

    def _generate_code(self, long_url: str) -> str:
        """随机而不是由 URL 推出来：同一个网址再缩一次必须得到另一条链接。"""
        return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))

    def _generate_owner_token(self) -> str:
        return "tok_" + secrets.token_urlsafe(16)

    def _insert(self, conn: sqlite3.Connection, link: Link) -> bool:
        try:
            conn.execute("INSERT INTO links (" + COLUMNS + ") VALUES (?, ?, ?, ?, 0, ?)",
                         (link.short_code, link.long_url, link.created_at, link.expires_at, link.owner_token))
        except sqlite3.IntegrityError:  # 这张表唯一会违反的约束就是主键：短码已被占用
            return False
        return True

    def create(self, long_url: str, custom_code: str | None = None,
               ttl_seconds: float | None = None) -> Link:
        url, code, ttl = _clean_url(long_url), _clean_code(custom_code), _clean_ttl(ttl_seconds)
        with self._tx() as conn:
            created = self._clock()
            draft = Link("", url, created, None if ttl is None else created + ttl, 0,
                         self._generate_owner_token(), created)
            if code is not None:
                link = replace(draft, short_code=code)
                if code in RESERVED_CODES or not self._insert(conn, link):
                    raise ConflictError("custom_code is already in use")
                return link
            for _ in range(MAX_GENERATION_ATTEMPTS):  # 至多五次，每次恰好调用一次 _generate_code
                candidate = self._generate_code(url)
                if not isinstance(candidate, str) or not AUTO_CODE_PATTERN.fullmatch(candidate):
                    raise CodeGenerationError("the generator returned an invalid code")
                link = replace(draft, short_code=candidate)
                if self._insert(conn, link):
                    return link
            raise CodeGenerationError("could not find a free short code")

    def get(self, short_code: str) -> Link | None:
        with self._tx(write=False) as conn:
            row = conn.execute("SELECT " + COLUMNS + " FROM links WHERE short_code = ?",
                               (short_code,)).fetchone() if isinstance(short_code, str) else None
            return None if row is None else Link(*row, read_at=self._clock())

    def resolve_redirect(self, short_code: str) -> str:
        with self._tx() as conn:
            now = self._clock()
            hit = conn.execute(  # 过期判断和计数在同一条语句里：不会出现"判断时没过期、计数时已过期"
                "UPDATE links SET hit_count = hit_count + 1"
                " WHERE short_code = ? AND (expires_at IS NULL OR ? < expires_at)", (short_code, now))
            if hit.rowcount == 1:
                return conn.execute("SELECT long_url FROM links WHERE short_code = ?", (short_code,)).fetchone()[0]
            exists = conn.execute("SELECT 1 FROM links WHERE short_code = ?", (short_code,)).fetchone()
        if exists:
            raise ExpiredLinkError("the link has expired")
        raise NotFoundError("unknown short code")

    def increment_hits(self, short_code: str) -> None:
        """给已存在的短码加一次点击（不看过期：过期判断是跳转的规则，不是计数的规则）。"""
        with self._tx() as conn:
            done = conn.execute("UPDATE links SET hit_count = hit_count + 1 WHERE short_code = ?", (short_code,))
            if done.rowcount == 0:
                raise NotFoundError("unknown short code")

    def delete(self, short_code: str, owner_token: str) -> bool:
        if not isinstance(owner_token, str) or not owner_token:  # 先校验令牌的形状：缺令牌是 400，不管短码在不在
            raise ValidationError("owner_token is required")
        with self._tx() as conn:
            row = conn.execute("SELECT owner_token FROM links WHERE short_code = ?", (short_code,)).fetchone()
            if row is None:
                return False
            if not secrets.compare_digest(row[0].encode(), owner_token.encode()):  # 常数时间比较
                raise PermissionDeniedError("owner_token does not match")
            conn.execute("DELETE FROM links WHERE short_code = ?", (short_code,))
            return True

    def get_stats(self) -> dict[str, Any]:
        with self._tx(write=False) as conn:  # 两条查询在同一个读事务里，看到的是同一时刻的数据
            total, hits = conn.execute("SELECT COUNT(*), COALESCE(SUM(hit_count), 0) FROM links").fetchone()
            top = conn.execute("SELECT short_code, long_url, hit_count FROM links"
                               " ORDER BY hit_count DESC, short_code ASC LIMIT 5").fetchall()
        return {"total_links": total, "total_hits": hits,
                "top_5_links": [{"short_code": c, "long_url": u, "hit_count": h} for c, u, h in top]}


@dataclass(frozen=True)
class Reply:
    status: int
    body: dict[str, Any]
    location: str | None = None


_STATUS = ((ValidationError, 400), (PermissionDeniedError, 403), (NotFoundError, 404), (ConflictError, 409),
           (ExpiredLinkError, 410), (CodeGenerationError, 500))


def _error(status: int, message: str) -> Reply:
    return Reply(status, {"error": message})


class Api:
    """HTTP 合同：解析请求体、调用服务、把异常翻成状态码。真实工作区里这些方法就是 Flask 路由的函数体。"""

    def __init__(self, service: URLShortener, base_url: str = "http://localhost:8080") -> None:
        self._service, self._base_url = service, base_url

    def _call(self, action: Callable[[], Reply]) -> Reply:
        try:
            return action()
        except ShortenerError as exc:
            status = next(code for kind, code in _STATUS if isinstance(exc, kind))
            return _error(status, str(exc))

    def create_link(self, body: object, base_url: str | None = None) -> Reply:
        if not isinstance(body, dict):
            return _error(400, "request body must be a JSON object")

        def go() -> Reply:
            link = self._service.create(body.get("long_url"), body.get("custom_code"), body.get("ttl_seconds"))
            root = (base_url or self._base_url).rstrip("/")
            return Reply(201, {**link.to_dict(), "short_url": f"{root}/{link.short_code}",
                               "owner_token": link.owner_token})
        return self._call(go)

    def redirect(self, short_code: str) -> Reply:
        def go() -> Reply:
            return Reply(302, {}, self._service.resolve_redirect(short_code))
        return self._call(go)

    def get_link(self, short_code: str) -> Reply:
        link = self._service.get(short_code)
        return _error(404, "unknown short code") if link is None else Reply(200, link.to_dict())

    def delete_link(self, short_code: str, body: object) -> Reply:
        token = body.get("owner_token") if isinstance(body, dict) else None  # 没有请求体和没有令牌是同一种错
        def go() -> Reply:
            if not self._service.delete(short_code, token):
                return _error(404, "unknown short code")
            return Reply(200, {"deleted": short_code})
        return self._call(go)

    def stats(self) -> Reply:
        return Reply(200, self._service.get_stats())

    def handle(self, method: str, path: str, raw_body: bytes = b"") -> Reply:
        """最小路由器：静态路由排在 `/<code>` 前面；路径对得上但方法不对是 405，路径对不上是 404。"""
        try:
            body: object = json.loads(raw_body) if raw_body else None
        except ValueError:  # 含 UnicodeDecodeError
            body = None
        path = path.rstrip("/") or "/"
        routes: list[tuple[str, str, Callable[[re.Match[str]], Reply]]] = [
            ("POST", r"/links", lambda m: self.create_link(body)),
            ("GET", r"/stats", lambda m: self.stats()),
            ("GET", r"/links/([^/]+)", lambda m: self.get_link(m[1])),
            ("DELETE", r"/links/([^/]+)", lambda m: self.delete_link(m[1], body)),
            ("GET", r"/([^/]+)", lambda m: self.redirect(m[1])),
        ]
        matched = False
        for verb, pattern, action in routes:
            found = re.fullmatch(pattern, path)
            matched = matched or found is not None
            if found and verb == method:
                return action(found)
        return _error(405, "method not allowed") if matched else _error(404, "not found")


if __name__ == "__main__":
    api = Api(URLShortener(":memory:"))
    made = api.handle("POST", "/links", b'{"long_url": "https://example.com/a", "custom_code": "demo"}')
    print(made.status, made.body)
    print(api.handle("GET", "/demo"))
    print(api.handle("GET", "/stats").body)
