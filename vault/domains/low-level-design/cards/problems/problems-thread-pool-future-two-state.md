---
id: problems-thread-pool-future-two-state
node: problems.components.thread-pool
type: qa
step: 7
tags: [grown]
---
## Q
`concurrent.futures.Future` 内部维护一个 `PENDING`/`RUNNING`/`DONE`/`CANCELLED` 四态状态机。自己实现一个线程池的 `Future`，要不要照着做一个同样的状态机？

## A
不需要，两态就够：一个 `threading.Event` 表示『完成了没有』，加两个互斥的可选字段（`_result`、`_exception`）表示『完成的方式』。`RUNNING` 这个中间状态在这个设计里没有任何代码依赖它——因为线程池不支持打断正在运行的任务（正在跑的任务不受 `shutdown` 影响），加一个从来不会被读取的状态字段只是『看起来更完整』；`CANCELLED` 同理，可以直接复用『完成、但完成的方式是异常』这条已有路径来表达『这个任务被放弃了』，不需要再造一个第三种终态。判据是：一个状态如果没有任何行为依赖它，就不该为了『看起来完整』而加进状态机——这是『更简单的答案是正确答案』的一个例子，四态状态机在这里是没有必要的过度设计。
