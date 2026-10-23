---
id: hft-machine-memory-ordering-volatile-vs-release
node: machine.memory-ordering
type: qa
step: 4
---
## Q
Java 里往 SPSC（单生产者单消费者）队列里发布一个序号，用 `volatile` 写和用 `VarHandle.setRelease` 有什么区别？为什么 Disruptor 和 Agrona 偏好后者？

## A
两者的区别在于写入之后要不要一个昂贵的栅栏：

- **`volatile` 写**（顺序一致，`seq_cst`）：保证这次写和之后的读不被重排。x86 上的实现是在写之后加一条 `lock addl` 之类的指令（禁止"写后读"重排的 StoreLoad 栅栏），约 20 个周期，还要清空存储缓冲区。
- **`setRelease`**（release 语义）：只保证"这次写之前的所有写，对看到这个值的线程都可见"。在 x86 上就是一条普通的 `mov`，**不加栅栏**，几乎免费。`AtomicLong.lazySet` 是同类的老写法。

SPSC 队列发布序号时，只需要"数据先写好，再让消费者看到序号"，这正是 release 的语义；不需要"我的写要先于我的下一次读"这种更强的保证。所以用 `setRelease` 对应读端的 `getAcquire` 就够了，省掉每条消息约 5–10 ns。

在每秒百万条消息的路径上，这是实实在在的差别；代价是代码更难读、更难证明正确，要靠严格的测试。
