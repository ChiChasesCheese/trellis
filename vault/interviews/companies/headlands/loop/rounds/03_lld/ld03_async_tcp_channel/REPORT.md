# ld03 · REPORT

## 概要

「异步 TCP 消息通道」出自 FastPrep 的 Low-level design 题（2023-03-09），摘要为「bounded message API over one TCP session, with local circular buffers, partial-I/O framing…」。

面试官想看五点：
1. 知道 TCP 是字节流，消息边界要自己加，部分读、部分写是常态；
2. 有界：每一层都有上限，满了要告诉上游，背压能一路传过内核；
3. `Selector` 的使用纪律：兴趣集怎么设、何时唤醒、「就绪」不等于「完成」，以及暂停读之后由谁来恢复；
4. 失败语义说清楚：EOF 出现在帧中间、半关闭、重连后哪些数据可能丢；
5. 怎么把并发 I/O 代码测得稳定。

讲义：`study/30-articles/ld03_async_tcp_channel.md`。

## 来源与置信度

置信度：中。只有 FastPrep 一个来源，而且只有标题和摘要。1p3a 974931（同一天，内容是 C++ 版本差异和 IPC 方法）可能相关，不计入 #refs。

(reconstructed)：四个 Part 的划分、帧格式（4 字节大端长度前缀）、`offer` / `poll` 的语义、出站和入站的背压规则、`finishSending`（半关闭）规则、重连时 pending 的语义，以及「已交给旧连接的消息可能丢失」。能确定的只有：一条 TCP 会话、有界的消息 API、本地环形缓冲区、处理部分 I/O 的分帧。

## 逐 Part 思路

1. **ByteRing / FrameCodec / FrameDecoder**（纯内存，不涉及网络）
   - 字节环用 `head + size` 表示，容量可以是任意正整数；回绕时一次拷贝拆成两段。`writeAll` 要么全写进去，要么一个字节都不写。`peekInt` 按大端读，能跨过回绕点。
   - 帧 = 4 字节大端长度 + 负载，负载为空也合法。`encode` 放不下时返回 false，不会留下半个帧头。
   - 解码器自己也有界，容量不小于 `maxFrame + 4`。`feed` 只消费放得下的那部分字节，这是入站背压的最底层。`next` 要等一帧凑齐才交付。只要看到 4 字节帧头，就立刻拒绝 `len < 0` 或 `len > maxFrame` 的帧，而且一旦失败就保持失败状态。
   - `hasTruncatedTail` 用来在 EOF 时判断流是不是在帧中间被截断。
2. **TcpMessageChannel**：一个跑 `Selector` 的 I/O 线程，加一个出站 `ByteRing`、一个入站 `FrameDecoder`，以及一把 `ReentrantLock` 和 `Condition`。所有系统调用都在锁外执行。
   - 每轮循环在锁内重新计算兴趣集：对端没关闭且入站环有空位时才注册 `OP_READ`；`wbuf` 里还有剩余数据或出站环不空时才注册 `OP_WRITE`。
   - `selector.wakeup()` 是粘性的：没在 select 时调用，下一次 select 会立即返回。`selectedKeys().remove(key)` 保证只有本轮真正被选中时才去读 `readyOps`。
   - 部分写：先把环里的字节搬到 16 KB 的直接缓冲区 `wbuf`；一次没写完，就等下一次 `OP_WRITE`。部分读：`rbuf` 的读取上限取入站环的剩余空间，保证 `feed` 一定吃得下。
   - `offer` 返回 false 表示暂时满了；通道已不可用则抛 ISE。只有出站环从空变成非空时才调用 `wakeup`。
   - EOF：设置 `peerClosed`。如果 EOF 出现在帧中间，就以 `EOFException` 失败，但已经收齐的完整帧仍然可以取走。
   - `finishSending`：把出站数据刷完后调用 `shutdownOutput`。本端已发 FIN 且对端也 EOF 时，自动关闭通道。`close` 立即关闭，并唤醒所有等待者。
   - `MessageServer`：一个接受连接的线程，加一个阻塞队列。
