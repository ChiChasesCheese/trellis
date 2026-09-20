---
nodes: [problems.social.chat-room]
url: https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/online_chat
---
# system-design-primer — Object-Oriented Design: Online Chat

值得读：`system-design-primer` 里唯一一份 Python 的聊天室骨架，常被当作这道题的起点引用。它用
**继承**表达单聊和群聊——`PrivateChat` 和 `GroupChat` 都是 `Chat` 的子类，`User` 各自维护一张
`friend_ids_to_private_chats` 和 `group_chats_by_id`；消息用创建时的时间戳排序，`message_user`/
`message_group` 只有方法签名和 `pass`，投递、持久化都留空。本题解用一个 `is_direct: bool` 字段
而不是子类区分单聊群聊（两者除了成员数没有任何字段或行为差异，继承不出的额外语义），并且用
**服务端到达顺序**（`seq`）取代客户端时间戳排序——"关键设计决策"第一条就是这一点。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/online_chat)

## Archived copy
![[src-donnemartin-chat-room-clip]]
%% trellis:end %%
