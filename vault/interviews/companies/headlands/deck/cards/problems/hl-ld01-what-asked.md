---
id: hl-ld01-what-asked
node: problems.ld01-spsc-channel
type: qa
step: 1
---
## Q
共享内存 SPSC 消息通道（Single-Producer Single-Consumer）题要设计什么？四个 Part 和共同约定是什么？

## A
行情进程把消息交给策略进程：只有一个写者、一个读者；**有界**（满了要明确告诉写者）；不丢、不重、不乱序（FIFO）；生产者宣布「没有更多了」之后，消费者能区分「暂时没有」和「永远没有了」（**drained**）；热路径没有锁、没有系统调用——两个进程直接读写同一块物理内存。

- **Part 1 `LongRing`**：单线程环形缓冲区，`long` 元素，2 的幂容量，head/tail 计数；
- **Part 2 `SpscLongRing`**：线程安全，`VarHandle` `setRelease/getAcquire`、cached index、填充防伪共享；
- **Part 3 `MessageRing`**：变长消息，长度前缀、8 字节对齐、回绕（PAD 记录）、`finish/isDrained`，建在 `MemorySegment` 上；
- **Part 4 `SharedChannel`**：同一个环放进内存映射文件，两个独立 JVM 进程各 `mmap` 一份。

**共同约定**：满不是错误，`offer` 返回 `false`；空：`LongQueue.poll()` 抛 `NoSuchElementException`（`long` 每个取值都可能是合法消息，没有哨兵），`MessageRing.poll()` 返回 `null`；容量必须 2 的幂：`LongQueue` 系 `[1, 2³⁰]`，`MessageRing` 系 `[16, 2³⁰]`，否则 `IllegalArgumentException`；一个对象只做一种角色（生产者调 `offer/finish`，消费者调 `poll/isDrained`），`size()`、`bytesPending()` 任何角色可调且是近似值。

考点：每个共享变量只有一个写者时 release/acquire 就够（不需要 CAS）；为什么 head/tail 自由增长；变长消息回绕的活性问题（PAD 必须单独发布）；跨进程内存序；如何测试。
