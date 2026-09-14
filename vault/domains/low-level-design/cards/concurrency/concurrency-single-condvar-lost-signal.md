---
id: concurrency-single-condvar-lost-signal
node: concurrency.patterns
type: qa
---
## Q
Your bounded queue uses **one** condition variable for producers and consumers and wakes with single `signal()`. Tests pass, but under load all threads eventually park forever. Why?

## A
The signal can be **delivered to the wrong class of waiter**. A consumer taking an item signals "state changed" — but the single condition may wake *another consumer*, which re-checks "queue empty", and waits again. The wakeup intended for a producer is consumed and lost; eventually every producer and consumer is parked.

- Fix 1: **two conditions** (`notFull`, `notEmpty`) so a signal targets the right waiters.
- Fix 2: keep one condition but use **`signalAll`** — correct, at the cost of thundering-herd wakeups.

## Q zh
你的有界队列给生产者和消费者用了**同一个**条件变量，并且用单个 `signal()` 唤醒。测试能过，但压力上来之后所有线程最终都永久 park 住了。为什么？

## A zh
信号可能**被投递给了错误类别的等待者**。一个消费者取走元素后发出"状态变了"的信号 —— 但这唯一的条件可能唤醒*另一个消费者*，它重新检查"队列是空的"，然后又去等。本该给生产者的那次唤醒被消费掉、丢失了；最终每个生产者和消费者都停在 park 上。

- 修法一：用**两个条件变量**（`notFull`、`notEmpty`），让信号精确指向该被唤醒的那一类。
- 修法二：仍用一个条件，但改用 **`signalAll`** —— 正确，代价是惊群式唤醒。
