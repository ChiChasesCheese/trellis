---
id: problems-bounded-blocking-queue-two-conditions-vs-one
node: problems.components.bounded-blocking-queue
type: qa
step: 2
tags: [grown]
---
## Q
一个有界阻塞队列里，`put` 等『不满』、`take` 等『不空』是两类不同的等待者。为什么最终选择两个 `Condition`（`_not_full`、`_not_empty`）共享同一把锁，而不是只用一个共享的 `Condition`？

## A
单个 `Condition` 配精确的 `notify()` 会丢信号：`notify()` 唤醒的是『任意一个』在这个条件变量上等待的线程，不区分它在等哪一类事——一个消费者取走元素腾出空位后调用 `notify()`，被唤醒的却可能是另一个还在等『非空』的消费者，它发现队列仍空就又睡回去，本该被唤醒的生产者那次信号就丢了。改用 `notify_all()` 能避免丢信号，但每次状态变化都要惊动全部等待者，造成『惊群』（thundering herd）：十个等待非空的消费者里，生产者放进一个元素后全部十个被唤醒，九个重新检查发现轮不到自己，白白抢一次锁又睡回去。两个 `Condition` 共享同一把 `Lock` 构造（`threading.Condition(lock)`），各自维护自己的等待队列，`put` 结束后只精确 `notify(self._not_empty)`，`take` 结束后只精确 `notify(self._not_full)`——既不丢信号也不惊群，而且判断谓词、修改队列、精确唤醒这三步依然发生在同一次加锁里，不引入新的死锁面。
