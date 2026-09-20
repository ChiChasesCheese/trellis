---
id: problems-bounded-blocking-queue-close-no-event
node: problems.components.bounded-blocking-queue
type: qa
step: 6
tags: [grown]
---
## Q
`close()` 需要『置位一个已关闭标志 + 唤醒所有等待者』，`threading.Event` 看起来正好是这个封装。为什么本题的有界阻塞队列没有用 `Event`，只用了一个受锁保护的 `bool`？

## A
因为已有的两个 `Condition` 加一把锁已经能完整表达这个语义，`Event` 反而会制造新问题：`put`/`take` 已经在各自的 `Condition` 上等待谓词，没有办法『同时』也在一个独立的 `Event` 上等——要么额外起一个线程去桥接两套等待原语（复杂度陡增，还多一条竞态路径），要么在 `while` 循环里加一条『或者 `Event` 被置位了』的检查，那就退化成直接查 `self._closed`，`Event` 成了多余的一层包装。真正的实现只需三行：在持有锁时把 `_closed` 置 `True`，依次对两个 `Condition` 调用 `notify_all()`——这本来就要在同一次加锁里做完，不然『置位』和『唤醒』之间可能被另一个线程插队产生新的竞态。这是『更简单的答案就是正确答案』的一个例子：先看现有的锁和条件变量能不能覆盖需求，而不是看到一个语义相似的标准库类型就急着引入它。
