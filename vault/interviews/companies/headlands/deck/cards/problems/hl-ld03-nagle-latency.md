---
id: hl-ld03-nagle-latency
node: problems.ld03-async-tcp-channel
type: qa
step: 12
---
## Q
Nagle 算法和 `TCP_NODELAY` 是什么？这个通道的吞吐、往返延迟实测是多少，多出来的延迟来自哪里？

## A
**Nagle**：把小写合并，等 ACK 或凑够一个段再发，省带宽，代价是延迟；与对端**延迟确认**相撞会产生约 **40 ms** 停顿（写-写-读模式）。消息通道必须 **`TCP_NODELAY`**（关闭 Nagle）。我们已在应用层批量（出站环 + 一次 `write` 发多条），不需要 Nagle。

**实测**（回环 127.0.0.1，32 字节消息含 4 B 头，各跑 3 次，macOS）：
- 吞吐：200 万条中位数 86–114 ms，即 17.5–23.3 M 条/s（约 630–840 MB/s），瓶颈是批量系统调用和线程交接，不是协议；
- 往返延迟，本通道：p50 36 µs，p99 46 µs，p99.9 52–53 µs，max 147–165 µs；
- 往返延迟，裸阻塞 `SocketChannel` 乒乓：p50 12.4 µs，p99 18 µs，p99.9 23 µs，max 59–121 µs；
- 多出的约 **24 µs** 来自**线程交接**：一次往返里应用线程 → I/O 线程（`wakeup` 系统调用 + 线程被唤醒）、I/O 线程 → 应用线程（`signalAll` + `unpark`）各两次。这正是低延迟系统「热路径 run-to-completion，不要线程交接」的原因，也是常让应用线程自己轮询网卡（内核旁路）的原因。这套通道为**吞吐和易用**设计，不是 µs 级往返。
- 数字来自 macOS 回环，Linux 上不同。

**内存**：出站环 + 入站环 + 2 × 16 KB 中转缓冲，不随消息数量增长。`offer/poll` 持锁期间只做内存拷贝；每条消息经历两次拷贝（进环、出环）和一次中转缓冲。

**虚拟线程 + 阻塞 I/O 的备选设计**：每连接两条虚拟线程（读、写），阻塞 `SocketChannel` + 有界 `ArrayBlockingQueue`：
- 读线程 `readNBytes(header, 0, 4)` 阻塞凑齐 4 字节，校验长度，`readNBytes(len)`，`inbox.put(payload)`（满了就阻塞 → 不再读 → TCP 窗口缩小，天然入站背压）；写线程 `outbox.take()` 后阻塞 `write`（部分写由阻塞 API 自动循环处理）；
- 优点：没有 `Selector`、兴趣集、`wbuf`、`wakeup`，代码量约 NIO 版的三分之一；缺点：每连接两条线程调度有抖动，「满了返回 false」靠 `ArrayBlockingQueue.offer` 按**消息数**而非**字节数**限界，难精细控制延迟；
- 选择：连接数很大、延迟不极端 → 虚拟线程；需绑核、批处理、极低延迟 → `Selector` 或内核旁路。

其他变体：多路复用服务端（一个 Selector 管 N 个连接）、心跳 / 空闲超时、压缩 / 批量（Nagle 的应用层版本，延迟 vs 吞吐）、TLS、零拷贝（`FileChannel.transferTo`、直接缓冲区、`MemorySegment`）。
