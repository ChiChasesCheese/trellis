"""社交网络（Social Network）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/social-network -q`。
内部表示随你选：测试只看公开方法与属性（`are_friends`、`is_following`、`is_blocked`、
`can_view`、`inbox_size`、`is_celebrity`、`like_count`、`comment_count` 等），不碰任何下划线
开头的东西。
"""

from __future__ import annotations

import itertools
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


class SocialNetworkError(Exception):
    """本组件所有失败的共同基类。"""


class UnknownUserError(SocialNetworkError, KeyError):
    """引用了一个没有注册过的用户 id。"""


class UnknownRequestError(SocialNetworkError, KeyError):
    """好友请求 id 不存在。"""


class DuplicateRequestError(SocialNetworkError):
    """两人之间已经有一条待处理的同向好友请求。"""


class InvalidRequestStateError(SocialNetworkError):
    """对一条已经不是"待处理"的请求再次接受/拒绝。"""


class BlockedError(SocialNetworkError):
    """双方存在拉黑关系，操作因此被拒绝。"""


class PostNotFoundError(SocialNetworkError, KeyError):
    """帖子 id 不存在。"""


class Visibility(Enum):
    """一条帖子的可见范围。"""

    PUBLIC = "public"
    FRIENDS = "friends"
    LIST = "list"


class FriendRequestStatus(Enum):
    """一条好友请求的状态机。"""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


@dataclass(frozen=True, slots=True)
class User:
    """一个用户。"""

    user_id: str
    display_name: str


@dataclass(slots=True)
class FriendRequest:
    """一条好友请求。"""

    request_id: str
    from_id: str
    to_id: str
    status: FriendRequestStatus = FriendRequestStatus.PENDING


@dataclass(frozen=True, slots=True)
class Post:
    """一条帖子。"""

    post_id: str
    author_id: str
    text: str
    visibility: Visibility
    audience_list: str | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Comment:
    """一条评论。"""

    comment_id: str
    post_id: str
    author_id: str
    text: str
    created_at: datetime


