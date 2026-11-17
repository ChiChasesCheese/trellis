"""关注演员与新片通知：修复练习。下面这份服务有几处缺陷，公开 API 与 `solution.py` 一致，
可以原样放进真实工作区的 `notification_service.py`。先让测试告诉你哪里坏了，再逐条修。

合同（每条都有测试）：
 1. 用户 id、演员 id、电影 id、片名都必须是 `str`，并且至少含一个"非空白"字符。空白字符只有这些：
    U+0009–000D、U+001C–0020、U+1680、U+2000–2006、U+2008–200A、U+2028–2029、U+205F、U+3000。
    U+00A0、U+0085、U+2007、U+202F 不在其中，算正常字符。字符串不裁剪、不改大小写。
 2. `actors` 只能是 `list`（`None`、元组、集合、生成器都不行），每个元素都合法；`[]` 合法；重复的 id 合并成集合。
 3. 非法输入抛 `ValueError("invalid_input")`，发生在碰任何状态之前，并且先于冲突判断。
 4. `follow` 记下一条（用户，演员）关系，已存在就什么都不做；`unfollow` 只删这一条，关系不存在也不报错；
    用户和演员不用先注册；关注不会补发关注之前登记的电影。
 5. 一部电影第一次 `add_movie(id, title, actors)` 返回 `True`；此刻关注了卡司里任意一位的用户，每人恰好收到一条
    `Notice(movie_id, title)`；没关注的人没有；卡司为空就没人收到。
 6. 同 id、同片名、同卡司集合再导入一次，返回 `False`，不发通知（即便之后有人新关注）；卡司的顺序和重复项不算差别。
 7. 同 id 但片名或卡司集合不同：抛 `RuntimeError("movie_conflict")`，状态原封不动。
 8. `inbox(user)` 按电影登记的先后给出全部通知（不是按 id 排序）；没见过的用户返回 `[]`；取关不收回已发的通知；
    返回值是副本，之后再怎么改它、再怎么导入，都不影响已拿到的列表；`Notice` 不可变。
 9. `actors` 在调用那一刻就被复制；调用方之后改自己的列表，服务里的卡司不变。
10. 所有方法可被多线程同时调用：同一部电影被并发导入，只有一次 `True`，其余 `False`，每个受众恰好一条通知；
    结果等价于某个串行顺序；校验或冲突失败不留下半截状态；不同实例互不影响。
11. 三个只读属性：`subscription_count`（现存关注关系数）、`tracked_actor_count`（至少有一个关注者的演员数）、
    `movie_count`（已登记电影数）。最后一个关注者走后，演员条目要消失，索引里不留空集合。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass

INVALID_INPUT = "invalid_input"
MOVIE_CONFLICT = "movie_conflict"


def _check_id(text):
    # 缺陷：str.strip() 的空白比合同多（U+00A0、U+0085 等也被吃掉）
    if not isinstance(text, str) or text.strip() == "":
        raise ValueError(INVALID_INPUT)


@dataclass(frozen=True)
class Notice:
    movie_id: str
    title: str


class NotificationService:
    def __init__(self):
        self._followers_of = {}  # 演员 -> 关注者集合
        self._films = {}  # 电影 id -> (片名, 卡司集合)
        self._mail = {}  # 用户 -> 通知列表
        self._mutex = threading.Lock()

    def follow(self, user, actor):
        _check_id(user)
        _check_id(actor)
        with self._mutex:
            self._followers_of.setdefault(actor, set()).add(user)

    def unfollow(self, user, actor):
        _check_id(user)
        _check_id(actor)
        with self._mutex:
            # 缺陷：取关写成了"再关注一次"，关系永远删不掉
            self._followers_of.setdefault(actor, set()).add(user)

    def add_movie(self, movie_id, title, actors):
        _check_id(movie_id)
        _check_id(title)
        if not isinstance(actors, list):
            raise ValueError(INVALID_INPUT)
        for name in actors:
            _check_id(name)
        cast = frozenset(actors)
        with self._mutex:
            if movie_id in self._films:
                # 缺陷：重复导入返回 True；同 id 内容不同也只是悄悄忽略，不抛冲突
                return True
            self._films[movie_id] = (title, cast)
            # 缺陷：要求关注者关注了卡司里的每一个人，而不是任意一个
            audience = None
            for name in cast:
                fans = self._followers_of.get(name, set())
                audience = set(fans) if audience is None else audience & fans
            for user in audience or ():
                self._mail.setdefault(user, []).append(Notice(movie_id, title))
            return True

    def inbox(self, user):
        _check_id(user)
        with self._mutex:
            # 缺陷：按电影 id 排序，丢了登记顺序
            return sorted(self._mail.get(user, []), key=lambda note: note.movie_id)

    @property
    def subscription_count(self):
        with self._mutex:
            return sum(len(users) for users in self._followers_of.values())

    @property
    def tracked_actor_count(self):
        with self._mutex:
            return len(self._followers_of)

    @property
    def movie_count(self):
        with self._mutex:
            return len(self._films)
