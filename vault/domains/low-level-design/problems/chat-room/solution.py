"""聊天室（Chat Room）：单聊与群聊、消息投递与已读、在线状态。
设计：`MessageStore` 只管消息本身（顺序、编辑、删除），`RoomDirectory` 只管房间与成员关系
（含单聊的去重、每人每房间的已读游标），`PresenceService` 只管连接与"正在输入"这类临时状态，
`ChatService` 把三者串起来、做投递编排。单聊不是另一套模型——它是恰好两个成员的房间，用同一套
消息与历史机制。顺序以**服务端到达顺序**为准，不信任客户端时间戳。这是进程内的对象设计，不是
分布式系统——没有多机复制、没有持久化队列，全部状态留在内存里，重启即丢。
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Protocol

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。带时区，跨来源的消息也能比较先后。"""
    return datetime.now(timezone.utc)


class ChatError(Exception):
    """本组件所有失败的共同基类，调用方可以只捕获这一个。"""


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
    """一个用户：只有系统需要知道的最小信息。"""

    user_id: str
    display_name: str


@dataclass(frozen=True, slots=True)
class Room:
    """一个房间：单聊只是恰好两个成员、`is_direct=True` 的房间，不是另一种类型。"""

    room_id: str
    name: str | None
    is_direct: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Message:
    """一条消息的快照。`seq` 是它在所属房间里的**服务端到达顺序**，不是客户端时间戳——
    客户端时钟可能不准、可能跨时区、消息也可能因网络重排乱序抵达，只有服务端收到的先后
    才是所有人都能达成一致的顺序。编辑/删除通过 `dataclasses.replace` 产生新版本覆盖
    存储里的旧版本，`seq` 和 `message_id` 永远不变，因此历史里的位置不会因为编辑而挪动。
    """

    message_id: str
    room_id: str
    sender_id: str
    text: str
    seq: int
    received_at: datetime
    edited_at: datetime | None = None
    deleted: bool = False


class Connection(Protocol):
    """一个已连接成员的投递端点。真实实现是一个 WebSocket 适配器；测试用一个把消息收进
    列表的假实现——协议只有一个方法，调用方不需要知道背后是不是网络连接。"""

    def deliver(self, message: Message) -> None: ...


class MessageStore:
    """消息本身：顺序、编辑、删除。它拥有的不变量是**顺序稳定**——`seq` 一旦分配，同一条
    消息永远排在同一个位置，编辑或删除只替换内容，不重排、不删除历史条目（软删除留下墓碑）。
    """

    def __init__(self, clock: Clock = utc_now) -> None:
        self._clock = clock
        self._messages: dict[str, Message] = {}
        self._order: dict[str, list[str]] = {}
        self._seq_counters: dict[str, itertools.count] = {}
        self._next_message_id = itertools.count(1)

    def append(self, room_id: str, sender_id: str, text: str) -> Message:
        seq = next(self._seq_counters.setdefault(room_id, itertools.count(1)))
        message = Message(f"msg-{next(self._next_message_id)}", room_id, sender_id, text,
                         seq, self._clock())
        self._messages[message.message_id] = message
        self._order.setdefault(room_id, []).append(message.message_id)
        return message

    def get(self, message_id: str) -> Message:
        try:
            return self._messages[message_id]
        except KeyError:
            raise MessageNotFoundError(message_id) from None

    def history(self, room_id: str, since_seq: int = 0, limit: int | None = None) -> tuple[Message, ...]:
        """`since_seq` 之后的消息，按到达顺序。断线重连时传上次的已读游标，天然就是补发。"""
        ids = self._order.get(room_id, ())
        messages = [self._messages[mid] for mid in ids if self._messages[mid].seq > since_seq]
        return tuple(messages[:limit] if limit is not None else messages)

    def latest_seq(self, room_id: str) -> int:
        ids = self._order.get(room_id, ())
        return self._messages[ids[-1]].seq if ids else 0

    def edit(self, message_id: str, editor_id: str, new_text: str) -> Message:
        message = self.get(message_id)
        if message.sender_id != editor_id:
            raise NotSenderError(f"{editor_id} did not send {message_id}")
        if message.deleted:
            raise MessageDeletedError(f"{message_id} was deleted")
        edited = replace(message, text=new_text, edited_at=self._clock())
        self._messages[message_id] = edited
        return edited

    def delete(self, message_id: str, actor_id: str) -> Message:
        message = self.get(message_id)
        if message.sender_id != actor_id:
            raise NotSenderError(f"{actor_id} did not send {message_id}")
        deleted = replace(message, text="", deleted=True, edited_at=self._clock())
        self._messages[message_id] = deleted
        return deleted


