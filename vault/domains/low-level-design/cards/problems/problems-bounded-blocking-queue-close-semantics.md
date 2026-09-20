---
id: problems-bounded-blocking-queue-close-semantics
node: problems.components.bounded-blocking-queue
type: qa
step: 5
tags: [grown]
---
## Q
有界阻塞队列的 `close()` 之后，`put` 和 `take` 的行为应该分别是什么？为什么不能让两者对称（比如都立刻失败，或都继续工作到队列变空）？

## A
`close()` 之后，`put` 立即失败（哪怕此刻明明有空位），`take` 继续把关闭前已经放进去的元素取完，直到确认排空才失败。两者故意不对称，因为它们回答的是两个不同的问题：`close()` 的语义是『停止接收新工作』，不是『丢弃已经接受的工作』。如果 `put` 在有空位时还继续成功，『关闭』就失去了意义；如果 `take` 在关闭后立即失败，关闭前排队等待处理的任务会被无声丢弃——对于队列背后往往是网络连接或后台任务这样的真实场景，这是不可接受的数据丢失。常见错误是把 `close()` 实现成『清空队列』，那混淆了『以后还能不能 put』和『现在队列里还有没有东西』这两件独立的事。
