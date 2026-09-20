"""社交网络的验收测试：好友与关注的区别、隐私可见性的单一判定点、拉黑切双向、
写扩散信息流与大V例外、评论点赞不改变扩散路径。

所有断言只看公开方法（`are_friends`、`is_following`、`is_blocked`、`can_view`、`is_celebrity`、
`like_count`、`comment_count`），不碰任何下划线属性。`make_network` 建网络放在每个测试函数体内
（不是 fixture）：starter 的 `__init__` 会 `raise NotImplementedError`，构造放在测试体内才会被
pytest 记成一次明确的失败，而不是一次容易被忽略的 fixture 错误。
"""

from __future__ import annotations

import importlib
import os
from datetime import datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

ALL_USERS = ("ada", "grace", "linus", "margaret", "alan", "barbara")


class FrozenClock:
    """固定时钟，测试自己推进；帖子的先后因此完全可预测。"""

    def __init__(self) -> None:
        self._base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._delta = timedelta()

    def __call__(self) -> datetime:
        return self._base + self._delta

    def advance(self, seconds: float) -> None:
        self._delta += timedelta(seconds=seconds)


def make_network(celebrity_threshold: int = 3):
    clock = FrozenClock()
    net = impl.SocialNetwork(clock=clock, celebrity_threshold=celebrity_threshold)
    for uid in ALL_USERS:
        net.register_user(uid, uid.title())
    return net, clock


# ---- 第 1 关：好友 vs 关注，帖子与信息流 -----------------------------------


def test_follow_is_one_way() -> None:
    network, _ = make_network()
    network.follow("linus", "ada")
    assert network.is_following("linus", "ada")
    assert not network.is_following("ada", "linus")
    assert not network.are_friends("linus", "ada")


def test_friend_request_accept_creates_mutual_friendship() -> None:
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    assert network.are_friends("ada", "grace")
    assert network.are_friends("grace", "ada")


def test_accept_friend_request_also_creates_mutual_follow() -> None:
    """好友暗含互相关注——两套机制服务不同的目的，接受好友请求时把它们接在一起。"""
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    assert network.is_following("ada", "grace")
    assert network.is_following("grace", "ada")


def test_declined_friend_request_creates_no_friendship() -> None:
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.decline_friend_request(request.request_id, "grace")
    assert not network.are_friends("ada", "grace")
    assert not network.is_following("ada", "grace")


def test_mirrored_friend_request_auto_accepts() -> None:
    """双方各自先发了一条给对方，第二条不该悬着——两个方向的意愿已经一致。"""
    network, _ = make_network()
    network.send_friend_request("ada", "grace")
    network.send_friend_request("grace", "ada")
    assert network.are_friends("ada", "grace")


def test_duplicate_friend_request_raises() -> None:
    network, _ = make_network()
    network.send_friend_request("ada", "grace")
    with pytest.raises(impl.DuplicateRequestError):
        network.send_friend_request("ada", "grace")


def test_unfriend_removes_both_directions_but_keeps_follow() -> None:
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    network.unfriend("ada", "grace")
    assert not network.are_friends("ada", "grace")
    assert not network.are_friends("grace", "ada")
    assert network.is_following("ada", "grace")  # 解除好友不强制取关


def test_public_post_visible_to_a_stranger() -> None:
    network, _ = make_network()
    post = network.create_post("ada", "hello world", impl.Visibility.PUBLIC)
    assert network.can_view(post.post_id, "linus")


def test_unknown_user_raises() -> None:
    network, _ = make_network()
    with pytest.raises(impl.UnknownUserError):
        network.follow("ghost", "ada")


# ---- 第 2 关：写扩散信息流与大V例外 -----------------------------------------


def test_feed_fanout_on_write_delivers_to_follower_inbox() -> None:
    network, _ = make_network()
    network.follow("linus", "ada")
    post = network.create_post("ada", "shipped it", impl.Visibility.PUBLIC)
    assert network.is_celebrity("ada") is False
    feed = network.get_feed("linus")
    assert feed == (post,)


def test_celebrity_account_skips_fanout_but_feed_still_shows_it() -> None:
    """粉丝数达到阈值（本测试设为 3）之后不再写扩散，改成读时从作者的近期帖子里拉。"""
    network, _ = make_network(celebrity_threshold=3)
    for follower in ("grace", "linus", "margaret"):
        network.follow(follower, "ada")
    assert network.is_celebrity("ada") is True
    post = network.create_post("ada", "big announcement", impl.Visibility.PUBLIC)
    feed = network.get_feed("linus")
    assert post in feed


def test_feed_orders_newest_first() -> None:
    network, clock = make_network()
    network.follow("linus", "ada")
    first = network.create_post("ada", "first", impl.Visibility.PUBLIC)
    clock.advance(10)
    second = network.create_post("ada", "second", impl.Visibility.PUBLIC)
    feed = network.get_feed("linus")
    assert feed == (second, first)


