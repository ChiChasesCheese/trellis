---
id: hi-sd-discord-messages-scylladb-5-coalescing
node: sd.in-the-wild.discord-messages-scylladb.exam
type: qa
step: 5
---
## Q
**Discord 消息：请求合并（request coalescing）**｜系统设计 · 业界案例

Discord 怎样让成千上万个读同一条消息的请求只产生一次数据库查询？为什么不直接用缓存？

## A
**场景。** 有人在大服务器发了一条 @everyone 公告，数千成员几乎同时打开频道。没有合并时，每个请求都独立向数据库要同一条消息，数千次读打到同一分区。

**做法。** 在 API 和数据库之间加一层 Rust 数据服务（业务逻辑仍留在 API）。
1. 路由：用一致性哈希，以 channel_id 作路由键，同一频道的请求到达同一个服务实例，实例增减时也基本稳定
2. 合并：实例里维护「查询键到正在进行的任务」的映射，第一个请求启动数据库查询，之后到达的相同请求加入这个任务，查询返回时把同一结果发给所有等待者

```python
async def get_message(channel_id: int, message_id: int) -> Message:
    key = (channel_id, message_id)
    # 原子地「有就复用，没有就启动」，重叠的请求共享同一次查询
    task = in_flight.get_or_start(key, lambda: spawn_query(channel_id, message_id))
    return await task.subscribe()
```

**为什么放在数据服务。** 数据库的缓存无法知道两个独立 RPC 请求的是同一条消息；数据服务看得到查询键，能在变成数据库读之前合并。

**为什么不直接缓存。** 缓存还能吸收查询结束后才到的请求，但要引入过期和失效。合并更窄：它从不返回旧结果，只让重叠的请求共享已在进行的工作。Discord 放弃了一些命中率，换来简单得多的一致性。
