---
id: hl-ld03-java21-features
node: problems.ld03-async-tcp-channel
type: qa
step: 14
---
## Q
异步 TCP 通道用到哪些 Java 21 特性和 API？各自比旧写法好在哪，什么时候别用？

## A
- **虚拟线程**：`ReconnectingClient` 的管理线程 `Thread.ofVirtual().name("reconnecting-client-" + addr).start(this::run)`，直线阻塞代码，不用 `CompletableFuture` 回调链；阻塞 I/O / `Condition.await` 时卸载，不占平台线程；适合「大部分时间在等」的任务（重连管理）。**不适合**热路径（热路径上的 I/O 线程仍然用平台线程）；`synchronized` 里阻塞会钉住载体线程。
- **`ReentrantLock` + `Condition`**：旧写法 `synchronized` + `wait()/notifyAll()`；可多条件、可超时（`awaitNanos`）、虚拟线程友好；代价是手写 `try/finally`。
- **record `ChannelConfig(maxFrame, outCapacity, inCapacity)`**：紧凑构造器校验容量 ≥ `maxFrame + 4`，非法配置造不出来；`of(int maxFrame)` 工厂方法。
- **`RandomGenerator`**（Java 17）：`rng.nextLong(cap + 1)`。
- **try-with-resources / `AutoCloseable`**：测试和 bench 里的通道、服务器，按相反顺序关闭、抑制异常；`close` 可重复调用；`var` 只在右边已写类型时用。
- **`Objects.checkFromIndexSize`**：`ByteRing.writeAll` 抛标准 IOOBE，且 `off + len` 不会溢出。
- NIO：`Selector`、`SocketChannel`、`ByteBuffer.allocateDirect`、`shutdownOutput()`、`TCP_NODELAY`、`selector.wakeup()`。

**追问**：
- 为什么只用一个 `Selector` 线程：连接数多时每连接一线程撑不住（栈内存、调度开销）；这里只一条连接，但同一 Selector 可注册很多通道；虚拟线程 + 阻塞 I/O 代码少约三分之二，但延迟抖动更大；
- 能做成无锁吗：出站环和入站环都是 SPSC，可换成 ld01 里 `setRelease/getAcquire` 的环，等待改忙等或 `park`；但值不值要看测量，现在持锁期间只拷几十字节，瓶颈在 `wakeup` 和线程交接；
- 应用一直不 `poll` 会怎样：入站环满 → 停止读 → 对端被拖慢（设计意图）；同一线程既等 `offer` 空间又不 `poll` 而对端也这样会死锁；
- 为什么容量必须 ≥ `maxFrame + 4`；
- 压力测试里 `offer` 返回 false 要等 200 ms 才算真堵死。
