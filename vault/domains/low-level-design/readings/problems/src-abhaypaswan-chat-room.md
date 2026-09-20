---
nodes: [problems.social.chat-room]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/chat-room
---
# lld-python — Chat Room

值得读：这份实现明确点名用的是**中介者模式（Mediator）**而不是观察者——`ChatRoom` 是中介者，
`User` 是同事对象，彼此不持有对方的引用，广播消息由房间的一个 `_fan_out` 方法统一路由，拉黑和
静音也在房间这一层过滤，把对等连接的 `O(N²)` 关系降成房间到用户的 `O(N)`。这个"成员不互相持有
引用"的原则本题解完全认同并采用（`ChatService`/`RoomDirectory`/`PresenceService` 互不持有对方，
只在方法参数里传递），区别在于本题解没有把它包装成一个显式的 Mediator 类——协调逻辑就写在
`ChatService.send_message` 这一个编排方法里，因为参与协调的类只有三个、职责边界早就分清楚了，
再包一层"中介者"对象只是多一层不增加信息的转发，"关键设计决策"里有一条专门讲这个取舍。direct
message 在该实现里刻意跳过历史记录以保护隐私；本题解选择让单聊复用完全相同的历史与已读机制
（"核心对象与职责"一节说明了为什么）。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/chat-room)

## Archived copy
![[src-abhaypaswan-chat-room-clip]]
%% trellis:end %%
