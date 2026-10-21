# ld03 · 异步 TCP 消息通道（Asynchronous TCP Message Channel）

## 背景

行情进程和策略进程在两台机器上，或者订单网关连接交易所——数据通过一条 TCP 连接流动。TCP 提供**可靠的有序字节流**，不是消息流：

* 你 `write` 了两条各 10 字节的消息，对端可能一次 `read` 到 20 字节（合并），也可能先读到 13 字节、再读到 7 字节（切开，**在消息中间**）；
* `write` 在发送缓冲区快满时只写进去一部分（**部分写**），剩下的要等"可写"再继续；
* 对端读得慢，内核缓冲区装满，TCP 窗口缩到 0，你的 `write` 写不进去——**背压**一路传回你的程序；
* 连接可能断：对端进程退出、网络中断、被 RST。

题目要你在字节流之上做一个**有界**的消息接口：`offer(消息)` 发、`poll()` 收，满了就说"满了"，而不是无限堆内存或阻塞死。

## 读题前你需要知道

最少要先懂：

* **TCP / 套接字 / Nagle / `TCP_NODELAY`**：套接字是内核给进程的网络端点；TCP 在两端之间提供可靠、有序的字节流。Nagle 算法会把小包攒起来再发以省带宽，代价是延迟；低延迟场景开 `TCP_NODELAY` 关掉它；
* **NIO `Selector` 与 `ByteBuffer`**：非阻塞 `SocketChannel` 的读写立刻返回（可能读 / 写 0 字节或一部分）；`Selector` 让一个线程等待多个通道的"可读 / 可写"就绪事件，用兴趣集（interest ops）声明关心哪些事件。`ByteBuffer` 带 `position` / `limit`，写完要 `flip()` 才能读；
* **虚拟线程 + 阻塞 I/O**：另一种写法——每个连接两条虚拟线程，直接用阻塞读写，代码更直，不需要 `Selector`；
* **环形缓冲区**：固定容量（2 的幂）的字节数组，`head` / `tail` 计数只增不减，下标 = 计数 `& mask`，写到末尾回绕时分两段拷贝；
* `record`：不可变值类型，自动生成 `equals` / `hashCode`；并发原语：`ReentrantLock` / `Condition`、`volatile` 等。

## 概述

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `ByteRing`、`FrameCodec`、`FrameDecoder` | 纯内存：字节环形缓冲区；4 字节大端长度前缀成帧；增量解码器（任意切分的字节块） | 回绕时分两段拷贝；`writeAll` 全有或全无；非法帧头只看头就报错；解码器自己也是有界的（入站背压） |
| 2 | `TcpMessageChannel`、`MessageServer` | 一条连接上的有界消息通道：一个 `Selector` I/O 线程 + 出站环 + 入站解码器；部分读写；EOF；`finishSending`（半关闭）；`close` | 兴趣集（interest ops）管理；唤醒 selector；EOF 在帧中间；半关闭语义 |
| 3 | （同上，行为） | 背压与有界性：接收方不读时 `offer` 返回 `false`；入站环满时停止读 socket；最小缓冲区压力测试 | 暂停读之后谁来恢复；`poll` 要唤醒 I/O 线程；容量恰好 `maxFrame + 4` 不死锁 |
| 4 | `Backoff`、`ReconnectingClient` | 指数退避；断线自动重连；断线期间有界的 pending 队列 | "已交给旧连接的消息会丢"的诚实语义；退避重置；close 时停止重连 |

所有类在默认包。starter 里已给出 `ChannelConfig` 与 `FrameException`；其余类的方法体是 `throw new UnsupportedOperationException("TODO")`。

## 共同约定

* **帧格式**：`[len:int32 大端][payload:len 字节]`。`len` 的合法范围 `[0, maxFrame]`；空负载合法。
* `ChannelConfig(maxFrame, outCapacity, inCapacity)`：字节数；`outCapacity`、`inCapacity` 必须 `>= maxFrame + 4`（否则一条最大的消息永远凑不齐 / 放不进），紧凑构造器校验。
* 所有测试在 `127.0.0.1` + 内核分配的临时端口上跑。不允许依赖 `Thread.sleep` 的时序来判断**正确性**（只允许用截止时间的轮询等待"最终发生"的事件）。
* 消息是不可变的 `byte[]`；通道不复制调用方之后修改的内容之外的东西——`offer` 返回前已经把字节拷进出站环。

## Part 1 · 缓冲区与成帧（纯内存）

