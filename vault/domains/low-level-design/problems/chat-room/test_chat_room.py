"""聊天室的验收测试：服务端到达顺序、单聊复用群聊模型、已读游标派生未读数、
投递到在线连接、断线重连靠游标补发、编辑删除不碰投递、断开连接后"正在输入"容器缩回去。

所有断言只看公开方法（`members_of`、`is_online`、`connected_count`、`typing_in`、
`typing_room_count`、`unread_count`），不碰任何下划线属性。`make_chat` 建服务放在每个测试
函数体内（不是 fixture）：starter 的 `__init__` 会 `raise NotImplementedError`，构造放在
测试体内才会被 pytest 记成一次明确的失败，而不是一次容易被忽略的 fixture 错误。
"""

from __future__ import annotations

import importlib
import os
from datetime import datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

ALL_USERS = ("ada", "grace", "linus", "margaret")


class FrozenClock:
    """固定时钟，测试自己推进；消息的到达顺序因此完全可预测。"""

    def __init__(self) -> None:
        self._base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._delta = timedelta()

    def __call__(self) -> datetime:
        return self._base + self._delta

    def advance(self, seconds: float) -> None:
        self._delta += timedelta(seconds=seconds)


class Inbox:
    """一个把收到的消息记进列表的假连接——测试用它代替真实的 WebSocket。"""

    def __init__(self) -> None:
        self.received: list = []

    def deliver(self, message) -> None:
        self.received.append(message)


def make_chat():
    clock = FrozenClock()
    chat = impl.ChatService(clock=clock)
    for uid in ALL_USERS:
        chat.register_user(uid, uid.title())
    return chat, clock


# ---- 第 1 关：房间、加入离开、发消息、服务端到达顺序 --------------------------


def test_group_room_delivers_history_in_arrival_order() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace", "linus"), name="team")
    first = chat.send_message(room.room_id, "ada", "hello")
    second = chat.send_message(room.room_id, "grace", "hi ada")
    history = chat.history(room.room_id, "linus")
    assert history == (first, second)
    assert [m.seq for m in history] == [1, 2]


def test_join_and_leave_change_membership() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ())
    chat.join(room.room_id, "grace")
    assert chat.members_of(room.room_id) == frozenset({"ada", "grace"})
    chat.leave(room.room_id, "ada")
    assert chat.members_of(room.room_id) == frozenset({"grace"})


def test_non_member_cannot_send_or_read() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ())
    with pytest.raises(impl.NotAMemberError):
        chat.send_message(room.room_id, "grace", "hi")
    with pytest.raises(impl.NotAMemberError):
        chat.history(room.room_id, "grace")


def test_order_is_server_arrival_not_a_client_timestamp() -> None:
    """seq 由服务端在收到消息的那一刻分配，与消息携带的任何客户端信息无关——这里甚至没有
    一个"客户端时间戳"参数可传，顺序完全由到达服务端的先后决定。"""
    chat, clock = make_chat()
    room = chat.create_room("ada", ("grace",))
    first = chat.send_message(room.room_id, "grace", "sent from a clock that is fast")
    clock.advance(-1000)  # 模拟下一条消息来自一个时钟严重落后的客户端
    second = chat.send_message(room.room_id, "ada", "sent from a clock that is slow")
    assert first.seq < second.seq
    assert chat.history(room.room_id, "ada") == (first, second)


def test_unknown_user_raises() -> None:
    chat, _ = make_chat()
    with pytest.raises(impl.UnknownUserError):
        chat.join("no-such-room", "ghost")


# ---- 第 2 关：单聊复用群聊模型；已读游标派生未读数 -----------------------------


def test_direct_room_is_a_two_member_room_reused_on_repeat_calls() -> None:
    chat, _ = make_chat()
    first_call = chat.direct_room("ada", "grace")
    second_call = chat.direct_room("grace", "ada")
    assert first_call.room_id == second_call.room_id
    assert first_call.is_direct is True
    assert chat.members_of(first_call.room_id) == frozenset({"ada", "grace"})


def test_direct_message_uses_the_same_send_and_history_api_as_group() -> None:
    chat, _ = make_chat()
    room = chat.direct_room("ada", "grace")
    message = chat.send_message(room.room_id, "ada", "just us two")
    assert chat.history(room.room_id, "grace") == (message,)


def test_unread_count_is_derived_from_the_read_cursor() -> None:
    chat, _ = make_chat()
    room = chat.direct_room("ada", "grace")
    chat.send_message(room.room_id, "ada", "one")
    chat.send_message(room.room_id, "ada", "two")
    assert chat.unread_count(room.room_id, "grace") == 2
    chat.mark_read(room.room_id, "grace")
    assert chat.unread_count(room.room_id, "grace") == 0


def test_unread_count_excludes_your_own_messages() -> None:
    chat, _ = make_chat()
    room = chat.direct_room("ada", "grace")
    chat.send_message(room.room_id, "ada", "hi")
    assert chat.unread_count(room.room_id, "ada") == 0  # 发送者自动被视为读到了自己这条


