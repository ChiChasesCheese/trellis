---
id: concurrency-bounded-queue-invariants
node: concurrency.patterns
type: qa
---
## Q
有界队列在并发中的不变量是什么？关键的临界区是什么？

## A
不变量：
- `size >= 0` 且 `size <= capacity`
- 如果 `size == 0`，消费者会阻塞
- 如果 `size == capacity`，生产者会阻塞

关键的临界区：
- 锁保护：`size`、`head`、`tail` 指针（或数组索引）
- 入队操作：增加大小，获取下一个写位置
- 出队操作：减少大小，获取下一个读位置

条件变量：
- `notEmpty`：当大小从 0 变为 1 时发出信号（通知等待的消费者）
- `notFull`：当大小从 capacity 变为 capacity-1 时发出信号（通知等待的生产者）
