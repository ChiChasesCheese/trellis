---
id: uth-compose-event-bus-1-needs
node: compose.event-bus
type: qa
step: 1
---
## Q
**事件总线要什么，单个列表为什么不够**｜Guava EventBus · 33.5.0

发布者只管 `post(event)`，订阅者自己登记想听的事件类型。发布时怎样快速找出该通知谁？只用一个订阅者列表会卡在哪？

## A
**背景。** 事件总线（event bus）让发布者和订阅者互不认识：订阅者登记「我要听 `OrderPaid` 事件」，发布者只管发。需求写成表：

| 操作 | 要求 |
|---|---|
| `register(listener)` | 登记；同一个监听器重复登记只算一次 |
| `post(event)` | 快速找出该通知的订阅者；订阅父类型的也要收到子类型的事件 |
| `unregister` | 退订 |
| 发布的同时 | 有人登记或退订，既不能崩，也不能漏发、重发 |

**为什么。** 一个大列表：每次发布都要逐个问「你听不听这类事件」，O(订阅者总数)。改成「事件类型 → 订阅者集合」的表，发布只查几个类型。可集合在遍历时被另一个线程修改，普通集合会抛 `ConcurrentModificationException`，或让读者看到改了一半的状态。

**对应 LeetCode：** 无直接对应的题