3. **背压**：整条链路是这样传导的——入站环满了 → 不再注册 `OP_READ` → 内核接收缓冲区填满 → TCP 窗口降到 0 → 对端 `write` 返回 0 → 对端出站环填满 → 对端 `offer` 返回 false。
   - 暂停读的时候置位 `readPaused` 标志。`poll()` 和 `poll(timeout)` 取走消息时清掉这个标志并调用 `wakeup`，I/O 线程才会重新打开读。
   - 即使缓冲区开到最小（`maxFrame + 4`），传输也不会死锁。
4. **Backoff / ReconnectingClient**
   - `Backoff` 用 `current > max/mult ? max : min(max, current*mult)` 防止乘法溢出；`next(RandomGenerator)` 实现全抖动（full jitter）。
   - 客户端的 `offer` 总是先放进有界的 pending 队列，按 `4 + len` 字节计数，上限为 `outCapacity`。
   - 一条虚拟线程负责：连接；连上后 `backoff.reset()`；把 pending 按顺序搬进通道（每 10 ms 或被唤醒时重试）；发现通道断开（`!isOpen` 或 `isPeerClosed`）时，把已交给旧通道的字节记入 `abandonedBytes`，然后退避、重连。
   - 语义如实说明：已经交给旧通道的字节可能丢失，这是 at-most-once 的尽力而为。

## 隐藏测试会打的坑

* 以为一次 `read` 就是一条消息。实际可能读到半个帧头，也可能一次读到「两条半」。
* 忽略 `write` 的返回值，导致几 MB 的大消息在部分写时丢掉尾巴。
* `OP_WRITE` 一直开着，CPU 空转；读到 `readyOps` 的旧值。
* 暂停读之后没人唤醒，通道永久卡住。变异检查时去掉 `poll()` 里的 `wakeup`，自旋 `poll()` 的测试会 20 秒超时失败，信息是「stalled after 3 messages」。
* 容量小于 `maxFrame + 4` 导致死锁；非法长度要等 `len` 字节凑齐才报错；帧头是 `0x7FFFFFFF` 时触发巨大的内存分配。
* 把 EOF 一律当成正常结束，吞掉半条消息；`close` 时接收缓冲区里还有数据，会发出 RST。
* `offer` 满了抛异常而不是返回 false；或者反过来，通道已关闭时也只返回 false。
* 测试里用 `sleep` 来判断「消息应该已经到了」。
* 重连：断线期间 `offer` 直接失败；pending 不设上限；`close` 之后还在重连；连接还没稳定就重置了退避；上限设为 `Long.MAX_VALUE` 时乘法溢出。
* 压力测试中 `offer` 返回 false 可能只是 I/O 线程还没来得及腾出空间，必须等 200 ms 仍然放不下，才算真的堵死。

## 复杂度 + 实测时间

- `ByteRing` 读写的代价与拷贝的字节数成正比；`FrameDecoder.next` 是 O(1) 加一次拷贝。
- `offer` / `poll` 持锁期间只做内存拷贝；每条消息经历两次拷贝（进环、出环）和一次中转缓冲。
- 内存：出站环 + 入站环 + 2 × 16 KB 中转缓冲，不随消息数量增长。

实测：全套 49 个测试约 4–5.6 s；在 12 个进程占满 CPU 的情况下也全部通过。

`ChannelBench`（本机回环，负载 32 字节，各跑 3 次）：

| 项目 | 结果 |
|---|---|
| 吞吐（200 万条，每次取中位数） | 86–114 ms，即 17.5–23.3 M 条/s（约 630–840 MB/s） |
| 往返延迟，本通道 | p50 36 µs，p99 46 µs，p99.9 52–53 µs，max 147–165 µs |
| 往返延迟，裸阻塞 `SocketChannel` 乒乓 | p50 12.4 µs，p99 18 µs，p99.9 23 µs，max 59–121 µs |
| 背压，两端环都是 4 KB | 发送端堵住前接受约 16,500 条（约 593 KB），接收端事后收到同样条数 |
| 背压，两端环都是 64 KB | 约 18,200 条（约 656 KB），接收端事后收到同样条数 |

