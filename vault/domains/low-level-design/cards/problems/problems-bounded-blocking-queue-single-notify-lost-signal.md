---
id: problems-bounded-blocking-queue-single-notify-lost-signal
node: problems.components.bounded-blocking-queue
type: qa
step: 3
tags: [grown]
---
## Q
如果坚持只用一个共享 `Condition`，还想避免惊群、于是用 `notify()` 而不是 `notify_all()`，压测下会观察到什么现象？

## A
所有线程最终都永久阻塞——这是丢信号（lost signal）的典型后果。`notify()` 唤醒的是这个条件变量上『任意一个』等待者，不区分它等的是『非满』还是『非空』。比如一个消费者刚取走元素、队列从满变成不满，它调用 `notify()`，但被唤醒的可能是另一个仍在等『非空』的消费者：它重新检查发现队列还是空的，于是又睡回去，本该被唤醒的生产者那次信号就这样凭空消失。长期运行下，生产者和消费者都会堆积在各自的等待上，系统看起来像卡死了，其实只是所有人都在等一个再也不会来的通知。修法要么是换成两个专用的 `Condition`（本题的选择，天生精确），要么退而求其次把 `notify()` 换成 `notify_all()`（不丢信号，但要接受惊群的代价）。
