"""社交网络（Social Network）：好友关系、发帖与信息流、隐私可见性规则。
设计：`SocialGraph` 只管关系（好友、关注、拉黑、命名分组），`ContentStore` 只管内容（帖子、
评论、点赞）并拥有唯一一处可见性判定 `can_view`，`FeedService` 决定信息流怎么产生（写扩散 +
大V读时合并），`SocialNetwork` 把三者串起来、做跨对象的校验。这是进程内的对象设计，不是分布式
系统——没有分片、没有跨机复制，全部状态留在内存里，重启即丢。
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
    """默认时钟。带时区，帖子之间的先后因此可以跨来源比较。"""
    return datetime.now(timezone.utc)


class SocialNetworkError(Exception):
    """本组件所有失败的共同基类，调用方可以只捕获这一个。"""


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
    """一条帖子的可见范围。取值集合是封闭的三档，因此用 `Enum`。"""

    PUBLIC = "public"     # 任何人（除被作者拉黑者）可见
    FRIENDS = "friends"    # 仅互为好友可见
    LIST = "list"          # 仅命名分组（如"亲密好友"）里的成员可见


class FriendRequestStatus(Enum):
    """一条好友请求的状态机：待处理 -> 接受 / 拒绝，不可逆。"""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


@dataclass(frozen=True, slots=True)
class User:
    """一个用户：只有系统需要知道的最小信息。"""

    user_id: str
    display_name: str


@dataclass(slots=True)
class FriendRequest:
    """一条好友请求。`status` 会变，所以不是 `frozen`——但它只由 `SocialGraph` 一处修改。"""

    request_id: str
    from_id: str
    to_id: str
    status: FriendRequestStatus = FriendRequestStatus.PENDING


@dataclass(frozen=True, slots=True)
class Post:
    """一条帖子：冻结快照，谁都能安全地拿去比较、排序、放进多个人的信息流。"""

    post_id: str
    author_id: str
    text: str
    visibility: Visibility
    audience_list: str | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Comment:
    """一条评论：独立实体，不是帖子上的一个字段——它有自己的作者和时间。"""

    comment_id: str
    post_id: str
    author_id: str
    text: str
    created_at: datetime


class SocialGraph:
    """用户之间的关系：好友（对称）、关注（不对称）、拉黑（对称）、命名分组。

    它拥有三条不变量：好友关系永远双向同时存在或同时不存在；拉黑立刻切断双方已有的好友与
    关注边，且此后任何一方都不能再对另一方发起关系或互动；接受好友请求会顺带建立双向关注
    （产品意义：好友本就该互相看到对方的信息流，除非之后显式取关）。
    """

    def __init__(self) -> None:
        self._friends: dict[str, set[str]] = {}
        self._requests: dict[str, FriendRequest] = {}
        self._pending_index: dict[tuple[str, str], str] = {}
        self._following: dict[str, set[str]] = {}
        self._followers: dict[str, set[str]] = {}
        self._blocked: dict[str, set[str]] = {}
        self._lists: dict[tuple[str, str], set[str]] = {}
        self._next_request_id = itertools.count(1)

    # ---- 好友：请求 + 接受，双向同时创建 --------------------------------

    def send_friend_request(self, from_id: str, to_id: str) -> FriendRequest:
        """发起一条好友请求。若对方已经先发了一条待处理请求给我，直接互相接受——两个方向的
        意愿本来就一致，没有理由让两条请求互相悬着。"""
        if from_id == to_id:
            raise ValueError("cannot friend yourself")
        if self.is_blocked(from_id, to_id):
            raise BlockedError(f"{from_id} and {to_id} have blocked each other")
        if self.are_friends(from_id, to_id):
            raise DuplicateRequestError(f"{from_id} and {to_id} are already friends")
        mirror = self._pending_request(to_id, from_id)
        if mirror is not None:
            self._accept(mirror)
            return mirror
        if self._pending_request(from_id, to_id) is not None:
            raise DuplicateRequestError(f"a pending request from {from_id} to {to_id} already exists")
        request = FriendRequest(f"freq-{next(self._next_request_id)}", from_id, to_id)
        self._requests[request.request_id] = request
        self._pending_index[(from_id, to_id)] = request.request_id
        return request

    def accept_friend_request(self, request_id: str, responder_id: str) -> None:
        request = self._require_pending(request_id)
        if responder_id != request.to_id:
            raise ValueError("only the recipient can accept a friend request")
        self._accept(request)

    def decline_friend_request(self, request_id: str, responder_id: str) -> None:
        request = self._require_pending(request_id)
        if responder_id != request.to_id:
            raise ValueError("only the recipient can decline a friend request")
        request.status = FriendRequestStatus.DECLINED
        self._pending_index.pop((request.from_id, request.to_id), None)

    def _require_pending(self, request_id: str) -> FriendRequest:
        try:
            request = self._requests[request_id]
        except KeyError:
            raise UnknownRequestError(request_id) from None
        if request.status is not FriendRequestStatus.PENDING:
            raise InvalidRequestStateError(f"request {request_id} is already {request.status.value}")
        return request

    def _accept(self, request: FriendRequest) -> None:
        request.status = FriendRequestStatus.ACCEPTED
        self._pending_index.pop((request.from_id, request.to_id), None)
        self._friends.setdefault(request.from_id, set()).add(request.to_id)
        self._friends.setdefault(request.to_id, set()).add(request.from_id)
        self.follow(request.from_id, request.to_id)
        self.follow(request.to_id, request.from_id)

    def _pending_request(self, from_id: str, to_id: str) -> FriendRequest | None:
        """O(1) 查某个方向有没有一条待处理请求——这条索引只装待处理的，接受/拒绝后立刻摘除，
        不会随着请求历史的增长而变慢（`_requests` 本身作为审计记录保留，故意不删）。"""
        request_id = self._pending_index.get((from_id, to_id))
        return self._requests.get(request_id) if request_id is not None else None

    def unfriend(self, a: str, b: str) -> None:
        """解除好友。**不**顺带取关——两人仍可能想继续看到彼此的公开信息流。"""
        self._friends.get(a, set()).discard(b)
        self._friends.get(b, set()).discard(a)

    def are_friends(self, a: str, b: str) -> bool:
        return b in self._friends.get(a, ())

    # ---- 关注：单向 --------------------------------------------------

    def follow(self, follower_id: str, followee_id: str) -> None:
        if follower_id == followee_id:
            raise ValueError("cannot follow yourself")
        if self.is_blocked(follower_id, followee_id):
            raise BlockedError(f"{follower_id} and {followee_id} have blocked each other")
        self._following.setdefault(follower_id, set()).add(followee_id)
        self._followers.setdefault(followee_id, set()).add(follower_id)

    def unfollow(self, follower_id: str, followee_id: str) -> None:
        self._following.get(follower_id, set()).discard(followee_id)
        self._followers.get(followee_id, set()).discard(follower_id)

    def is_following(self, follower_id: str, followee_id: str) -> bool:
        return followee_id in self._following.get(follower_id, ())

    def followers_of(self, user_id: str) -> frozenset[str]:
        """快照，不是内部集合本身——调用方不该能改写图的状态。"""
        return frozenset(self._followers.get(user_id, ()))

    def following_of(self, user_id: str) -> frozenset[str]:
        return frozenset(self._following.get(user_id, ()))

    def follower_count(self, user_id: str) -> int:
        return len(self._followers.get(user_id, ()))

    # ---- 拉黑：对称，且立刻切断已有关系 --------------------------------

    def block(self, blocker_id: str, blocked_id: str) -> None:
        """拉黑必须切两个方向——可见性和互动都不能再发生，无论谁拉黑了谁。"""
        self._blocked.setdefault(blocker_id, set()).add(blocked_id)
        self._blocked.setdefault(blocked_id, set()).add(blocker_id)
        self._friends.get(blocker_id, set()).discard(blocked_id)
        self._friends.get(blocked_id, set()).discard(blocker_id)
        self._following.get(blocker_id, set()).discard(blocked_id)
        self._followers.get(blocked_id, set()).discard(blocker_id)
        self._following.get(blocked_id, set()).discard(blocker_id)
        self._followers.get(blocker_id, set()).discard(blocked_id)

    def unblock(self, blocker_id: str, blocked_id: str) -> None:
        """解除拉黑不恢复好友或关注——想重新联系，重新发起。"""
        self._blocked.get(blocker_id, set()).discard(blocked_id)
        self._blocked.get(blocked_id, set()).discard(blocker_id)

    def is_blocked(self, a: str, b: str) -> bool:
        return b in self._blocked.get(a, ())

    # ---- 命名分组：帖子按分组可见 --------------------------------------

    def create_list(self, owner_id: str, name: str) -> str:
        self._lists.setdefault((owner_id, name), set())
        return name

    def add_to_list(self, owner_id: str, name: str, member_id: str) -> None:
        self._lists.setdefault((owner_id, name), set()).add(member_id)

    def list_contains(self, owner_id: str, name: str | None, user_id: str) -> bool:
        return name is not None and user_id in self._lists.get((owner_id, name), ())


class ContentStore:
    """帖子、评论、点赞的存储，以及**唯一一处**可见性判定。

    可见性检查不属于 `Post`（它不该认识 `SocialGraph`），也不重复写在 `FeedService` 和
    facade 里——`can_view` 把关系图当参数传入而不是持有引用，任何需要判断"谁能看这条帖子"
    的地方都调它一次，永不第二处实现。
    """

    def __init__(self, clock: Clock = utc_now) -> None:
        self._clock = clock
        self._posts: dict[str, Post] = {}
        self._comments: dict[str, list[Comment]] = {}
        self._likes: dict[str, set[str]] = {}
        self._next_post_id = itertools.count(1)
        self._next_comment_id = itertools.count(1)

    def create_post(self, author_id: str, text: str, visibility: Visibility = Visibility.PUBLIC,
                    audience_list: str | None = None) -> Post:
        if visibility is Visibility.LIST and audience_list is None:
            raise ValueError("LIST visibility requires an audience_list name")
        post = Post(f"post-{next(self._next_post_id)}", author_id, text, visibility,
                   audience_list, self._clock())
        self._posts[post.post_id] = post
        return post

    def get(self, post_id: str) -> Post:
        try:
            return self._posts[post_id]
        except KeyError:
            raise PostNotFoundError(post_id) from None

    def can_view(self, post: Post, viewer_id: str, graph: SocialGraph) -> bool:
        """**唯一**的可见性判定。发布时用它筛谁值得写扩散，读信息流时再用它兜底——两处调用
        同一个函数，因此拉黑之类的规则只需要写在这一个地方就对所有路径生效。"""
        if graph.is_blocked(post.author_id, viewer_id):
            return False
        if viewer_id == post.author_id:
            return True
        if post.visibility is Visibility.PUBLIC:
            return True
        if post.visibility is Visibility.FRIENDS:
            return graph.are_friends(post.author_id, viewer_id)
        return graph.list_contains(post.author_id, post.audience_list, viewer_id)

    def add_comment(self, post_id: str, author_id: str, text: str) -> Comment:
        self.get(post_id)
        comment = Comment(f"comment-{next(self._next_comment_id)}", post_id, author_id,
                         text, self._clock())
        self._comments.setdefault(post_id, []).append(comment)
        return comment

    def comments_for(self, post_id: str) -> tuple[Comment, ...]:
        return tuple(self._comments.get(post_id, ()))

    def comment_count(self, post_id: str) -> int:
        return len(self._comments.get(post_id, ()))

    def like(self, post_id: str, user_id: str) -> bool:
        """幂等：重复点赞不报错也不重复计数，返回这一次是不是真的新增了一个赞。"""
        self.get(post_id)
        likers = self._likes.setdefault(post_id, set())
        if user_id in likers:
            return False
        likers.add(user_id)
        return True

    def unlike(self, post_id: str, user_id: str) -> bool:
        likers = self._likes.get(post_id)
        if not likers or user_id not in likers:
            return False
        likers.discard(user_id)
        return True

    def like_count(self, post_id: str) -> int:
        return len(self._likes.get(post_id, ()))


class FeedService:
    """信息流：写扩散（fan-out on write）为主，大V例外读时合并。

    每次发帖把帖子 id 推进每个能看到它的关注者的收件箱（有界，防止无限增长）；这份扩散是
    **发布时刻的快照**——之后解除好友不会把已经推送的帖子收回，这是写扩散模型本身的代价，
    诚实地承认它。拉黑不受这条限制：`can_view` 在读信息流时仍会被再判一次，所以拉黑总是
    立即生效，即便帖子已经躺在收件箱里。粉丝数达到阈值的账号（大V）完全跳过扩散——扩散一条
    要写几百万份收件箱不现实——改成读者在读信息流时把大V的近期帖子直接拉过来合并。
    """

    def __init__(self, store: ContentStore, celebrity_threshold: int = 10_000,
                inbox_capacity: int = 200, authored_capacity: int = 50) -> None:
        self._store = store
        self._celebrity_threshold = celebrity_threshold
        self._inbox_capacity = inbox_capacity
        self._authored_capacity = authored_capacity
        self._inboxes: dict[str, deque[str]] = {}
        self._authored: dict[str, deque[str]] = {}
        self._muted: dict[str, set[str]] = {}

    def is_celebrity(self, author_id: str, graph: SocialGraph) -> bool:
        return graph.follower_count(author_id) >= self._celebrity_threshold

    def publish(self, post: Post, graph: SocialGraph) -> None:
        self._authored.setdefault(post.author_id, deque(maxlen=self._authored_capacity)) \
            .appendleft(post.post_id)
        if self.is_celebrity(post.author_id, graph):
            return
        for follower_id in graph.followers_of(post.author_id):
            if self._store.can_view(post, follower_id, graph):
                self._inboxes.setdefault(follower_id, deque(maxlen=self._inbox_capacity)) \
                    .appendleft(post.post_id)

    def mute(self, viewer_id: str, author_id: str) -> None:
        self._muted.setdefault(viewer_id, set()).add(author_id)

    def unmute(self, viewer_id: str, author_id: str) -> None:
        self._muted.get(viewer_id, set()).discard(author_id)

    def inbox_size(self, user_id: str) -> int:
        return len(self._inboxes.get(user_id, ()))

    def get_feed(self, viewer_id: str, graph: SocialGraph, limit: int = 20) -> tuple[Post, ...]:
        muted = self._muted.get(viewer_id, frozenset())
        candidates = list(self._inboxes.get(viewer_id, ()))
        for followee_id in graph.following_of(viewer_id):
            if self.is_celebrity(followee_id, graph):
                candidates.extend(self._authored.get(followee_id, ()))
        seen: set[str] = set()
        posts: list[Post] = []
        for post_id in candidates:
            if post_id in seen:
                continue
            seen.add(post_id)
            try:
                post = self._store.get(post_id)
            except PostNotFoundError:
                continue
            if post.author_id in muted or not self._store.can_view(post, viewer_id, graph):
                continue
            posts.append(post)
        posts.sort(key=lambda p: (p.created_at, p.post_id), reverse=True)
        return tuple(posts[:limit])


class SocialNetwork:
    """整个系统的入口：持有关系图、内容仓库、信息流服务，并做跨对象的编排与校验。

    `create_post` 要先落库再扩散，`add_comment`/`like` 要先查拉黑再落库——这些是需要看到
    两个子对象才能做的判断，facade 因此不是纯转发：它是编排点。
    """

    def __init__(self, clock: Clock = utc_now, celebrity_threshold: int = 10_000,
                inbox_capacity: int = 200) -> None:
        self._users: dict[str, User] = {}
        self._graph = SocialGraph()
        self._content = ContentStore(clock)
        self._feed = FeedService(self._content, celebrity_threshold, inbox_capacity)

    def register_user(self, user_id: str, display_name: str) -> User:
        user = User(user_id, display_name)
        self._users[user_id] = user
        return user

    def _require(self, user_id: str) -> None:
        if user_id not in self._users:
            raise UnknownUserError(user_id)

    def send_friend_request(self, from_id: str, to_id: str) -> FriendRequest:
        self._require(from_id)
        self._require(to_id)
        return self._graph.send_friend_request(from_id, to_id)

    def accept_friend_request(self, request_id: str, responder_id: str) -> None:
        self._graph.accept_friend_request(request_id, responder_id)

    def decline_friend_request(self, request_id: str, responder_id: str) -> None:
        self._graph.decline_friend_request(request_id, responder_id)

    def unfriend(self, a: str, b: str) -> None:
        self._graph.unfriend(a, b)

    def are_friends(self, a: str, b: str) -> bool:
        return self._graph.are_friends(a, b)

    def follow(self, follower_id: str, followee_id: str) -> None:
        self._require(follower_id)
        self._require(followee_id)
        self._graph.follow(follower_id, followee_id)

    def unfollow(self, follower_id: str, followee_id: str) -> None:
        self._graph.unfollow(follower_id, followee_id)

    def is_following(self, follower_id: str, followee_id: str) -> bool:
        return self._graph.is_following(follower_id, followee_id)

    def block(self, blocker_id: str, blocked_id: str) -> None:
        self._graph.block(blocker_id, blocked_id)

    def unblock(self, blocker_id: str, blocked_id: str) -> None:
        self._graph.unblock(blocker_id, blocked_id)

    def is_blocked(self, a: str, b: str) -> bool:
        return self._graph.is_blocked(a, b)

    def create_list(self, owner_id: str, name: str) -> str:
        return self._graph.create_list(owner_id, name)

    def add_to_list(self, owner_id: str, name: str, member_id: str) -> None:
        self._graph.add_to_list(owner_id, name, member_id)

    def create_post(self, author_id: str, text: str, visibility: Visibility = Visibility.PUBLIC,
                    audience_list: str | None = None) -> Post:
        self._require(author_id)
        post = self._content.create_post(author_id, text, visibility, audience_list)
        self._feed.publish(post, self._graph)
        return post

    def can_view(self, post_id: str, viewer_id: str) -> bool:
        return self._content.can_view(self._content.get(post_id), viewer_id, self._graph)

    def add_comment(self, post_id: str, author_id: str, text: str) -> Comment:
        post = self._content.get(post_id)
        if self._graph.is_blocked(post.author_id, author_id):
            raise BlockedError(f"{author_id} cannot interact with {post.author_id}")
        return self._content.add_comment(post_id, author_id, text)

    def comments_for(self, post_id: str) -> tuple[Comment, ...]:
        return self._content.comments_for(post_id)

    def comment_count(self, post_id: str) -> int:
        return self._content.comment_count(post_id)

    def like(self, post_id: str, user_id: str) -> bool:
        post = self._content.get(post_id)
        if self._graph.is_blocked(post.author_id, user_id):
            raise BlockedError(f"{user_id} cannot interact with {post.author_id}")
        return self._content.like(post_id, user_id)

    def unlike(self, post_id: str, user_id: str) -> bool:
        return self._content.unlike(post_id, user_id)

    def like_count(self, post_id: str) -> int:
        return self._content.like_count(post_id)

    def mute(self, viewer_id: str, author_id: str) -> None:
        self._feed.mute(viewer_id, author_id)

    def unmute(self, viewer_id: str, author_id: str) -> None:
        self._feed.unmute(viewer_id, author_id)

    def is_celebrity(self, user_id: str) -> bool:
        return self._feed.is_celebrity(user_id, self._graph)

    def get_feed(self, viewer_id: str, limit: int = 20) -> tuple[Post, ...]:
        return self._feed.get_feed(viewer_id, self._graph, limit)


def _demo() -> None:
    network = SocialNetwork(celebrity_threshold=2)
    for uid in ("ada", "grace", "linus"):
        network.register_user(uid, uid.title())
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    network.follow("linus", "ada")
    post = network.create_post("ada", "hello, friends", Visibility.FRIENDS)
    network.like(post.post_id, "grace")
    print("grace's feed:", [p.text for p in network.get_feed("grace")])
    print("linus's feed (not a friend):", [p.text for p in network.get_feed("linus")])


if __name__ == "__main__":
    _demo()
