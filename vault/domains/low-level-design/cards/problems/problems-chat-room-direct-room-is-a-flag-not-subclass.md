---
id: problems-chat-room-direct-room-is-a-flag-not-subclass
node: problems.social.chat-room
type: qa
step: 2
tags: [grown]
---
## Q
聊天室设计里，私聊（direct message）应该是 `Room` 的一个子类（比如 `PrivateChat(Room)`），还是同一个 `Room` 类上的一个字段？

## A
是同一个 `Room` 类加一个 `is_direct: bool` 字段，不是子类。判断依据：除了成员数量固定为二，私聊和群聊在发消息、读历史、标记已读这些行为上没有任何一行不同的逻辑——继承要买来的是多态（不同子类在同一个方法上有不同行为），这里没有任何方法需要“如果是私聊就……否则……”的分支，继承因此买不到任何好处，只会让本该共享的代码分裂成两条路径。用一个 `frozenset({a, b})` 做键的索引让 `direct_room(a, b)` 幂等（反复调用返回同一个房间），私聊和群聊此后走的是完全相同的 `send_message`/`history` 代码路径。
