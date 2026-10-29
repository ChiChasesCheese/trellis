---
id: uth-compose-event-bus-5-pubsub
node: compose.event-bus
type: qa
step: 5
---
## Q
**借到面试题：应急事件发布订阅**｜Guava EventBus · 33.5.0

面试要你实现应急事件的发布订阅：订阅者登记，发布者发布；处理函数里可能再发布事件或退订。怎样借事件总线的骨架？

## A
**结构。** 同一个骨架：一张订阅表，发布时先拍快照。持锁只做两件事：给事件编号，把当前匹配的订阅者拍成一个列表；释放锁之后，再逐个调用处理函数。

**为什么。** 持锁调用处理函数时，处理函数里的再次 `publish` 会在同一线程上重新拿锁，不可重入的锁就死锁。快照还保证遍历时别人增删订阅者不会出错，这正是 Guava 里写时复制集合的作用；手写时「在锁内拷一份列表」就达到同样效果。

**坑。** 嵌套发布会让后面的订阅者先收到后发的事件（嵌套的那次先送完）；要保证有序，就得像 Guava 那样给每个线程排一个队列。

**例题：** 应急事件发布订阅（Emergency Pub/Sub）

设计应急响应系统里的发布订阅类：一些组件订阅（`subscribe`）应急事件，另一些发布（`publish`）事件，发布时通知所有匹配的订阅者。订阅者出错不能影响别人，处理函数里可能再调 `publish` 或退订。

```python
def publish(self, topic, severity, message, location=""):
    with self._lock:
        self._seq += 1
        event = EmergencyEvent(self._seq, topic, severity,
                               message, location, self._clock())
        targets = [(s, box) for s, box in self._subs.items()
                   if s.accepts(event)]
    for sub, box in targets:
        dead = sub.deliver(event) if box is None else box.offer(event)
        if dead is not None:
            self._record_dead(dead)
    return event
```
