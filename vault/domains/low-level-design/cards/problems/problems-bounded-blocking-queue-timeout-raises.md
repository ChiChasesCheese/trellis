---
id: problems-bounded-blocking-queue-timeout-raises
node: problems.components.bounded-blocking-queue
type: qa
step: 4
tags: [grown]
---
## Q
有界阻塞队列的 `put(timeout=)`／`take(timeout=)` 在截止时间内没能完成，应该返回一个哨兵值（比如 `None`）还是抛异常？为什么？

## A
抛异常（本题统一抛 `QueueTimeout`）。返回哨兵值有一个致命问题：如果队列本身就用来传递 `None` 这样的合法值，调用方没法分辨『超时了』还是『确实取到一个 `None`』，这个坑在动态类型语言里格外容易踩、而且失败得悄无声息——调用方多半直接把哨兵值当正常数据往下传。抛异常让失败路径和成功路径在类型上彻底分开：调用方要么显式 `try/except`，要么让异常冒泡终止当前操作，没有『忘记检查返回值』这条隐藏分支。这也是标准库 `queue.Queue` 自己的选择——超时的 `put`/`get` 分别抛 `queue.Full`／`queue.Empty`，本题延续这个先例。
