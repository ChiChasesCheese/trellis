"""ScreenShelf 私人片单服务（待修复）。公开 API 与 `solution.py` 一致；放进真实工作区时，另存为 `service.py`，
并把 `ServiceError` 换成 `from models import ServiceError`。

这份代码能跑，却会让两个用户互相看到对方的片单、重复添加也报 201、删除一张片单会连带删光别人的、移除一部电影会删掉
同一张片单里的其他电影：它就是要你修的东西。规则（每一条都有测试）：

1. 输入：user 是适配器给的非空字符串，不 strip，大小写敏感。name 必须是 `str`，`strip()` 之后长度 1..80（按 Unicode 字符计），
   存的是 strip 之后的值；不合格 `ServiceError(400, "invalid_name")`。movie_id 必须恰好是 `int`（bool 不算），范围 1..2147483647，
   否则 `(400, "invalid_movie")`；电影不需要出现在任何片库里。list_id 是 1..2**63-1 的整数。
2. create 返回 `(201, {id, owner, name, movies: []})`；id 由 SQLite 自增，新库从 1 起，删除后不复用；重名允许。
   get 同样的形状，movies 去重并升序；rename 返回 `(200, 更新后的片单)`；返回值是新对象，改它不影响库里的数据。
3. 一张片单只属于一个用户；get、rename、delete、add_movie、remove_movie 对「不存在」和「别人的」一律 `(404, "list_not_found")`；
   新名字、电影 id 先于归属校验；被拒绝的操作什么都不改。
4. add_movie 第一次插入返回 `(201, 更新后的片单)`，已经存在返回 `(200, 原样的片单)`；成员关系只属于这一张片单。
   remove_movie 只删指定的那一部，返回 `(204, None)`，不在其中是 `(404, "movie_not_found")`（先查片单、后查电影）。
   delete 只删这一张片单和它的成员，返回 `(204, None)`，再删一次是 `list_not_found`。
5. 每个写操作返回之前提交；同一路径上的第二个服务实例立刻看得到；不同路径互不相干；close 释放连接且可重复调用；
   同一实例内的调用串行执行；不能用进程内存代替数据库。
6. HTTP 适配器是固定的（下面的 `dispatch` 已经写好，不用改）。

Python 3.11，只用标准库。
"""

from __future__ import annotations

import re
import sqlite3
import threading
from collections.abc import Mapping
from typing import Any

MAX_NAME = 80
MAX_MOVIE_ID = 2**31 - 1
MAX_LIST_ID = 2**63 - 1


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


