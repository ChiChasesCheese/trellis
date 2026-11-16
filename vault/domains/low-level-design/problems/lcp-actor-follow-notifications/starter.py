"""关注演员与新片通知：修复练习。下面这份服务有几处缺陷，公开 API 与 `solution.py` 一致，
可以原样放进真实工作区的 `notification_service.py`。先让测试告诉你哪里坏了，再逐条修。

产品规则（逐条都有测试）：
 1. 所有 id 和片名必须是 `str`，且不能是"空白"：空串，或只含 U+0009–000D、U+001C–0020、U+1680、
    U+2000–2006、U+2008–200A、U+2028–2029、U+205F、U+3000 的串。其他字符（包括 U+00A0、U+0085、
    U+2007、U+202F）都是合法字符。字符串原样保存，区分大小写，首尾空白不去掉。
 2. `actors` 必须是 `list`（不能是 `None`、元组、生成器），元素逐个合法；空列表合法；重复的演员 id 当集合处理。
 3. 非法输入抛 `ValueError("invalid_input")`，发生在动任何状态之前；校验先于冲突检查。
 4. `follow` 加一条（用户，演员）关系，重复关注无事发生；`unfollow` 只删这一条，关系或用户不存在也无事发生；
    用户和演员不需要注册；关注不会回填关注之前已登记的电影。
 5. 第一次 `add_movie(id, title, actors)` 登记电影并返回 `True`；在登记那一刻关注了卡司中至少一人的每个用户，
    恰好收到一条 `Notice(movie_id, title)`（关注多个卡司成员、卡司里有重复 id 都只收一条）；其余用户没有；卡司为空没人收到。
 6. 同 id、同片名、卡司集合相等的重复导入返回 `False`，不产生通知（哪怕关注者变了）；卡司顺序和重复不影响相等。
 7. 同 id 但片名不同或卡司集合不同：抛 `RuntimeError("movie_conflict")`，什么都不改。
 8. `inbox(user)` 按电影成功登记的先后顺序返回全部通知（不是按 id 排序）；未知用户得到空列表；取关不删历史通知；
    返回的列表是副本：调用方改它、之后的导入，都不影响已经拿到的结果；`Notice` 不可变。
 9. 入参 `actors` 在调用时就复制：之后调用方改自己的列表，不影响服务里已登记的卡司。
10. 所有方法可以被多个线程同时调用；同一部电影被并发导入多次，恰好一次 `True`，其余 `False`，每个受众恰好一条通知；
    并发调用等价于某个串行顺序；校验或冲突失败不留半截状态；不同实例互相独立。
11. 只读属性 `subscription_count`（现存关注关系个数）、`tracked_actor_count`（至少有一个关注者的演员个数）、
    `movie_count`（已登记电影数）：取关到没人关注时，索引里不留空集合。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass

INVALID_INPUT = "invalid_input"
MOVIE_CONFLICT = "movie_conflict"


def _valid(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(INVALID_INPUT)


@dataclass(frozen=True)
class Notice:
    movie_id: str
    title: str


class NotificationService:
    def __init__(self):
        self._follows = {}
        self._movies = {}
        self._inboxes = {}
        self._lock = threading.RLock()

    def follow(self, user, actor):
        _valid(user)
        _valid(actor)
        with self._lock:
            self._follows.setdefault(user, set()).add(actor)

    def unfollow(self, user, actor):
        _valid(user)
        _valid(actor)
        with self._lock:
            self._follows.setdefault(user, set()).add(actor)

    def add_movie(self, movie_id, title, actors):
        _valid(movie_id)
        _valid(title)
        if not isinstance(actors, list):
            raise ValueError(INVALID_INPUT)
        for actor in actors:
            _valid(actor)
        incoming = (title, frozenset(actors))
        with self._lock:
            if movie_id in self._movies:
                if self._movies[movie_id] != incoming:
                    return False
                return True
            self._movies[movie_id] = incoming
            for user, follows in self._follows.items():
                if incoming[1] <= follows:
                    self._inboxes.setdefault(user, []).append(Notice(movie_id, title))
            return True

    def inbox(self, user):
        _valid(user)
        with self._lock:
            return sorted(self._inboxes.get(user, []), key=lambda notice: notice.movie_id)

    @property
    def subscription_count(self):
        with self._lock:
            return sum(len(actors) for actors in self._follows.values())

    @property
    def tracked_actor_count(self):
        with self._lock:
            return len(set().union(*self._follows.values()))

    @property
    def movie_count(self):
        with self._lock:
            return len(self._movies)
