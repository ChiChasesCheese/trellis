"""ScreenShelf 私人片单修复：参考解。放进真实工作区时，另存为 `service.py`，并把本地的 `ServiceError` 换成
`from models import ServiceError`；`dispatch` 在真实工作区是固定文件，这里按它的行为重写了一份，好让第 6 条也能被测试。

产品规则（编号即测试编号，每一条都有测试）：

1. 输入：user 是适配器给的非空字符串，服务不再校验，也不做 strip，`"Ann"` 和 `"ann"` 是两个用户。
   name 必须是 `str`，`strip()` 之后长度 1..80（按 Unicode 字符计），存的是 strip 之后的值；不合格 `ServiceError(400, "invalid_name")`。
   movie_id 必须恰好是 `int`（bool 不算），范围 1..2147483647，否则 `(400, "invalid_movie")`；电影不需要出现在任何片库里。
   list_id 是 1..2**63-1 的整数，由适配器保证。
2. 创建、读取、改名：create 返回 `(201, {id, owner, name, movies: []})`；id 由 SQLite 自增，新库从 1 起，删除后也不复用；重名允许。
   get 返回同样的形状，movies 去重并升序；rename 返回 `(200, 更新后的片单)`；所有返回值都是新对象，改它不影响库里的数据。
3. 归属与校验顺序：一张片单只属于一个用户；get、rename、delete、add_movie、remove_movie 对「不存在」和「别人的」
   一律 `(404, "list_not_found")`，外人分不出这两种；新名字、电影 id 先于归属校验；被拒绝的操作什么都不改。
4. 成员与删除：add_movie 第一次插入返回 `(201, 更新后的片单)`，已经存在返回 `(200, 原样的片单)`；成员关系只属于这一张片单；
   remove_movie 只删指定的那一部，返回 `(204, None)`，不在其中是 `(404, "movie_not_found")`（先查片单、后查电影）；
   delete 只删这一张片单和它的成员，返回 `(204, None)`，再删一次是 `list_not_found`。
5. 持久化与连接：每个写操作返回之前提交；同一路径上的第二个服务实例立刻看得到；不同路径互不相干；
   close 释放连接且可重复调用；同一实例内的调用串行执行；不能用进程内存代替数据库。
6. HTTP：`POST /watchlists`、`GET|PATCH|DELETE /watchlists/{id}`、`POST /watchlists/{id}/movies`、`DELETE /watchlists/{id}/movies/{movie_id}`；
   请求头 `X-User-ID` 缺失或空白是 401 `unauthorized`；错误体是 `{"error": 代码}`；路径不合法或 list id 超出 64 位是 404 `not_found`；
   路径合法但方法不对是 405 `method_not_allowed`；请求体多了或少了键是 400 `invalid_input`；204 没有响应体。
"""

from __future__ import annotations

import re
import sqlite3
import threading
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

MAX_NAME = 80
MAX_MOVIE_ID = 2**31 - 1
MAX_LIST_ID = 2**63 - 1