怎么读这些数字：

- 本通道比裸 socket 多出的约 24 µs，来自应用线程和 I/O 线程之间的两次交接。这正是热路径要在一个线程里一口气处理完（run-to-completion）的原因。
- 请求 `SO_*BUF = 4096`，在这台 macOS 上读回来的实际值是发送 65,328 B、接收约 0.5 MB，所以真正的缓冲主要在内核里。
- 把出站环加大 60 KB，多接受了约 1,700 条（约 60 KB），和预期一致。
- 把接收端的入站环加大，却没有多接受消息：读回的内核接收缓冲区同时缩小了约 57 KB（约 465 KB 对约 523 KB）。原因没有查清。
- 以上往返和背压数字只在 macOS 回环上测过，没有在 Linux 上验证。

## 测试清单（脚本数）

共 49 个，0 失败：part1 21、part2 13、part3 5、part4 10；edge 29、perf 2、conc 4、io 23。

- **FramingTest**（part1，21 个）：
  - 字节环：基本读写、回绕、部分写、部分读、`writeAll` 的原子性、`peekInt` 的大端与符号位、出错时不改状态、和 `ArrayDeque` 随机对照。
  - `FrameCodec`：帧头字节、空负载、放不下时不留半个帧头、超过 `maxFrame`。
  - `FrameDecoder`：整帧、在每个可能的位置切开、逐字节输入、恰好 `maxFrame`、有界 `feed` 和恢复、非法帧头及其粘性失败、`hasFrame` 和截断的尾巴、随机切块。
  - 100 万条消息走一遍字节环 + 解码器的 perf 测试。
- **TcpMessageChannelTest**（part2 13 个 + part3 5 个）：
  - 功能：请求应答；空消息、最大消息、几 MB 的消息；1 万条按序到达；双向同时各发 5000 条；用裸 socket 逐字节发送、一次发「两条半」；非法帧头；帧中间 EOF；`finishSending` 半关闭直到双方都关闭；突然 `close`；`close` 能唤醒阻塞中的 `poll`；20 万条回环 perf。
  - 背压：对端不读时 `offer` 最终返回 false，且事后不丢消息；阻塞 `offer` 能等到空间；最小缓冲区下传 2 万条；自旋的非阻塞 `poll` 能恢复被暂停的读；慢读者。
- **ReconnectTest**（part4，10 个）：
  - `Backoff` 5 个：退避序列、`reset`、上限为 `Long.MAX_VALUE` 时不溢出、全抖动的取值范围、非法参数。
  - `ReconnectingClient` 5 个：服务端踢掉连接后重连并继续收发；服务端整个下线、再在同一端口重新上线后，消息全部按序到达；pending 有上限；`close` 之后不再重连；连接成功后退避被重置。

变异检查（每次只改 reference 的一处）：