```java
public final class ByteRing {
    public ByteRing(int capacity)                              // > 0，任意正整数（不要求 2 的幂）
    public int capacity(); public int size(); public int free(); public boolean isEmpty()
    public int write(ByteBuffer src)                           // 尽量多写，返回写入数；src.position 前进同样数量
    public int read(ByteBuffer dst)                            // 尽量多读
    public boolean writeAll(byte[] src, int off, int len)      // 全有或全无
    public int peekInt(int offset); public int peekInt()       // 大端，不消费；不足 4 字节 → IllegalStateException
    public byte[] take(int n); public void skip(int n)         // 不足 → IllegalStateException（状态不变）；n<0 → IAE
    public void clear()
}
public final class FrameCodec {
    public static final int HEADER = 4;
    public static boolean encode(ByteRing out, byte[] payload, int maxFrame)   // 放不下 false（不留半个头）；超 maxFrame → IAE
}
public final class FrameDecoder {
    public FrameDecoder(int maxFrame, int capacity)            // capacity < maxFrame + 4 → IAE
    public int feed(ByteBuffer src)                            // 返回实际消费数，满了可能小于 remaining
    public byte[] next()                                       // 不够一帧 null；非法帧头 → FrameException（粘性）
    public boolean hasFrame(); public int buffered(); public int free()
    public boolean hasTruncatedTail()                          // 完整帧之后是否还有一截不完整的尾巴
}
```

* 回绕：写入 / 读出跨过数组末尾时要拆成两段拷贝。
* **非法帧头**（`len < 0` 或 `len > maxFrame`）在**只看到 4 字节头**时就必须报错：不能等 `len` 个字节凑齐（`2^31 − 1` 永远凑不齐，还会诱导你分配 2 GB）。报错后解码器**粘性失败**：流已经失去同步，没有"跳过这一帧继续"。
* `feed` 是有界的：环里放不下的字节**不消费**，调用方要先 `next()` 腾空间再继续喂——这是入站背压在最低层的体现。

## Part 2 · `TcpMessageChannel`（一条连接）

```java
public final class TcpMessageChannel implements AutoCloseable {
    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg) throws IOException
    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg, int timeoutMs) throws IOException
    public static TcpMessageChannel wrap(SocketChannel connected, ChannelConfig cfg) throws IOException   // 接管已连接的 socket
    public boolean offer(byte[] msg)                            // 非阻塞；false = 出站缓冲区放不下
    public boolean offer(byte[] msg, long timeoutMs) throws InterruptedException
    public byte[] poll()                                        // 非阻塞；没有返回 null
    public byte[] poll(long timeoutMs) throws InterruptedException
    public void finishSending()                                 // 刷完后发 FIN（半关闭）
    public void close()                                         // 立刻关，丢弃未发送数据，幂等
    public boolean isOpen(); public boolean isPeerClosed(); public boolean isDrained()
    public Throwable failure(); public int unsentBytes(); public boolean awaitClosed(long timeoutMs) throws InterruptedException
    public InetSocketAddress localAddress() throws IOException; public SocketAddress remoteAddress() throws IOException
}
public final class MessageServer implements AutoCloseable {
    public MessageServer(int port, ChannelConfig cfg) throws IOException      // 127.0.0.1；port 0 = 临时端口
    public int port(); public InetSocketAddress address()
    public TcpMessageChannel accept(long timeoutMs) throws InterruptedException   // 超时 null
    public void close()
}
```

### 语义

* **一个 I/O 线程 + 一个 `Selector`**（题目要求 NIO；虚拟线程 + 阻塞 I/O 是备选）。应用线程只和两个有界缓冲区打交道，**系统调用都在 I/O 线程里**，且不持有锁。
* `offer`：消息超过 `maxFrame` → `IllegalArgumentException`；通道已 `close` / 已 `finishSending` / 已失败 → `IllegalStateException`（与"暂时满了"的 `false` 区分）；放得下 → 编码进出站环并返回 `true`（保证按序写进 socket，除非连接失败）。
* **部分写**：`write` 只写了一部分时，剩余数据必须保留（连同位置），等下一次 `OP_WRITE`。出站环是 `ByteRing`，经一个中转缓冲区进入 socket。
* **部分读**：读到的字节喂给 `FrameDecoder`；`poll` 只在凑齐一整帧时返回。
* `poll()` / `poll(timeout)`：对端关闭或本端关闭之后，**已缓冲的完整消息仍可取**。帧头非法 ⟹ `poll` 抛 `FrameException`，通道失败（`failure()` 是它）。
* **EOF（对端关闭）≠ 本端关闭**：`isPeerClosed()` 变 `true`，之后仍可 `poll` 剩余消息、仍可 `offer`（半关闭）。`isDrained()` = 不会再有新消息且缓冲区里没有完整消息。**EOF 恰好落在一帧中间** ⟹ 流被截断：`failure()` 是 `EOFException`，通道关闭，但之前收齐的完整帧仍可取。
* `finishSending()`：之后 `offer` 抛 `IllegalStateException`；已接受的消息刷完后 `shutdownOutput()`（发 FIN）；当本端已发 FIN **且**对端也关闭，通道自动关闭（`failure()` 为 `null`）。
* `close()`：立刻关闭，未发送的数据丢弃；唤醒所有阻塞在 `poll(timeout)` / `offer(msg, timeout)` / `awaitClosed` 的线程。
* `TCP_NODELAY` 必须开（关闭 Nagle，小消息不被延迟合并）。

