---
id: problems-chat-room-dm-idempotent-index
node: problems.social.chat-room
type: qa
step: 8
tags: [grown]
---
## Q
聊天室设计里，反复调用 `direct_room(a, b)`（包括参数顺序颠倒的 `direct_room(b, a)`）应该创建新房间还是返回同一个房间？用什么数据结构实现？

## A
应该返回同一个房间——私聊的身份由“这两个人是谁”决定，与调用了多少次、参数顺序无关。实现是一个 `dict[frozenset[str], str]` 索引：键是这两个用户 id 的 `frozenset`（天然无序，`{a, b}` 和 `{b, a}` 是同一个 `frozenset`），值是房间 id。第一次调用时索引里没有这个键，创建新房间并登记；之后无论以哪种参数顺序调用，都能查到同一个房间 id。选 `frozenset` 而不是排序后的元组，是因为它直接表达了“这是一个无序对”的语义，不需要额外写一行“先按字典序排序两个 id”的代码。
