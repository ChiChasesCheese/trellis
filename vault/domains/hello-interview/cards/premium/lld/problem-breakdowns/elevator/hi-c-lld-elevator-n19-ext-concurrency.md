---
id: hi-c-lld-elevator-n19-ext-concurrency
node: lld.problem-breakdowns.elevator.notes
type: qa
step: 19
---
## Q
**电梯系统 · 扩展三：多个呼叫同时到达**｜摘要 · 追问

真实系统里呼叫是并发到达的，会出现哪两个问题？怎么解？

## A
- **问题一：** 两个呼叫同时进入 `request_elevator`，都选中同一部"空闲"电梯；"选"和"加"必须是一个原子操作。
- **问题二：** `step()` 一边遍历请求集合并删除，另一边 `add_request` 正在加入，会发生并发修改。
- **解法一：加锁。** `request_elevator` 和 `step()` 用同一把锁，互斥访问；简单正确，但呼叫要等 `step` 做完，反之亦然。
- **解法二：并发队列。** `add_request` 只写线程安全的队列，`step()` 开头把队列倒入工作集合；写入方和 `step` 各管各的数据，完全不需要锁，也没有争用。
- **取舍：** 锁更好讲；队列更优雅，不阻塞呼叫。两种都是好答案。
