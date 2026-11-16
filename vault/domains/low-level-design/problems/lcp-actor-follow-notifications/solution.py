"""关注演员与新片通知（修复版），设计五行：

1. 关注关系只存一份反向索引"演员 -> 关注者集合"：新片上线时对卡司求并集，天然每人一份，也不必遍历全部用户。
2. 电影 id 对应一条冻结记录（片名、卡司集合）；重复导入拿新记录和旧记录比较：相同返回 False，不同抛冲突。
3. 一把锁罩住"判重、算受众、登记电影、写收件箱"；校验和冲突检查都在第一次写入之前，失败不留痕。
4. 收件箱按插入顺序追加冻结的 `Notice`，读取返回新列表；取关只动索引，不动历史。
5. 集合清空时立刻删除，关注索引的大小只和现存的关注关系成正比。
"""

from __future__ import annotations

import threading
from collections.abc import Iterable
from dataclasses import dataclass

INVALID_INPUT = "invalid_input"
MOVIE_CONFLICT = "movie_conflict"

# 合同逐个列出的"空白字符"：不能用 str.strip() / str.isspace()，它们还会把 U+0085、U+00A0、U+2007、U+202F 当成空白。
_BLANK_CHARS = frozenset(
    "\t\n\v\f\r\x1c\x1d\x1e\x1f  "
    "          "
    "   　"
)


def _valid(value: object) -> str:
    """合法的标识符：是 str，且至少有一个非空白字符。空串也是空白。"""
    if not isinstance(value, str) or all(ch in _BLANK_CHARS for ch in value):
        raise ValueError(INVALID_INPUT)
    return value


@dataclass(frozen=True)
class Notice:
    movie_id: str
    title: str


@dataclass(frozen=True)
class _Movie:
    """一部已登记的电影。卡司是集合：顺序和重复都不影响相等。"""

    title: str
    cast: frozenset[str]


class MovieCatalog:
    """电影登记表，"新电影／重复导入／冲突"只在这里判定。不带锁，由服务的锁保护。"""

    def __init__(self) -> None:
        self._movies: dict[str, _Movie] = {}

    def is_new(self, movie_id: str, movie: _Movie) -> bool:
        """只读判定：没见过返回 True；记录完全相同返回 False；同 id 不同内容抛冲突。不修改任何东西。"""
        known = self._movies.get(movie_id)
        if known is None:
            return True
        if known != movie:
            raise RuntimeError(MOVIE_CONFLICT)
        return False

    def add(self, movie_id: str, movie: _Movie) -> None:
        self._movies[movie_id] = movie

    def __len__(self) -> int:
        return len(self._movies)


class Subscriptions:
    """关注索引：演员 -> 关注者集合。不带锁，由服务的锁保护。"""

    def __init__(self) -> None:
        self._followers: dict[str, set[str]] = {}

    def follow(self, user: str, actor: str) -> None:
        self._followers.setdefault(actor, set()).add(user)

    def unfollow(self, user: str, actor: str) -> None:
        users = self._followers.get(actor)
        if users is None:
            return
        users.discard(user)
        if not users:
            del self._followers[actor]

    def audience(self, cast: Iterable[str]) -> set[str]:
        """关注了卡司中至少一人的用户，每人一次。"""
        users: set[str] = set()
        for actor in cast:
            users.update(self._followers.get(actor, ()))
        return users

    @property
    def edge_count(self) -> int:
        return sum(len(users) for users in self._followers.values())

    @property
    def actor_count(self) -> int:
        return len(self._followers)


class Inboxes:
    """每个用户一份按插入顺序追加的通知历史。不带锁，由服务的锁保护。"""

    def __init__(self) -> None:
        self._notices: dict[str, list[Notice]] = {}

    def deliver(self, users: Iterable[str], notice: Notice) -> None:
        for user in users:
            self._notices.setdefault(user, []).append(notice)

    def snapshot(self, user: str) -> list[Notice]:
        """新列表；`Notice` 本身是冻结的，所以调用方拿到的和内部状态互不影响。读不创建条目。"""
        return list(self._notices.get(user, ()))


class NotificationService:
    """所有公开方法都在同一把锁下执行：任意并发调用等价于某一个串行顺序（可线性化）。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._catalog = MovieCatalog()
        self._subscriptions = Subscriptions()
        self._inboxes = Inboxes()

    def follow(self, user: str, actor: str) -> None:
        _valid(user)
        _valid(actor)
        with self._lock:
            self._subscriptions.follow(user, actor)

    def unfollow(self, user: str, actor: str) -> None:
        _valid(user)
        _valid(actor)
        with self._lock:
            self._subscriptions.unfollow(user, actor)

    def add_movie(self, movie_id: str, title: str, actors: list[str]) -> bool:
        _valid(movie_id)
        _valid(title)
        if not isinstance(actors, list):
            raise ValueError(INVALID_INPUT)
        # 先把调用方的列表复制成不可变集合再校验：之后调用方怎么改它，校验过的内容都不变。
        cast = frozenset(_valid(actor) for actor in list(actors))
        movie = _Movie(title, cast)
        with self._lock:
            if not self._catalog.is_new(movie_id, movie):
                return False
            # 到这里不会再失败：先算出受众，再一并提交，电影和通知要么都在要么都不在。
            audience = self._subscriptions.audience(cast)
            self._catalog.add(movie_id, movie)
            self._inboxes.deliver(audience, Notice(movie_id, title))
            return True

    def inbox(self, user: str) -> list[Notice]:
        _valid(user)
        with self._lock:
            return self._inboxes.snapshot(user)

    @property
    def subscription_count(self) -> int:
        """现存的（用户，演员）关注关系个数。"""
        with self._lock:
            return self._subscriptions.edge_count

    @property
    def tracked_actor_count(self) -> int:
        """至少有一个关注者的演员个数：最后一个关注者取关后应当归零。"""
        with self._lock:
            return self._subscriptions.actor_count

    @property
    def movie_count(self) -> int:
        with self._lock:
            return len(self._catalog)


if __name__ == "__main__":
    service = NotificationService()
    service.follow("alice", "actor-1")
    service.follow("alice", "actor-2")
    service.follow("bob", "actor-2")
    print(service.add_movie("m1", "Opening Night", ["actor-1", "actor-2", "actor-1"]))
    print(service.add_movie("m1", "Opening Night", ["actor-2", "actor-1"]))
    print(service.inbox("alice"), service.inbox("bob"))
    try:
        service.add_movie("m1", "Another Title", ["actor-1"])
    except RuntimeError as exc:
        print("conflict:", exc)
