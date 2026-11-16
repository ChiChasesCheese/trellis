"""评论与回复练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `comment_service.py`。

产品规则（逐条都有测试）：
 1. 结构只有两层：帖子 → 评论 → 回复。回复属于一条评论，回复下面没有回复。
 2. `add_comment(post_id, user_id, content)` 返回字典 `{id, post_id, user_id, content, created_at, replies}`，
    新评论的 `replies` 是空列表。
 3. `add_reply(post_id, comment_id, user_id, content)` 返回字典 `{id, post_id, comment_id, user_id, content, created_at}`，
    没有 `replies` 键。
 4. `get_comments(post_id)` 返回该帖子的整串评论，每条评论带自己的 `replies`，形状与上面两个方法的返回一致；
    帖子存在但没有评论时返回 `[]`。
 5. `user_id` 与 `content` 必须是字符串，且 `str.strip()` 之后非空；`None`、数字、空串、纯空白都抛 `ValidationError`。
    `strip` 只用来判空：存进去、返回的都是调用方给的原值，首尾空白不去掉。
 6. 检查顺序固定：先校验 `user_id` 与 `content`，再查帖子，加回复时最后查评论。
    帖子不存在抛 `NotFoundError`；评论不存在、或存在但属于另一个帖子，也抛 `NotFoundError`。
 7. 评论 ID 与回复 ID 是两条独立的序列，各自从 1 开始递增，不按帖子分；失败的调用不消耗 ID。
 8. 顺序就是成功提交的顺序：评论按提交顺序返回，每条评论下的回复也是；后提交的 ID 更大。
    `created_at` 只是以秒为单位的浮点元数据，不能拿它排序。
 9. 帖子之间互不影响：一个帖子里的评论不会出现在另一个帖子里。
10. 返回值是快照：调用方随便改返回的字典或列表，服务内部状态都不变；读取同样不能把内部列表交出去。
11. 线程安全：并发调用下 ID 不重复、写入互不破坏；与写入同时进行的读取看到某一时刻的整串。
12. 时钟可以注入（返回秒的浮点数），默认 `time.time`，测试里没有 `sleep`。
13. 复杂度：加评论 O(1)；加回复不扫描全站；读取的代价与返回的评论加回复总数成正比。
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol, TypedDict

Clock = Callable[[], float]


class NotFoundError(Exception):
    """帖子或评论不存在。"""


class ValidationError(Exception):
    """`user_id` 或 `content` 不合法。"""


class PostStore(Protocol):
    def exists(self, post_id: int) -> bool: ...


class ReplyDict(TypedDict):
    id: int
    post_id: int
    comment_id: int
    user_id: str
    content: str
    created_at: float


class CommentDict(TypedDict):
    id: int
    post_id: int
    user_id: str
    content: str
    created_at: float
    replies: list[ReplyDict]


class CommentService:
    def __init__(self, post_store: PostStore, clock: Clock = time.time) -> None:
        self.post_store = post_store
        # TODO：在这里准备数据结构和锁。

    def add_comment(self, post_id: int, user_id: str, content: str) -> CommentDict:
        raise NotImplementedError

    def add_reply(self, post_id: int, comment_id: int, user_id: str, content: str) -> ReplyDict:
        raise NotImplementedError

    def get_comments(self, post_id: int) -> list[CommentDict]:
        raise NotImplementedError