| 变异 | 结果 |
|---|---|
| 删掉 `poll()` 里的唤醒 | 自旋 `poll` 的测试 20 秒超时失败 |
| 删掉 `poll(timeout)` 里的唤醒 | 多个测试失败 |
| 删掉 `offer` 在环从空变非空时的唤醒 | 5 个测试失败 |
| 非法帧头只校验 `len < 0` | 2 个测试失败 |
| 环回绕段的起点算错 | 12 个测试失败 |
| `Backoff` 的乘法不防溢出 | 1 个测试失败 |
| `selectedKeys().remove(key)` 改成 `clear()` | 测试仍全部通过——这是等价变异，不是漏测 |

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J10 虚拟线程 | `ReconnectingClient` 的管理线程：`Thread.ofVirtual().name(…).start(…)`，里面是「连接 → 等待 → 退避」的直线式阻塞代码 | 不用写回调链，阻塞时也不占平台线程。热路径上的 I/O 线程仍然用平台线程 |
| J16 `ReentrantLock` / `Condition` | 通道和客户端的全部共享状态 | 支持多个条件、可以带超时等待（`awaitNanos`）；在虚拟线程里不会钉住载体线程（`synchronized` 会） |
| J01 record | `ChannelConfig` 的紧凑构造器做校验（容量 ≥ `maxFrame + 4`） | 非法配置根本造不出来 |
| `RandomGenerator`（Java 17） | `Backoff.next(rng)` 里的 `rng.nextLong(cap + 1)` | 统一的随机数接口，有 `long` 范围的方法；测试里传一个带种子的 `Random`，结果就是确定的 |
| try-with-resources / `AutoCloseable` | 测试和 bench 里的通道、服务器 | 按相反顺序关闭；`close` 可重复调用 |
| J08 var | 测试里的 `var p = pair(CFG)` | 右边已经写明类型时不用再写一遍 |
| `Objects.checkFromIndexSize` | `ByteRing.writeAll` | 抛标准的 IOOBE，而且 `off + len` 不会溢出 |

## 面试官可能的追问

1. **为什么只用一个 `Selector` 线程？** 连接数多的时候，每个连接一个线程撑不住（栈内存、调度开销）。这道题只有一条连接，但同一个 `Selector` 可以注册很多通道。另一种做法是虚拟线程 + 阻塞 I/O，代码大约少三分之二，但延迟抖动更大。
2. **能做成无锁吗？** 出站环和入站环都是单生产者单消费者（SPSC），可以换成 ld01 里用 `setRelease` / `getAcquire` 实现的环，等待改成忙等或 `park`。但值不值得要看测量：现在持锁期间只拷贝几十个字节，瓶颈在 `wakeup` 和线程交接，不在锁。
3. **对端掉电，既没有 FIN 也没有 RST，怎么发现？** TCP 本身区分不了「暂时没消息」和「对方已经没了」，要靠应用层心跳。`SO_KEEPALIVE` 默认空闲两小时才开始探测，太粗了。
4. **重连后能保证不丢吗？** 本实现是 at-most-once 的尽力而为，丢掉的字节记在 `abandonedBytes` 里。要做到不丢，需要应用层的序号 + 确认 + 重传（at-least-once），再加上去重。FIX 的会话层就是这样做的。
5. **Nagle 算法和 `TCP_NODELAY`？** 必须打开 `TCP_NODELAY`。我们已经在应用层批量发送了（出站环 + 一次 `write` 发多条），不需要 Nagle；开着 Nagle 再碰上延迟确认，会出现约 40 ms 的停顿。
6. **应用一直不 `poll` 会怎样？** 入站环满 → 停止读 → 对端被拖慢，这正是设计意图。但如果同一个线程既在等 `offer` 的空间、又不去 `poll`，而对端也是这样，就会死锁。所以接口约定是：收和发放在不同线程，或者使用非阻塞的 `offer`。
7. **行情和订单的背压策略一样吗？** 不一样。订单不能丢：满了就停止接收并报警（fail closed）。行情可以合并（conflation），只保留最新值。通道只负责报告「满了」，丢什么由业务决定。
8. **为什么容量必须不小于 `maxFrame + 4`？** 否则入站环里可能是半条最大消息、而且已经满了：读不进新字节，这条消息也永远凑不齐，就死锁了。出站方向则是最大的消息永远 `offer` 不进去。
9. **epoll 的水平触发和边缘触发？** NIO 在 Linux 上表现为水平触发，所以一次只读一部分也不会丢事件。
10. **TLS 怎么接进来？** 把 `SSLEngine` 的 `wrap` / `unwrap` 放在字节流和 `FrameDecoder` 之间。难点在于处理 `BUFFER_UNDERFLOW`，以及握手阶段的 `NEED_WRAP` / `NEED_UNWRAP`。现在的结构（环 + 中转缓冲 + I/O 线程）正好留出了放它的位置。