class RoomDirectory:
    """房间与成员关系：谁在哪个房间里、单聊的去重、每人每房间的已读游标。

    未读数**不存**在这里——它是"房间里 seq 大于游标、且不是自己发的消息数"，每次问的时候
    现算，游标是唯一的存储，不会和一个单独维护的计数字段互相漂移。
    """

    def __init__(self, clock: Clock = utc_now) -> None:
        self._clock = clock
        self._rooms: dict[str, Room] = {}
        self._members: dict[str, set[str]] = {}
        self._dm_index: dict[frozenset[str], str] = {}
        self._cursors: dict[tuple[str, str], int] = {}
        self._next_room_id = itertools.count(1)

    def create_room(self, member_ids: set[str], name: str | None = None) -> Room:
        room = Room(f"room-{next(self._next_room_id)}", name, False, self._clock())
        self._rooms[room.room_id] = room
        self._members[room.room_id] = set(member_ids)
        return room

    def direct_room(self, a: str, b: str) -> Room:
        """单聊就是恰好两个成员的房间；用一对用户的无序 key 做去重，反复调用返回同一个房间。"""
        if a == b:
            raise ValueError("cannot direct-message yourself")
        key = frozenset((a, b))
        room_id = self._dm_index.get(key)
        if room_id is not None:
            return self._rooms[room_id]
        room = Room(f"room-{next(self._next_room_id)}", None, True, self._clock())
        self._rooms[room.room_id] = room
        self._members[room.room_id] = {a, b}
        self._dm_index[key] = room.room_id
        return room

    def get(self, room_id: str) -> Room:
        try:
            return self._rooms[room_id]
        except KeyError:
            raise UnknownRoomError(room_id) from None

    def add_member(self, room_id: str, user_id: str) -> None:
        self.get(room_id)
        self._members.setdefault(room_id, set()).add(user_id)

    def remove_member(self, room_id: str, user_id: str) -> None:
        """离开房间也清掉这个人在这个房间的已读游标——不是任何人还在关心的状态。"""
        self._members.get(room_id, set()).discard(user_id)
        self._cursors.pop((room_id, user_id), None)

    def members_of(self, room_id: str) -> frozenset[str]:
        """快照，不是内部集合本身——调用方不该能改写房间的成员表。"""
        return frozenset(self._members.get(room_id, ()))

    def is_member(self, room_id: str, user_id: str) -> bool:
        return user_id in self._members.get(room_id, ())

    def mark_read(self, room_id: str, user_id: str, seq: int) -> None:
        self._cursors[(room_id, user_id)] = seq

    def last_read(self, room_id: str, user_id: str) -> int:
        return self._cursors.get((room_id, user_id), 0)


class PresenceService:
    """连接与"正在输入"：进程内的临时状态，**从不落盘、从不进历史**。

    它拥有的不变量是**断开必须缩回去**：一个用户断开连接时，不仅要摘掉他的连接，还要把他
    "正在输入"的每一个房间都清干净——反向索引 `_typing_rooms` 让这一步不必扫描所有房间，
    直接查"这个人正在哪些房间输入"。忘了这一步，断线用户会在所有人眼里永远"正在输入"。
    """

    def __init__(self) -> None:
        self._connections: dict[str, Connection] = {}
        self._typing: dict[str, set[str]] = {}
        self._typing_rooms: dict[str, set[str]] = {}

    def connect(self, user_id: str, connection: Connection) -> None:
        self._connections[user_id] = connection

    def disconnect(self, user_id: str) -> None:
        self._connections.pop(user_id, None)
        for room_id in self._typing_rooms.pop(user_id, ()):
            self._typing.get(room_id, set()).discard(user_id)

    def is_online(self, user_id: str) -> bool:
        return user_id in self._connections

    def connection_of(self, user_id: str) -> Connection | None:
        return self._connections.get(user_id)

    def connected_count(self) -> int:
        return len(self._connections)

    def set_typing(self, room_id: str, user_id: str, typing: bool) -> None:
        if typing:
            self._typing.setdefault(room_id, set()).add(user_id)
            self._typing_rooms.setdefault(user_id, set()).add(room_id)
        else:
            self._typing.get(room_id, set()).discard(user_id)
            self._typing_rooms.get(user_id, set()).discard(room_id)

    def typing_in(self, room_id: str) -> frozenset[str]:
        return frozenset(self._typing.get(room_id, ()))

    def typing_room_count(self, user_id: str) -> int:
        return len(self._typing_rooms.get(user_id, ()))