class SocialGraph:
    """用户之间的关系：好友（对称）、关注（不对称）、拉黑（对称）、命名分组。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def send_friend_request(self, from_id: str, to_id: str) -> FriendRequest:
        raise NotImplementedError

    def accept_friend_request(self, request_id: str, responder_id: str) -> None:
        raise NotImplementedError

    def decline_friend_request(self, request_id: str, responder_id: str) -> None:
        raise NotImplementedError

    def unfriend(self, a: str, b: str) -> None:
        raise NotImplementedError

    def are_friends(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def follow(self, follower_id: str, followee_id: str) -> None:
        raise NotImplementedError

    def unfollow(self, follower_id: str, followee_id: str) -> None:
        raise NotImplementedError

    def is_following(self, follower_id: str, followee_id: str) -> bool:
        raise NotImplementedError

    def followers_of(self, user_id: str) -> frozenset[str]:
        raise NotImplementedError

    def following_of(self, user_id: str) -> frozenset[str]:
        raise NotImplementedError

    def follower_count(self, user_id: str) -> int:
        raise NotImplementedError

    def block(self, blocker_id: str, blocked_id: str) -> None:
        raise NotImplementedError

    def unblock(self, blocker_id: str, blocked_id: str) -> None:
        raise NotImplementedError

    def is_blocked(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def create_list(self, owner_id: str, name: str) -> str:
        raise NotImplementedError

    def add_to_list(self, owner_id: str, name: str, member_id: str) -> None:
        raise NotImplementedError

    def list_contains(self, owner_id: str, name: str | None, user_id: str) -> bool:
        raise NotImplementedError


class ContentStore:
    """帖子、评论、点赞的存储，以及唯一一处可见性判定。"""

    def __init__(self, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    def create_post(self, author_id: str, text: str, visibility: Visibility = Visibility.PUBLIC,
                    audience_list: str | None = None) -> Post:
        raise NotImplementedError

    def get(self, post_id: str) -> Post:
        raise NotImplementedError

    def can_view(self, post: Post, viewer_id: str, graph: SocialGraph) -> bool:
        raise NotImplementedError

    def add_comment(self, post_id: str, author_id: str, text: str) -> Comment:
        raise NotImplementedError

    def comments_for(self, post_id: str) -> tuple[Comment, ...]:
        raise NotImplementedError

    def comment_count(self, post_id: str) -> int:
        raise NotImplementedError

    def like(self, post_id: str, user_id: str) -> bool:
        raise NotImplementedError

    def unlike(self, post_id: str, user_id: str) -> bool:
        raise NotImplementedError

    def like_count(self, post_id: str) -> int:
        raise NotImplementedError


class FeedService:
    """信息流：写扩散为主，大V例外读时合并。"""

    def __init__(self, store: ContentStore, celebrity_threshold: int = 10_000,
                inbox_capacity: int = 200, authored_capacity: int = 50) -> None:
        raise NotImplementedError

    def is_celebrity(self, author_id: str, graph: SocialGraph) -> bool:
        raise NotImplementedError

    def publish(self, post: Post, graph: SocialGraph) -> None:
        raise NotImplementedError

    def mute(self, viewer_id: str, author_id: str) -> None:
        raise NotImplementedError

    def unmute(self, viewer_id: str, author_id: str) -> None:
        raise NotImplementedError

    def inbox_size(self, user_id: str) -> int:
        raise NotImplementedError

    def get_feed(self, viewer_id: str, graph: SocialGraph, limit: int = 20) -> tuple[Post, ...]:
        raise NotImplementedError


class SocialNetwork:
    """整个系统的入口：持有关系图、内容仓库、信息流服务，并做跨对象的编排与校验。"""

    def __init__(self, clock: Clock = utc_now, celebrity_threshold: int = 10_000,
                inbox_capacity: int = 200) -> None:
        raise NotImplementedError

    def register_user(self, user_id: str, display_name: str) -> User:
        raise NotImplementedError

    def send_friend_request(self, from_id: str, to_id: str) -> FriendRequest:
        raise NotImplementedError

    def accept_friend_request(self, request_id: str, responder_id: str) -> None:
        raise NotImplementedError

    def decline_friend_request(self, request_id: str, responder_id: str) -> None:
        raise NotImplementedError

    def unfriend(self, a: str, b: str) -> None:
        raise NotImplementedError

    def are_friends(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def follow(self, follower_id: str, followee_id: str) -> None:
        raise NotImplementedError

    def unfollow(self, follower_id: str, followee_id: str) -> None:
        raise NotImplementedError

    def is_following(self, follower_id: str, followee_id: str) -> bool:
        raise NotImplementedError

    def block(self, blocker_id: str, blocked_id: str) -> None:
        raise NotImplementedError

    def unblock(self, blocker_id: str, blocked_id: str) -> None:
        raise NotImplementedError

    def is_blocked(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def create_list(self, owner_id: str, name: str) -> str:
        raise NotImplementedError

    def add_to_list(self, owner_id: str, name: str, member_id: str) -> None:
        raise NotImplementedError

    def create_post(self, author_id: str, text: str, visibility: Visibility = Visibility.PUBLIC,
                    audience_list: str | None = None) -> Post:
        raise NotImplementedError

    def can_view(self, post_id: str, viewer_id: str) -> bool:
        raise NotImplementedError

    def add_comment(self, post_id: str, author_id: str, text: str) -> Comment:
        raise NotImplementedError

    def comments_for(self, post_id: str) -> tuple[Comment, ...]:
        raise NotImplementedError

    def comment_count(self, post_id: str) -> int:
        raise NotImplementedError

    def like(self, post_id: str, user_id: str) -> bool:
        raise NotImplementedError

    def unlike(self, post_id: str, user_id: str) -> bool:
        raise NotImplementedError

    def like_count(self, post_id: str) -> int:
        raise NotImplementedError

    def mute(self, viewer_id: str, author_id: str) -> None:
        raise NotImplementedError

    def unmute(self, viewer_id: str, author_id: str) -> None:
        raise NotImplementedError

    def is_celebrity(self, user_id: str) -> bool:
        raise NotImplementedError

    def get_feed(self, viewer_id: str, limit: int = 20) -> tuple[Post, ...]:
        raise NotImplementedError