class WatchlistService:
    def __init__(self, database_path: str) -> None:
        self._conn = sqlite3.connect(database_path, check_same_thread=False)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS watchlists (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                name  TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS entries (
                list_id  INTEGER NOT NULL REFERENCES watchlists (id) ON DELETE CASCADE,
                movie_id INTEGER NOT NULL,
                PRIMARY KEY (list_id, movie_id)
            );
            """
        )
        self._guard = threading.RLock()

    def close(self) -> None:
        with self._guard:
            self._conn.close()

    @property
    def membership_count(self) -> int:
        with self._guard:
            return self._conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]

    def _clean(self, name: object) -> str:
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= MAX_NAME:
            raise ServiceError(400, "invalid_name")
        return name

    def _check_movie(self, movie_id: object) -> int:
        if type(movie_id) is not int or not 1 <= movie_id <= MAX_MOVIE_ID:
            raise ServiceError(400, "invalid_movie")
        return movie_id

    def _fetch(self, user: str, list_id: int) -> dict[str, Any]:
        head = self._conn.execute("SELECT id, owner, name FROM watchlists WHERE id = :id", {"id": list_id}).fetchone()
        if head is None:
            raise ServiceError(404, "list_not_found")
        movies = self._conn.execute(
            "SELECT movie_id FROM entries WHERE list_id = :id ORDER BY movie_id", {"id": list_id}
        ).fetchall()
        return {"id": head[0], "owner": head[1], "name": head[2], "movies": [row[0] for row in movies]}

    def get(self, user: str, list_id: int) -> dict[str, Any]:
        with self._guard:
            return self._fetch(user, list_id)

    def create(self, user: str, name: str) -> tuple[int, dict[str, Any]]:
        name = self._clean(name)
        with self._guard, self._conn:
            made = self._conn.execute("INSERT INTO watchlists (owner, name) VALUES (:who, :title)", {"who": user, "title": name})
            return 201, self._fetch(user, made.lastrowid)

    def rename(self, user: str, list_id: int, name: str) -> tuple[int, dict[str, Any]]:
        name = self._clean(name)
        with self._guard, self._conn:
            self._fetch(user, list_id)
            self._conn.execute("UPDATE watchlists SET name = :title WHERE id = :id", {"title": name, "id": list_id})
            return 200, self._fetch(user, list_id)

    def delete(self, user: str, list_id: int) -> tuple[int, None]:
        with self._guard, self._conn:
            self._fetch(user, list_id)
            self._conn.execute("DELETE FROM watchlists WHERE id != :id", {"id": list_id})
            return 204, None

    def add_movie(self, user: str, list_id: int, movie_id: int) -> tuple[int, dict[str, Any]]:
        movie = self._check_movie(movie_id)
        with self._guard, self._conn:
            self._fetch(user, list_id)
            self._conn.execute(
                "INSERT OR IGNORE INTO entries (list_id, movie_id) VALUES (:id, :movie)", {"id": list_id, "movie": movie}
            )
            return 201, self._fetch(user, list_id)

    def remove_movie(self, user: str, list_id: int, movie_id: int) -> tuple[int, None]:
        movie = self._check_movie(movie_id)
        with self._guard, self._conn:
            self._fetch(user, list_id)
            gone = self._conn.execute(
                "DELETE FROM entries WHERE list_id = :id AND movie_id != :movie", {"id": list_id, "movie": movie}
            )
            if gone.rowcount == 0:
                raise ServiceError(404, "movie_not_found")
            return 204, None


ID_DIGITS = r"[1-9][0-9]*"  # 不允许前导零，也不允许 0
ROUTE = re.compile(rf"/watchlists(?:/({ID_DIGITS})(?:/(movies)(?:/({ID_DIGITS}))?)?)?")


def error_reply(status: int, code: str) -> tuple[int, dict[str, str]]:
    return status, {"error": code}


def has_only(body: object, key: str) -> bool:
    return isinstance(body, dict) and set(body) == {key}


def dispatch(
    service: WatchlistService,
    method: str,
    path: str,
    user: str | None,
    body: object = None,
    query: Mapping[str, str] | None = None,
    key: str | None = None,
) -> tuple[int, Any]:
    """HTTP 适配器：先看用户，再看路径，再看方法与请求体，最后才调服务。"""
    if not isinstance(user, str) or not user.strip():
        return error_reply(401, "unauthorized")
    found = ROUTE.fullmatch(path)
    if found is None:
        return error_reply(404, "not_found")
    raw_list, tail, raw_movie = found.groups()
    if raw_list is not None and (len(raw_list) > 19 or int(raw_list) > MAX_LIST_ID):
        return error_reply(404, "not_found")  # 先比长度再转换：避免把超长数字串变成整数
    list_id = int(raw_list) if raw_list is not None else 0
    shape = (method, raw_list is not None, tail is not None, raw_movie is not None)
    try:
        if shape == ("POST", False, False, False):
            return service.create(user, body["name"]) if has_only(body, "name") else error_reply(400, "invalid_input")
        if shape == ("GET", True, False, False):
            return 200, service.get(user, list_id)
        if shape == ("PATCH", True, False, False):
            return service.rename(user, list_id, body["name"]) if has_only(body, "name") else error_reply(400, "invalid_input")
        if shape == ("DELETE", True, False, False):
            return service.delete(user, list_id)
        if shape == ("POST", True, True, False):
            if not has_only(body, "movie_id"):
                return error_reply(400, "invalid_input")
            return service.add_movie(user, list_id, body["movie_id"])  # type: ignore[index]
        if shape == ("DELETE", True, True, True):
            if len(raw_movie) > 10 or int(raw_movie) > MAX_MOVIE_ID:
                return error_reply(400, "invalid_movie")
            return service.remove_movie(user, list_id, int(raw_movie))
        return error_reply(405, "method_not_allowed")
    except ServiceError as failure:
        return error_reply(failure.status, failure.code)