SCHEMA = """
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


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def clean_name(name: object) -> str:
    """名字合法才返回 strip 之后的值：存进库里的就是这个，不是调用方传来的原样。"""
    if not isinstance(name, str):
        raise ServiceError(400, "invalid_name")
    trimmed = name.strip()
    if not 1 <= len(trimmed) <= MAX_NAME:
        raise ServiceError(400, "invalid_name")
    return trimmed


def check_movie(movie_id: object) -> int:
    """用 `type(...) is int` 挡住 bool：`True` 是 int 的子类，会被 isinstance 放行。"""
    if type(movie_id) is not int or not 1 <= movie_id <= MAX_MOVIE_ID:
        raise ServiceError(400, "invalid_movie")
    return movie_id


def list_missing() -> ServiceError:
    """「不存在」和「别人的」是同一个错误：每次新建，不共享异常对象。"""
    return ServiceError(404, "list_not_found")


@dataclass(frozen=True, slots=True)
class Watchlist:
    """一张片单读出来的快照：冻结的值，成员是元组，调用方拿不到库里的任何东西。"""

    id: int
    owner: str
    name: str
    movies: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "owner": self.owner, "name": self.name, "movies": list(self.movies)}


class ShelfStore:
    """SQLite 这一层：持有唯一的连接和锁，每条 SQL 都带着所有者条件，事务只在这里开关。"""

    def __init__(self, database_path: str) -> None:
        self._conn = sqlite3.connect(database_path, check_same_thread=False)
        self._conn.execute("PRAGMA foreign_keys = ON")  # 每个连接都要开：不开，级联删除就静默失效
        self._conn.executescript(SCHEMA)
        self._lock = threading.RLock()

    def close(self) -> None:
        with self._lock:
            self._conn.close()  # 关一个已关闭的连接什么也不做，所以 close 可以重复调用

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """持锁、立即取得写权限、成功就提交、任何异常都回滚。读后写的流程必须整个包在里面。"""
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield
            except BaseException:
                self._conn.rollback()
                raise
            self._conn.commit()

    def load(self, owner: str, list_id: int) -> Watchlist | None:
        """一条语句读出片单和它的成员：所有者条件在 WHERE 里，别人的片单就是读不到。"""
        with self._lock:
            rows = self._conn.execute(
                "SELECT s.id, s.owner, s.name, m.movie_id FROM watchlists AS s "
                "LEFT JOIN entries AS m ON m.list_id = s.id "
                "WHERE s.id = :shelf AND s.owner = :who ORDER BY m.movie_id",
                {"shelf": list_id, "who": owner},
            ).fetchall()
        if not rows:
            return None
        head = rows[0]
        return Watchlist(head[0], head[1], head[2], tuple(row[3] for row in rows if row[3] is not None))

    def owns(self, owner: str, list_id: int) -> bool:
        with self._lock:
            row = self._conn.execute(
                "SELECT 1 FROM watchlists WHERE id = :shelf AND owner = :who", {"shelf": list_id, "who": owner}
            ).fetchone()
        return row is not None

    def insert_list(self, owner: str, name: str) -> int:
        with self._lock:
            cursor = self._conn.execute("INSERT INTO watchlists (owner, name) VALUES (:who, :title)", {"who": owner, "title": name})
        assert cursor.lastrowid is not None  # 只为类型检查收窄；删掉这行不改变程序的保证
        return cursor.lastrowid

    def rename(self, owner: str, list_id: int, name: str) -> bool:
        with self._lock:
            cursor = self._conn.execute(
                "UPDATE watchlists SET name = :title WHERE id = :shelf AND owner = :who",
                {"title": name, "shelf": list_id, "who": owner},
            )
        return cursor.rowcount == 1

    def drop(self, owner: str, list_id: int) -> bool:
        """只删这一行；成员由外键的 ON DELETE CASCADE 带走。"""
        with self._lock:
            cursor = self._conn.execute("DELETE FROM watchlists WHERE id = :shelf AND owner = :who", {"shelf": list_id, "who": owner})
        return cursor.rowcount == 1

    def add_entry(self, list_id: int, movie_id: int) -> bool:
        """主键冲突才什么都不做（比 OR IGNORE 窄）；真的插入了返回 True，已经存在返回 False。"""
        with self._lock:
            cursor = self._conn.execute(
                "INSERT INTO entries (list_id, movie_id) VALUES (:shelf, :movie) "
                "ON CONFLICT (list_id, movie_id) DO NOTHING",
                {"shelf": list_id, "movie": movie_id},
            )
        return cursor.rowcount == 1

    def remove_entry(self, list_id: int, movie_id: int) -> bool:
        with self._lock:
            cursor = self._conn.execute(
                "DELETE FROM entries WHERE list_id = :shelf AND movie_id = :movie",
                {"shelf": list_id, "movie": movie_id},
            )
        return cursor.rowcount == 1

    def entry_count(self) -> int:
        with self._lock:
            return self._conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]


class WatchlistService:
    """校验输入、决定状态码、把写操作包进事务；不拼 SQL，也不保存任何随请求变化的状态。"""

    def __init__(self, database_path: str) -> None:
        self._store = ShelfStore(database_path)

    def close(self) -> None:
        self._store.close()

    @property
    def membership_count(self) -> int:
        """全库的成员行数：测试用它看出删除片单后成员是否真的被带走（API 看不到孤儿行）。"""
        return self._store.entry_count()

    def _snapshot(self, user: str, list_id: int) -> Watchlist:
        found = self._store.load(user, list_id)
        if found is None:
            raise list_missing()
        return found

    def get(self, user: str, list_id: int) -> dict[str, Any]:
        return self._snapshot(user, list_id).to_dict()

    def create(self, user: str, name: str) -> tuple[int, dict[str, Any]]:
        trimmed = clean_name(name)
        with self._store.transaction():
            new_id = self._store.insert_list(user, trimmed)
            return 201, self._snapshot(user, new_id).to_dict()

    def rename(self, user: str, list_id: int, name: str) -> tuple[int, dict[str, Any]]:
        trimmed = clean_name(name)  # 先校验名字，再看归属
        with self._store.transaction():
            if not self._store.rename(user, list_id, trimmed):
                raise list_missing()
            return 200, self._snapshot(user, list_id).to_dict()

    def delete(self, user: str, list_id: int) -> tuple[int, None]:
        with self._store.transaction():
            if not self._store.drop(user, list_id):
                raise list_missing()
        return 204, None

    def add_movie(self, user: str, list_id: int, movie_id: int) -> tuple[int, dict[str, Any]]:
        movie = check_movie(movie_id)
        with self._store.transaction():
            if not self._store.owns(user, list_id):
                raise list_missing()
            inserted = self._store.add_entry(list_id, movie)
            return (201 if inserted else 200), self._snapshot(user, list_id).to_dict()

    def remove_movie(self, user: str, list_id: int, movie_id: int) -> tuple[int, None]:
        movie = check_movie(movie_id)
        with self._store.transaction():
            if not self._store.owns(user, list_id):
                raise list_missing()
            if not self._store.remove_entry(list_id, movie):
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


if __name__ == "__main__":
    shelf = WatchlistService(":memory:")
    try:
        _, made = shelf.create("ann", "  Friday night  ")
        print(shelf.add_movie("ann", made["id"], 42))  # (201, ...)
        print(shelf.add_movie("ann", made["id"], 42))  # (200, ...)：同一部不会插第二次
        print(dispatch(shelf, "GET", f"/watchlists/{made['id']}", "ben"))  # (404, {'error': 'list_not_found'})
    finally:
        shelf.close()