def test_mute_filters_feed_without_unfollowing() -> None:
    network, _ = make_network()
    network.follow("linus", "ada")
    post = network.create_post("ada", "noise", impl.Visibility.PUBLIC)
    network.mute("linus", "ada")
    assert post not in network.get_feed("linus")
    assert network.is_following("linus", "ada")  # 静音不等于取关


# ---- 第 3 关：隐私可见性——单一判定点 ----------------------------------------


def test_friends_only_post_hidden_from_non_friend() -> None:
    network, _ = make_network()
    post = network.create_post("ada", "just for friends", impl.Visibility.FRIENDS)
    assert not network.can_view(post.post_id, "linus")


def test_friends_only_post_visible_to_friend() -> None:
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    post = network.create_post("ada", "just for friends", impl.Visibility.FRIENDS)
    assert network.can_view(post.post_id, "grace")


def test_list_post_visible_only_to_list_members() -> None:
    network, _ = make_network()
    network.create_list("ada", "inner-circle")
    network.add_to_list("ada", "inner-circle", "grace")
    post = network.create_post("ada", "secret", impl.Visibility.LIST, audience_list="inner-circle")
    assert network.can_view(post.post_id, "grace")
    assert not network.can_view(post.post_id, "linus")


def test_block_cuts_visibility_both_directions() -> None:
    network, _ = make_network()
    post_by_ada = network.create_post("ada", "public post", impl.Visibility.PUBLIC)
    network.block("ada", "linus")
    assert not network.can_view(post_by_ada.post_id, "linus")
    post_by_linus = network.create_post("linus", "another public post", impl.Visibility.PUBLIC)
    assert not network.can_view(post_by_linus.post_id, "ada")


def test_block_survives_already_fanned_out_posts() -> None:
    """写扩散是发布时刻的快照，但拉黑走的是可见性判定，读时依然立即生效。"""
    network, _ = make_network()
    network.follow("linus", "ada")
    post = network.create_post("ada", "before the block", impl.Visibility.PUBLIC)
    assert post in network.get_feed("linus")
    network.block("ada", "linus")
    assert post not in network.get_feed("linus")


def test_block_removes_existing_friendship_and_follow() -> None:
    network, _ = make_network()
    request = network.send_friend_request("ada", "grace")
    network.accept_friend_request(request.request_id, "grace")
    network.block("ada", "grace")
    assert not network.are_friends("ada", "grace")
    assert not network.is_following("ada", "grace")
    assert not network.is_following("grace", "ada")


def test_block_prevents_new_friend_requests_and_follow() -> None:
    network, _ = make_network()
    network.block("ada", "grace")
    with pytest.raises(impl.BlockedError):
        network.send_friend_request("ada", "grace")
    with pytest.raises(impl.BlockedError):
        network.follow("grace", "ada")


# ---- 第 4 关：评论与点赞，不碰扩散路径 --------------------------------------


def test_like_is_an_idempotent_toggle() -> None:
    network, _ = make_network()
    post = network.create_post("ada", "hi", impl.Visibility.PUBLIC)
    assert network.like(post.post_id, "grace") is True
    assert network.like(post.post_id, "grace") is False
    assert network.like_count(post.post_id) == 1
    assert network.unlike(post.post_id, "grace") is True
    assert network.like_count(post.post_id) == 0


def test_comment_is_its_own_entity_with_a_count() -> None:
    network, _ = make_network()
    post = network.create_post("ada", "hi", impl.Visibility.PUBLIC)
    network.add_comment(post.post_id, "grace", "nice!")
    network.add_comment(post.post_id, "linus", "congrats")
    assert network.comment_count(post.post_id) == 2
    authors = {c.author_id for c in network.comments_for(post.post_id)}
    assert authors == {"grace", "linus"}


def test_blocked_user_cannot_comment_or_like() -> None:
    network, _ = make_network()
    post = network.create_post("ada", "hi", impl.Visibility.PUBLIC)
    network.block("ada", "linus")
    with pytest.raises(impl.BlockedError):
        network.add_comment(post.post_id, "linus", "nope")
    with pytest.raises(impl.BlockedError):
        network.like(post.post_id, "linus")


def test_comment_and_like_do_not_change_feed_fanout() -> None:
    """第 4 关的判分点：加评论/点赞，`FeedService.publish` 一行不用动。"""
    network, _ = make_network()
    network.follow("linus", "ada")
    post = network.create_post("ada", "hi", impl.Visibility.PUBLIC)
    before = network.get_feed("linus")
    network.add_comment(post.post_id, "linus", "nice")
    network.like(post.post_id, "linus")
    after = network.get_feed("linus")
    assert before == after
