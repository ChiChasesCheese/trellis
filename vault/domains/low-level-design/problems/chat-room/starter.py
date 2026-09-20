"""聊天室（Chat Room）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/chat-room -q`。
内部表示随你选：测试只看公开方法与属性（`members_of`、`is_online`、`connected_count`、
`typing_in`、`typing_room_count`、`unread_count` 等），不碰任何下划线开头的东西。
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Protocol

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


class ChatError(Exception):
    """本组件所有失败的共同基类。"""


class UnknownUserError(ChatError, KeyError):
    """引用了一个没有注册过的用户 id。"""


class UnknownRoomError(ChatError, KeyError):
    """房间 id 不存在。"""


class NotAMemberError(ChatError):
    """对一个自己不在其中的房间发消息、读历史或标记已读。"""


class NotSenderError(ChatError):
    """编辑或删除一条不是自己发的消息。"""


class MessageDeletedError(ChatError):
    """编辑一条已经被删除的消息。"""


class MessageNotFoundError(ChatError, KeyError):
    """消息 id 不存在。"""


@dataclass(frozen=True, slots=True)
class User:
    """一个用户。"""

    user_id: str
    display_name: str


@dataclass(frozen=True, slots=True)
class Room:
    """一个房间：单聊只是恰好两个成员的房间。"""

    room_id: str
    name: str | None
    is_direct: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Message:
    """一条消息的快照。`seq` 是服务端到达顺序。"""

    message_id: str
    room_id: str
    sender_id: str
    text: str
    seq: int
    received_at: datetime
    edited_at: datetime | None = None
    deleted: bool = False


class Connection(Protocol):
    """一个已连接成员的投递端点。"""

    def deliver(self, message: Message) -> None: ...


class MessageStore:
    """消息本身：顺序、编辑、删除。"""

    def __init__(self, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    def append(self, room_id: str, sender_id: str, text: str) -> Message:
        raise NotImplementedError

    def get(self, message_id: str) -> Message:
        raise NotImplementedError

    def history(self, room_id: str, since_seq: int = 0, limit: int | None = None) -> tuple[Message, ...]:
        raise NotImplementedError

    def latest_seq(self, room_id: str) -> int:
        raise NotImplementedError

    def edit(self, message_id: str, editor_id: str, new_text: str) -> Message:
        raise NotImplementedError

    def delete(self, message_id: str, actor_id: str) -> Message:
        raise NotImplementedError


class RoomDirectory:
    """房间与成员关系：谁在哪个房间里、单聊的去重、每人每房间的已读游标。"""

    def __init__(self, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    def create_room(self, member_ids: set[str], name: str | None = None) -> Room:
        raise NotImplementedError

    def direct_room(self, a: str, b: str) -> Room:
        raise NotImplementedError

    def get(self, room_id: str) -> Room:
        raise NotImplementedError

    def add_member(self, room_id: str, user_id: str) -> None:
        raise NotImplementedError

    def remove_member(self, room_id: str, user_id: str) -> None:
        raise NotImplementedError

    def members_of(self, room_id: str) -> frozenset[str]:
        raise NotImplementedError

    def is_member(self, room_id: str, user_id: str) -> bool:
        raise NotImplementedError

    def mark_read(self, room_id: str, user_id: str, seq: int) -> None:
        raise NotImplementedError

    def last_read(self, room_id: str, user_id: str) -> int:
        raise NotImplementedError


class PresenceService:
    """连接与"正在输入"：进程内的临时状态，从不落盘、从不进历史。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def connect(self, user_id: str, connection: Connection) -> None:
        raise NotImplementedError

    def disconnect(self, user_id: str) -> None:
        raise NotImplementedError

    def is_online(self, user_id: str) -> bool:
        raise NotImplementedError

    def connection_of(self, user_id: str) -> Connection | None:
        raise NotImplementedError

    def connected_count(self) -> int:
        raise NotImplementedError

    def set_typing(self, room_id: str, user_id: str, typing: bool) -> None:
        raise NotImplementedError

    def typing_in(self, room_id: str) -> frozenset[str]:
        raise NotImplementedError

    def typing_room_count(self, user_id: str) -> int:
        raise NotImplementedError


class ChatService:
    """整个系统的入口：持有房间目录、消息仓库、在线状态，并编排发消息时的投递。"""

    def __init__(self, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    def register_user(self, user_id: str, display_name: str) -> User:
        raise NotImplementedError

    def create_room(self, creator_id: str, member_ids: tuple[str, ...] = (), name: str | None = None) -> Room:
        raise NotImplementedError

    def direct_room(self, a: str, b: str) -> Room:
        raise NotImplementedError

    def join(self, room_id: str, user_id: str) -> None:
        raise NotImplementedError

    def leave(self, room_id: str, user_id: str) -> None:
        raise NotImplementedError

    def members_of(self, room_id: str) -> frozenset[str]:
        raise NotImplementedError

    def send_message(self, room_id: str, sender_id: str, text: str) -> Message:
        raise NotImplementedError

    def edit_message(self, message_id: str, editor_id: str, new_text: str) -> Message:
        raise NotImplementedError

    def delete_message(self, message_id: str, actor_id: str) -> Message:
        raise NotImplementedError

    def history(self, room_id: str, viewer_id: str, since_seq: int = 0,
               limit: int | None = None) -> tuple[Message, ...]:
        raise NotImplementedError

    def mark_read(self, room_id: str, user_id: str, seq: int | None = None) -> None:
        raise NotImplementedError

    def unread_count(self, room_id: str, user_id: str) -> int:
        raise NotImplementedError

    def connect(self, user_id: str, connection: Connection) -> None:
        raise NotImplementedError

    def disconnect(self, user_id: str) -> None:
        raise NotImplementedError

    def is_online(self, user_id: str) -> bool:
        raise NotImplementedError

    def connected_count(self) -> int:
        raise NotImplementedError

    def set_typing(self, room_id: str, user_id: str, typing: bool) -> None:
        raise NotImplementedError

    def typing_in(self, room_id: str) -> frozenset[str]:
        raise NotImplementedError

    def typing_room_count(self, user_id: str) -> int:
        raise NotImplementedError