## Part 3 · 背压与有界性

* **出站**：对端不读 ⟹ 内核发送缓冲区满 ⟹ `write` 返回 0 ⟹ 出站环渐满 ⟹ `offer` 返回 `false`。`offer(msg, timeoutMs)` 等到放得下或超时。**接受过的每一条消息，在对端开始读之后必须按序、不丢、不重地到达**。
* **入站**：应用不 `poll` ⟹ 入站环满 ⟹ I/O 线程**停止监听 `OP_READ`**（不再从内核取数据）⟹ 内核接收缓冲区满 ⟹ TCP 窗口为 0 ⟹ 对端 `write` 写不出去。应用 `poll` 腾出空间后，**必须唤醒 I/O 线程**恢复读（`poll()`（非阻塞）和 `poll(timeout)` 都要）。
* **最小缓冲区**：`inCapacity = outCapacity = maxFrame + 4` 时仍然必须工作（2 万条随机长度的消息，每条都在环的回绕边界上被切开）。
* 有界性：出站环 + 内核缓冲区 + 入站环之外，不能有任何随消息数增长的内存。

## Part 4 · 重连

```java
public final class Backoff {
    public Backoff(long initialMs, long maxMs, int multiplier)    // 初始 > 0；max >= initial；multiplier >= 1
    public long next()                                            // initial, initial*m, … 封顶 max，不溢出
    public long next(RandomGenerator rng)                         // 全抖动：[0, next()] 均匀
    public void reset()
}
public final class ReconnectingClient implements AutoCloseable {
    public ReconnectingClient(InetSocketAddress addr, ChannelConfig cfg, Backoff backoff)
    public boolean offer(byte[] msg)          // false = pending 满了；close 之后 IllegalStateException
    public byte[] poll()                      // 当前连接上的入站消息；断线期间 null
    public boolean isConnected(); public int connectCount(); public int failedAttempts()
    public long abandonedBytes(); public int pendingBytes(); public void close()
}
```

### 语义

* 后台一个线程（本参考用虚拟线程）：连接 → 成功后把 `pending` 里的消息按序搬进当前通道 → 通道断开（`!isOpen()` 或 `isPeerClosed()`）⟹ 丢掉旧通道 ⟹ 退避后重连。连接失败 ⟹ `failedAttempts++`，按 `Backoff` 等待再试；连接成功 ⟹ `backoff.reset()`。
* `offer` 永远先进 `pending`（保证顺序），`pending` 有界：已编码字节（`4 + len` 之和）不得超过 `cfg.outCapacity()`，放不下返回 `false`。断线期间 `offer` 仍然成功（直到装满）。
* **诚实的语义**：已经交给旧通道（进了它的出站环 / 内核缓冲区）的消息，连接断掉时**可能丢失**。TCP 只保证连接存续期间的有序不丢，不保证对端应用处理了；要不丢必须有应用层序号 + 确认 + 重传（at-least-once + 去重）。本类是 at-most-once 的尽力而为，丢失字节数累计在 `abandonedBytes()`。
* `close()`：关闭当前通道、唤醒管理线程、之后不再重连、`offer` 抛异常、幂等。

## 样例

```java
var cfg = new ChannelConfig(1024, 16 * 1024, 16 * 1024);
try (var srv = new MessageServer(0, cfg);
     var client = TcpMessageChannel.connect(srv.address(), cfg)) {
    var server = srv.accept(5_000);
    client.offer("hello".getBytes());                  // true
    server.poll(5_000);                                // "hello"
    server.offer("world".getBytes());
    client.poll(5_000);                                // "world"

    for (int i = 0; i < 1000; i++) client.offer(new byte[10]);
    client.finishSending();                            // 刷完后发 FIN
    // server 一直 poll(...) 直到返回 null，然后 server.isDrained() == true，server.isPeerClosed() == true
}

var d = new FrameDecoder(10, 64);
d.feed(ByteBuffer.wrap(new byte[]{0, 0, 0, 3, 'a'}));   // 头 + 1/3 的负载
d.next();                                               // null（不完整）
d.feed(ByteBuffer.wrap(new byte[]{'b', 'c', 0, 0}));
d.next();                                               // "abc"；剩下两个字节是下一帧的半个头
d.hasTruncatedTail();                                   // true
```