def test_leaving_a_room_forgets_the_read_cursor() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    chat.send_message(room.room_id, "ada", "hi")
    chat.mark_read(room.room_id, "grace")
    chat.leave(room.room_id, "grace")
    chat.join(room.room_id, "grace")
    assert chat.unread_count(room.room_id, "grace") == 1  # 重新加入后视为从未读过


# ---- 第 3 关：投递给在线成员；断线重连靠游标补发；在线状态与"正在输入"是临时状态 -----


def test_message_is_delivered_to_connected_members_only() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace", "linus"))
    grace_inbox = Inbox()
    chat.connect("grace", grace_inbox)  # linus 没连接
    message = chat.send_message(room.room_id, "ada", "hi both")
    assert grace_inbox.received == [message]


def test_offline_member_catches_up_via_history_using_their_cursor() -> None:
    """离线成员什么都不会被推送；重连后用它自己保存的已读游标调历史接口就能拿到全部欠账
    ——不需要服务端额外记一份"待补发"的队列。"""
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    while_offline = chat.send_message(room.room_id, "ada", "you were offline for this")
    grace_inbox = Inbox()
    chat.connect("grace", grace_inbox)  # 重连，什么都没被主动推送
    assert grace_inbox.received == []
    missed = chat.history(room.room_id, "grace", since_seq=0)
    assert while_offline in missed


def test_disconnect_makes_a_user_offline_and_shrinks_connected_count() -> None:
    chat, _ = make_chat()
    chat.connect("ada", Inbox())
    chat.connect("grace", Inbox())
    assert chat.connected_count() == 2
    chat.disconnect("ada")
    assert chat.is_online("ada") is False
    assert chat.connected_count() == 1


def test_disconnect_clears_typing_state_in_every_room() -> None:
    """断开连接必须让"正在输入"这个容器缩回去——这是本题里唯一必须收缩的容器。"""
    chat, _ = make_chat()
    room_a = chat.create_room("ada", ("grace",))
    room_b = chat.create_room("ada", ("linus",))
    chat.set_typing(room_a.room_id, "ada", True)
    chat.set_typing(room_b.room_id, "ada", True)
    assert chat.typing_room_count("ada") == 2
    chat.disconnect("ada")
    assert chat.typing_room_count("ada") == 0
    assert "ada" not in chat.typing_in(room_a.room_id)
    assert "ada" not in chat.typing_in(room_b.room_id)


def test_sending_a_message_clears_your_own_typing_indicator() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    chat.set_typing(room.room_id, "ada", True)
    assert "ada" in chat.typing_in(room.room_id)
    chat.send_message(room.room_id, "ada", "done typing")
    assert "ada" not in chat.typing_in(room.room_id)


# ---- 第 4 关：编辑与删除，不碰投递路径 ----------------------------------------


def test_edit_message_is_reflected_in_history() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    message = chat.send_message(room.room_id, "ada", "oops typo")
    chat.edit_message(message.message_id, "ada", "fixed now")
    edited = chat.history(room.room_id, "grace")[0]
    assert edited.text == "fixed now"
    assert edited.edited_at is not None
    assert edited.seq == message.seq  # 编辑不改变它在历史里的位置


def test_only_the_sender_can_edit_or_delete() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    message = chat.send_message(room.room_id, "ada", "mine")
    with pytest.raises(impl.NotSenderError):
        chat.edit_message(message.message_id, "grace", "hijacked")
    with pytest.raises(impl.NotSenderError):
        chat.delete_message(message.message_id, "grace")


def test_delete_tombstones_the_message_but_keeps_its_place_in_history() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    first = chat.send_message(room.room_id, "ada", "will delete this")
    second = chat.send_message(room.room_id, "ada", "keep this")
    chat.delete_message(first.message_id, "ada")
    history = chat.history(room.room_id, "grace")
    assert len(history) == 2
    assert history[0].deleted is True
    assert history[0].text == ""
    assert history[1] == second


def test_cannot_edit_a_deleted_message() -> None:
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    message = chat.send_message(room.room_id, "ada", "bye")
    chat.delete_message(message.message_id, "ada")
    with pytest.raises(impl.MessageDeletedError):
        chat.edit_message(message.message_id, "ada", "undo?")


def test_edit_and_delete_do_not_change_delivery_to_online_members() -> None:
    """第 4 关的判分点：加编辑/删除，`ChatService.send_message` 的投递逻辑一行不用动——
    编辑删除只改 `MessageStore` 里已经发生过的消息，不产生新的投递事件。"""
    chat, _ = make_chat()
    room = chat.create_room("ada", ("grace",))
    grace_inbox = Inbox()
    chat.connect("grace", grace_inbox)
    message = chat.send_message(room.room_id, "ada", "hi")
    assert len(grace_inbox.received) == 1
    chat.edit_message(message.message_id, "ada", "hi there")
    chat.delete_message(message.message_id, "ada")
    assert len(grace_inbox.received) == 1  # 没有因为编辑或删除产生新的投递