class ChatService:
    """整个系统的入口：持有房间目录、消息仓库、在线状态，并编排"发消息时投递给谁"。

    `send_message` 要先落库、再顺带清掉自己的"正在输入"、标记自己已读、最后才投递给在线
    成员——这四步需要看到三个子对象才能做完，facade 因此不是纯转发：它是编排点。
    """

    def __init__(self, clock: Clock = utc_now) -> None:
        self._users: dict[str, User] = {}
        self._rooms = RoomDirectory(clock)
        self._messages = MessageStore(clock)
        self._presence = PresenceService()

    def register_user(self, user_id: str, display_name: str) -> User:
        user = User(user_id, display_name)
        self._users[user_id] = user
        return user

    def _require_user(self, user_id: str) -> None:
        if user_id not in self._users:
            raise UnknownUserError(user_id)

    def _require_member(self, room_id: str, user_id: str) -> None:
        self._rooms.get(room_id)
        if not self._rooms.is_member(room_id, user_id):
            raise NotAMemberError(f"{user_id} is not a member of {room_id}")

    def create_room(self, creator_id: str, member_ids: tuple[str, ...] = (), name: str | None = None) -> Room:
        for user_id in (creator_id, *member_ids):
            self._require_user(user_id)
        return self._rooms.create_room({creator_id, *member_ids}, name)

    def direct_room(self, a: str, b: str) -> Room:
        self._require_user(a)
        self._require_user(b)
        return self._rooms.direct_room(a, b)

    def join(self, room_id: str, user_id: str) -> None:
        self._require_user(user_id)
        self._rooms.add_member(room_id, user_id)

    def leave(self, room_id: str, user_id: str) -> None:
        self._rooms.remove_member(room_id, user_id)

    def members_of(self, room_id: str) -> frozenset[str]:
        return self._rooms.members_of(room_id)

    def send_message(self, room_id: str, sender_id: str, text: str) -> Message:
        self._require_member(room_id, sender_id)
        message = self._messages.append(room_id, sender_id, text)
        self._presence.set_typing(room_id, sender_id, False)
        self._rooms.mark_read(room_id, sender_id, message.seq)
        for member_id in self._rooms.members_of(room_id):
            if member_id == sender_id:
                continue
            connection = self._presence.connection_of(member_id)
            if connection is not None:
                connection.deliver(message)
        return message

    def edit_message(self, message_id: str, editor_id: str, new_text: str) -> Message:
        return self._messages.edit(message_id, editor_id, new_text)

    def delete_message(self, message_id: str, actor_id: str) -> Message:
        return self._messages.delete(message_id, actor_id)

    def history(self, room_id: str, viewer_id: str, since_seq: int = 0,
               limit: int | None = None) -> tuple[Message, ...]:
        self._require_member(room_id, viewer_id)
        return self._messages.history(room_id, since_seq, limit)

    def mark_read(self, room_id: str, user_id: str, seq: int | None = None) -> None:
        self._require_member(room_id, user_id)
        target = seq if seq is not None else self._messages.latest_seq(room_id)
        self._rooms.mark_read(room_id, user_id, target)

    def unread_count(self, room_id: str, user_id: str) -> int:
        cursor = self._rooms.last_read(room_id, user_id)
        return sum(1 for m in self._messages.history(room_id, cursor) if m.sender_id != user_id)

    def connect(self, user_id: str, connection: Connection) -> None:
        self._require_user(user_id)
        self._presence.connect(user_id, connection)

    def disconnect(self, user_id: str) -> None:
        self._presence.disconnect(user_id)

    def is_online(self, user_id: str) -> bool:
        return self._presence.is_online(user_id)

    def connected_count(self) -> int:
        return self._presence.connected_count()

    def set_typing(self, room_id: str, user_id: str, typing: bool) -> None:
        self._require_member(room_id, user_id)
        self._presence.set_typing(room_id, user_id, typing)

    def typing_in(self, room_id: str) -> frozenset[str]:
        return self._presence.typing_in(room_id)

    def typing_room_count(self, user_id: str) -> int:
        return self._presence.typing_room_count(user_id)


def _demo() -> None:
    class Printer:
        def deliver(self, message: Message) -> None:
            print(f"  -> delivered to a connected member: {message.text!r}")

    chat = ChatService()
    for uid in ("ada", "grace"):
        chat.register_user(uid, uid.title())
    room = chat.direct_room("ada", "grace")
    chat.connect("grace", Printer())
    chat.send_message(room.room_id, "ada", "hi grace")
    print("grace's unread:", chat.unread_count(room.room_id, "grace"))
    chat.mark_read(room.room_id, "grace")
    print("grace's unread after reading:", chat.unread_count(room.room_id, "grace"))


if __name__ == "__main__":
    _demo()
