"""评论与回复（Comments & Replies）：帖子 → 评论 → 回复两级结构的进程内服务。
设计：每个帖子一个 `Thread`，评论按提交顺序存在以评论 ID 为键的 dict 里，状态按帖子天然隔离；
回复是不可变的 `Reply`，挂在所属评论的列表里；评论 ID 与回复 ID 是两条独立的全局递增序列；
文本校验与帖子检查在锁外，锁里只做"读时钟 → 分配 ID → 追加"这一小段，ID 在所有检查之后才分配；
对外只给每次新建的字典与列表（快照），内部对象永不出门；读取也在锁里，看到的是某一时刻的整串。
"""

from __future__ import annotations

import itertools
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, TypedDict, TypeGuard

Clock = Callable[[], float]
"""时钟：返回以秒为单位的浮点时间；生产用 `time.time`，测试注入假时钟。"""


class NotFoundError(Exception):
    """帖子或评论不存在（评论存在但属于别的帖子，也算不存在）。"""


class ValidationError(Exception):
    """`user_id` 或 `content` 不是字符串，或去掉首尾空白后为空。"""


class PostStore(Protocol):
    """服务只需要帖子仓库回答一个问题：这个帖子在不在。"""

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


def _require_text(value: object, field_name: str) -> None:
    """必须是字符串且去空白后非空；`strip` 只用来判空，存进去的仍是原值。"""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a string with at least one non-whitespace character")


def _is_id(value: object) -> TypeGuard[int]:
    """ID 是真正的整数；`True` 虽然等于 1，却不是 ID。"""
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class Reply:
    """一条回复。不可变：一旦提交就不会再变，所以快照可以直接共享它。"""

    id: int
    post_id: int
    comment_id: int
    user_id: str
    content: str
    created_at: float

    def to_dict(self) -> ReplyDict:
        return {
            "id": self.id,
            "post_id": self.post_id,
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
        }


@dataclass(slots=True)
class Comment:
    """一条评论和它的回复（按提交顺序）。唯一会变的是 `replies`，且只会在末尾追加。"""

    id: int
    post_id: int
    user_id: str
    content: str
    created_at: float
    replies: list[Reply] = field(default_factory=list)

    def to_dict(self) -> CommentDict:
        """每次都新建字典和列表；值只有字符串与数字，一层拷贝就够。"""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "replies": [reply.to_dict() for reply in self.replies],
        }


class Thread:
    """一个帖子下的全部评论。不变量：dict 的插入顺序就是提交顺序，也就是 ID 升序。"""

    def __init__(self) -> None:
        self._comments: dict[int, Comment] = {}

    def append(self, comment: Comment) -> None:
        self._comments[comment.id] = comment

    def find(self, comment_id: object) -> Comment | None:
        """按 ID 直接取，不扫描；别的帖子的评论不在这个 dict 里，所以天然取不到。"""
        return self._comments.get(comment_id) if _is_id(comment_id) else None

    def snapshot(self) -> list[CommentDict]:
        return [comment.to_dict() for comment in self._comments.values()]


class CommentService:
    """评论服务。一把锁保护所有可变状态；公开方法返回的都是新对象。"""

    def __init__(self, post_store: PostStore, clock: Clock = time.time) -> None:
        self.post_store = post_store
        self._clock = clock
        self._lock = threading.Lock()
        self._threads: dict[int, Thread] = {}
        self._comment_ids = itertools.count(1)
        self._reply_ids = itertools.count(1)

    def add_comment(self, post_id: int, user_id: str, content: str) -> CommentDict:
        """先校验文本，再查帖子；都通过之后才进锁、读时钟、分配 ID。"""
        _require_text(user_id, "user_id")
        _require_text(content, "content")
        self._require_post(post_id)
        with self._lock:
            now = self._clock()
            comment = Comment(next(self._comment_ids), post_id, user_id, content, now)
            thread = self._threads.get(post_id)
            if thread is None:
                thread = self._threads[post_id] = Thread()
            thread.append(comment)
            return comment.to_dict()

    def add_reply(self, post_id: int, comment_id: int, user_id: str, content: str) -> ReplyDict:
        """顺序固定：文本 → 帖子 → 评论（必须在这个帖子下）。评论查不到就不分配回复 ID。"""
        _require_text(user_id, "user_id")
        _require_text(content, "content")
        self._require_post(post_id)
        with self._lock:
            thread = self._threads.get(post_id)
            comment = thread.find(comment_id) if thread is not None else None
            if comment is None:
                raise NotFoundError(f"comment {comment_id!r} not found under post {post_id!r}")
            now = self._clock()
            reply = Reply(next(self._reply_ids), post_id, comment.id, user_id, content, now)
            comment.replies.append(reply)
            return reply.to_dict()

    def get_comments(self, post_id: int) -> list[CommentDict]:
        """整串快照在锁里生成：不会看到"回复已经在、评论却还没有"的半截状态。"""
        self._require_post(post_id)
        with self._lock:
            thread = self._threads.get(post_id)
            return thread.snapshot() if thread is not None else []

    def _require_post(self, post_id: object) -> None:
        if not _is_id(post_id) or not self.post_store.exists(post_id):
            raise NotFoundError(f"post {post_id!r} not found")


class _DemoPosts:
    def exists(self, post_id: int) -> bool:
        return post_id in (10, 20)


if __name__ == "__main__":
    service = CommentService(_DemoPosts())
    first = service.add_comment(10, "u1", "Hello Leet")
    service.add_reply(10, first["id"], "u2", "Hi Code")
    for item in service.get_comments(10):
        print(item["id"], item["content"], [r["content"] for r in item["replies"]])
