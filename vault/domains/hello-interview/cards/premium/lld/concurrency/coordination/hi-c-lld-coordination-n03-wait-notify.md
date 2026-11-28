---
id: hi-c-lld-coordination-n03-wait-notify
node: lld.concurrency.coordination.notes
type: qa
step: 3
---
## Q
**并发协调 · 条件变量：wait/notify**｜摘要 · 必会

等待与通知（condition variable）怎么避免轮询？为什么条件必须放在 `while` 里检查？

## A
- **机制：** 一把锁加一个附着其上的条件变量。线程发现条件不满足时调用 `wait`，它原子地释放锁并让线程完全休眠，不占 CPU；另一个线程改变状态后调用 `notify`，被唤醒的线程要先重新拿到锁才能继续。
- **模板：** `with cond: while not ready: cond.wait(); ...; cond.notify_all()`。
- **为什么必须 `while`：** 被唤醒到重新拿到锁之间，别的线程可能已经把东西拿走了；而且系统还可能出现没有任何通知的虚假唤醒。所以醒来后要重新检查条件。
- **对比轮询：** 睡眠轮询要么浪费 CPU（睡得短）要么延迟高（睡得长）；wait/notify 空闲时零 CPU，来活立刻被唤醒。
- 面试里很少直接用，了解原理即可。
