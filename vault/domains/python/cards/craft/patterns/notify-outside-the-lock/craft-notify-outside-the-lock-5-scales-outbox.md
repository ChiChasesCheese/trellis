---
id: craft-notify-outside-the-lock-5-scales-outbox
node: craft.patterns.notify-outside-the-lock
type: qa
step: 5
---
## Q
**锁内记事件、锁外派发 · 从事件列表到发件箱（outbox）**｜架构

进程内，事件列表在锁内追加、锁外派发。放到服务里，「状态变更」是数据库事务，「通知」是发消息到 Kafka。如果在事务里直接发消息，会有什么问题？同样的结构怎么搬过去？

## A
**要点。** 同构：事务内只写状态和一行「待发事件」（发件箱表 outbox），事务提交后由中继（relay）把事件发出去并标记已发。事务里不调外部系统，原因和锁里不调回调一样：外部系统慢、失败、或者回头读自己。

```python
with db:                                # 一个事务
    db.execute("INSERT INTO orders VALUES (1, 'PAID')")
    db.execute("INSERT INTO outbox (topic, payload) VALUES ('order.paid', '{...}')")

def relay():
    for row_id, topic, payload in db.execute("SELECT ... WHERE sent=0"):
        publish(payload)                # 事务外调用外部系统
        with db:
            db.execute("UPDATE outbox SET sent=1 WHERE id=?", (row_id,))
```

relay 在发出之后、标记之前崩溃，重启后再跑一次，实际输出：

```
发布次数 2 -> 至少一次，消费者要去重
```

**变化。** 内存里列表和状态在同一个锁下，要么都在要么都不在（崩溃时一起消失）；数据库里靠同一个事务提供同样的保证。但是进程可以在「发出」和「标记」之间崩溃，所以送达变成至少一次（at-least-once），消费者要靠事件 ID 去重（见幂等键）。

**信号。** 状态变化后要通知别的服务，而且不能「状态改了通知丢了」或「通知发了状态没改」。