## 边界清单（隐藏测试会打）

| 类别 | 例子 |
|---|---|
| 环 | 容量 1；写满再写（部分写）；回绕分两段；`writeAll` 放不下一个字节都不写；`peekInt` 跨回绕、符号位；随机操作对照 `ArrayDeque<Byte>` |
| 成帧 | 空负载；恰好 `maxFrame`；`maxFrame + 1`；负长度；`0x7FFFFFFF`；字节逐个到达；在**每一个**切分点切开三条消息；解码器满了 `feed` 返回部分；随机切块 100 条 × 40 轮 |
| 截断 | 半个头；头完整负载不全；完整帧后接半个头；非法头不算截断 |
| 通道 I/O | 空消息、最大消息、几 MB 大消息（部分写）、1 万条按序、双向同时 5,000 条、裸 socket 逐字节发送、一次写入"两条半" |
| 错误 | 非法帧头 ⟹ `FrameException` + 通道失败 + 之前的消息仍可取；对端在帧中间关闭 ⟹ `EOFException`；`close` 后 `offer` 抛异常；`close` 唤醒阻塞的 `poll(30_000)` |
| 半关闭 | `finishSending` 后 `offer` 抛；对端先收齐全部再看到 EOF；对端仍能回话；双方 `finishSending` ⟹ 两端关闭且 `failure() == null` |
| 背压 | 接收方不读 ⟹ `offer` 最终返回 `false` 且有界；开始读后全部按序到达、数量相等；带超时的 `offer` 在对端读之后成功；最小缓冲区 2 万条；自旋的非阻塞 `poll()` 也能恢复暂停的读 |
| 重连 | 服务端踢掉连接 ⟹ 自动重连并继续收发；服务端整个下线 ⟹ 断线期间 `offer` 成功、重新上线（同一端口）后按序全部到达；`pending` 有界（10 条 × 50 字节 = 500）；`close` 后不再重连；失败几次后成功，再被踢，重连应当从最短退避开始 |
| 退避 | `100,200,400,800,1000,1000…`；`reset`；`Long.MAX_VALUE` 上限不溢出；`multiplier = 1`；全抖动在 `[0, 当前上限]`；非法参数 |
| 性能 | 100 万条 32 字节经环 + 解码器 < 2 s；20 万条经回环 < 5 s（实际远低于 1 s） |

## 相关变体

* **虚拟线程 + 阻塞 I/O 版本**：每个连接两条虚拟线程（读、写），阻塞 `SocketChannel` 读写 + 有界 `ArrayBlockingQueue`；代码更直，延迟略高。
* **多路复用的服务端**：一个 `Selector` 管 N 个连接（例如回显服务器）。
* **应用层确认 + 序号 + 重放**：给每条消息一个序号，对端周期性确认；断线重连时从对端的"已收到序号"继续——at-least-once，加去重得到 effectively-once。
* **心跳 / 空闲超时**：检测"半开连接"（对端机器掉电，TCP 不会通知）。
* **压缩 / 批量**：多条小消息合并成一次 `write`（Nagle 的应用层版本，延迟 vs 吞吐）。
* **TLS**：`SSLEngine` 的 `wrap/unwrap` 与部分 I/O 的交互。
* **零拷贝**：`FileChannel.transferTo`、直接缓冲区、`MemorySegment`。
* C++ 版：`epoll` + 环形缓冲 + `recv/send` 返回 `EAGAIN`；追问边缘触发 vs 水平触发。

## 考什么

1. **TCP 是字节流**：消息边界必须自己带；部分读 / 部分写是常态而不是异常。
2. **有界 = 每一层都有上限**，满了向上游说"满了"，且这条信息一路传到对端（背压穿过内核）。
3. **`Selector` 的纪律**：谁修改兴趣集、怎么唤醒、"就绪不等于完成"；暂停读之后谁来恢复。
4. **正确的失败语义**：EOF 在帧中间、非法帧头、半关闭、断线时哪些数据可能丢——说出来比假装不丢更重要。
5. **并发正确性的测试方法**：截止时间轮询而非 `sleep`；确定性消息（序号可校验）；最小缓冲区压力。
