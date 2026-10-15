# ld03 · 异步 TCP 消息通道：成帧、部分 I/O、背压、半关闭、重连 —— 讲义

> 题面：`loop/rounds/03_lld/ld03_async_tcp_channel/problem.md` · 代码：同目录 `reference/`（`ByteRing` `FrameCodec` `FrameDecoder` `TcpMessageChannel` `MessageServer` `Backoff` `ReconnectingClient`）· 测试：`test/`（49 个）
> 实验代码：`study/30-articles/examples/ld03/ChannelBench.java`（吞吐、往返延迟、背压）。本文的"实测"来自它和测试套件在本机（Apple M 系列，12 核，macOS，JDK 21.0.12）的运行。**全部在回环接口（127.0.0.1）上，测的是软件和内核开销，不是网线。**
> 写法说明见 `study/TEXTBOOK.md`。读者设定：只会基本 Java，没学过网络编程、NIO、背压。前置基础课：`study/00-foundations/networking_basics.md`（TCP / Nagle / `Selector` / 虚拟线程），本篇不重复它的内容，只在需要处链接。
> **题面是 (reconstructed)**：证据只有 FastPrep 的一句话摘要「bounded message API over one TCP session, with local circular buffers, partial-I/O framing…」。

---

## 1. 这道题在问什么

### 1.1 用大白话

两个程序隔着网络通信：一个（比如行情网关）不停地发**消息**，另一个（比如策略）接收。它们之间只有一条 TCP 连接。你要写一个小库，让两端的程序员只用两个方法：

```java
boolean offer(byte[] message)   // 发一条消息；"满了"就返回 false
byte[]  poll()                  // 收一条消息；没有就返回 null
```

听起来简单，难点全在"TCP 不是消息，是水管里的字节"：

* 你发两条消息，对方可能收到"一条半"然后"半条"——**消息边界不存在**；
* 你要发的数据多、网络慢，操作系统只肯接收你的一部分——**部分写**；
* 对方读得慢，水管会满，满了以后你的 `write` 就写不进去——要把这个"满"一路传回给调用 `offer` 的人，而不是在内存里无限堆积——**背压**；
* 连接会断。

题目的关键词逐个翻译：**one TCP session**（一条连接）、**bounded**（每一层都有上限）、**local circular buffers**（本地环形缓冲区：一个放待发送的字节，一个放收到但还没凑成消息的字节）、**partial-I/O framing**（部分读写时的成帧）。

### 1.2 手算：字节流上的两条消息

约定：每条消息前加 **4 字节的长度**（大端），后面是内容。发两条消息 `"AB"`（2 字节）和 `"CDE"`（3 字节），线上的字节是：

```text
消息1           消息2
00 00 00 02 41 42 | 00 00 00 03 43 44 45          共 13 字节（41 = 'A'，42 = 'B'，43 = 'C' …）
```

接收方的 `read` 把这 13 字节切成了任意几块（TCP 不保证怎么切）。假设切成 `5 + 6 + 2`：

```text
第 1 次 read 收到: 00 00 00 02 41                      缓冲区: [00 00 00 02 41]
   解码器: 看头 → 长度 = 2；需要 4+2 = 6 字节，现有 5 → 不够，返回 null（什么都不交付）
第 2 次 read 收到: 42 00 00 00 03 43                   缓冲区: [00 00 00 02 41 42 00 00 00 03 43]
   解码器: 长度 2，现有 11 ≥ 6 → 交付 "AB"，消费 6 字节 → 缓冲区 [00 00 00 03 43]
   再看头 → 长度 = 3，需要 7，现有 5 → null
第 3 次 read 收到: 44 45                               缓冲区: [00 00 00 03 43 44 45]
   解码器: 长度 3，现有 7 ≥ 7 → 交付 "CDE"
```

### 1.3 手算：背压

假设出站环 64 字节，每条消息帧 36 字节（4 + 32）。对方一直不读：

```text
offer #1 → 环 36/64   true
offer #2 → 环 72 > 64 放不下 → false    ← 调用方知道"满了"，由它决定等 / 丢 / 降级
（I/O 线程把环里的字节写进内核发送缓冲区；对方不读，内核缓冲区也满了，write 返回 0；环不再被腾空）
```

对方开始读 → 内核缓冲区腾出空间 → 我们的 `write` 又能写 → 出站环腾出空间 → `offer` 又返回 `true`。**"满"这一信息，从对方的应用，穿过两端的内核，一路传回我们的调用者。**

### 1.4 四个 Part

1. `ByteRing` + `FrameCodec` + `FrameDecoder`：纯内存，没有网络。环形缓冲区；4 字节长度前缀；增量解码器。
2. `TcpMessageChannel` / `MessageServer`：一个 `Selector` I/O 线程，部分读写，EOF，半关闭。
3. 背压与有界性：入站环满了停止读；最小缓冲区的压力测试。
4. `Backoff` + `ReconnectingClient`：指数退避，断线重连，断线期间的有界 pending。

---

## 2. 前置知识

### 2.1 TCP 是字节流，不是消息流

**是什么**：TCP 给两端提供一对**可靠、有序的字节管道**。可靠 = 不丢不重；有序 = 先写的先到。它**不保留**你每次 `write` 的边界。

**为什么需要知道**：没有它，你会写出"一次 `read` = 一条消息"的代码，开发机上（数据量小、延迟低）都能跑，一上线就偶发错乱。

**怎么工作**：

```text
发送方的 write 调用:   [AAAA]   [BBBBBB]   [CC]
TCP 在线上的分段:      [AAAABB]  [BBBB]  [CC]        ← 由 MSS、拥塞窗口、Nagle 等决定，不是你决定
接收方的 read 调用:    [AAAABBBBBBCC] 一次读完    或   [AAAAB] [BBBBB] [BCC]    ← 同样不是你决定
```

**Java 里怎么写**：见 §5。基础讲解见 `networking_basics.md` §2、§8.4（"TCP 是字节流：必须自己做帧"）。

### 2.2 成帧（framing）：自己给消息加边界

**是什么**：在字节流之上约定"怎么知道一条消息从哪到哪"的规则。

**三种常见办法**：

| 办法 | 做法 | 优点 | 缺点 |
|---|---|---|---|
| 定长 | 每条消息固定 N 字节 | 最简单 | 浪费空间；变长消息不行 |
| 分隔符 | 以 `\n` 结尾（HTTP/1 头、Redis 旧协议） | 人可读 | 内容里不能出现分隔符，要转义；找分隔符要逐字节扫描 |
| **长度前缀** | `[长度][内容]` | 二进制安全；解码只看头；可以一次分配 | 必须保护长度字段（下面） |

本题用**长度前缀**，4 字节**大端**（高位字节先发，网络字节序，Java 的 `ByteBuffer` 默认也是大端）。

**必须防御长度字段**：对端发来 `0x7FFFFFFF`（21 亿）。如果你"先看到长度，就去分配那么多字节再等"，就被一个恶意的（或出 bug 的）4 字节搞挂了内存——这是真实世界里常见的拒绝服务攻击。所以：①约定 `maxFrame`；②**只看到 4 字节头就检查**，超过立刻报错；③长度为负（高位为 1 的 int）同样报错。报错后流已经失去同步（不知道下一条从哪开始），只能断开重连，所以解码器"粘性失败"。

### 2.3 阻塞 vs 非阻塞 I/O、`Selector`

（完整讲解在 `networking_basics.md` §8；这里只列本题用到的规则。）

* **非阻塞**：`read` 没数据时立刻返回 0（不睡眠）；`write` 发送缓冲区满时返回 0 或只写一部分。
* **`Selector`**：一个线程"同时盯着"很多套接字，问内核"哪些就绪了"。`select()` 睡眠直到有套接字就绪、或别的线程调用了 `selector.wakeup()`。
* **兴趣集（interest ops）**：你告诉 selector 你关心哪些事件：`OP_READ`（有数据可读）、`OP_WRITE`（发送缓冲区有空位）。
* **规则 1：就绪 ≠ 完成**。`OP_READ` 只表示"现在读不会阻塞"，不表示"一条完整消息到了"。
* **规则 2：`OP_WRITE` 不要常开**。只要发送缓冲区有空位它就一直就绪，`select()` 立刻返回，你的循环就变成 100% CPU 的忙等。**只在"还有数据要写"时才打开**，写完就关。
* **规则 3：谁改兴趣集**。本实现只有 I/O 线程改；别的线程要改变 I/O 线程的行为时，设置状态 + `selector.wakeup()`，由 I/O 线程在循环顶部**重新计算**兴趣集。`wakeup()` 是"粘性"的：如果当时没有 `select` 在进行，下一次 `select` 立刻返回——所以不会丢唤醒。
* **规则 4：`selectedKeys` 和 `readyOps`**。`select()` 返回后，只有被选中的 key 的 `readyOps` 是新鲜的；如果一次 `select` 是被 `wakeup` 叫醒的，没有 key 被选中，`key.readyOps()` 里可能还是**上一轮的旧值**。所以代码写 `if (selector.selectedKeys().remove(key)) { 看 readyOps }`——只有"这一轮真的被选中"才信它。

### 2.4 `ByteBuffer` 的三个游标

`position`（下一个要读/写的位置）、`limit`（可操作区域末端）、`capacity`。写完之后要 `flip()` 才能读；读完要 `clear()` 或 `compact()` 才能再写。详见 `networking_basics.md` §8.3。本题的 `ByteRing.write(ByteBuffer src)` 从 `src.position` 开始读 `n` 个字节并前进 `position`；`read(ByteBuffer dst)` 反过来。

`allocateDirect`：直接缓冲区在 JVM 堆外，`SocketChannel` 读写时可以少一次拷贝；本实现的两个 16 KB 中转缓冲区（`rbuf`、`wbuf`）用它。

### 2.5 环形缓冲区（字节版）

（完整讲解在 `study/30-articles/ld01_spsc_channel.md` §2.3。）本题的 `ByteRing` 是单线程字节环，容量任意正整数（所以用 `%` 而不是 `& mask`）。两个变量：`head`（下一个要读的位置）和 `size`（当前字节数）；写入位置 = `(head + size) % capacity`。回绕时一次拷贝拆成两段。

```text
容量 8，head=6，size=4（占用下标 6,7,0,1）：  [ 2 3 . . . . 0 1 ]    写入位置 (6+4)%8 = 2
读 4 字节：先读下标 6,7（尾部这一段），再读 0,1（开头这一段）
```

### 2.6 背压（backpressure）

**是什么**：下游处理不过来时，让上游**慢下来**（或停下来），而不是上游一直发、中间堆积。

**为什么需要**：没有背压的系统，快的生产者 + 慢的消费者 = 中间队列无限增长 = 内存耗尽或延迟爆炸。**每一层的缓冲区都必须有上限，满了要向上游表达"满了"。**

**怎么工作：本题里的四层**

```text
 应用线程 ──offer──▶ [出站环 outCapacity] ──I/O线程 write──▶ [内核发送缓冲区] ══网络══▶ [内核接收缓冲区] ──I/O线程 read──▶ [入站环 inCapacity] ──poll──▶ 应用线程
      ▲ false 表示满了                          ▲ write 返回 0                         TCP 窗口缩小到 0               ▲ 满了就不再监听 OP_READ
```

* 入站环满 → I/O 线程不再读 → 内核接收缓冲区满 → TCP 向对端通告窗口 = 0 → 对端内核发送缓冲区满 → 对端 `write` 返回 0 → 对端出站环满 → 对端 `offer` 返回 `false`。**一个应用的"没空读"，穿过六层，变成另一个应用的"满了"。**
* Little 定律（L = λ·W）：缓冲区里的消息数 = 到达速率 × 停留时间。停留时间无上限则 L 无上限。

### 2.7 EOF、半关闭与 RST

* 对端调用 `close()`（或 `shutdownOutput()`）→ 发送 **FIN**；本端 `read` 返回 **-1**（EOF）。EOF 的意思是"对端不会再发数据了"，**不等于"我也该关了"**：TCP 是全双工，可以只关一个方向（**半关闭**）。
* `socketChannel.shutdownOutput()`：本端不再发送（发 FIN），但仍可接收。本题的 `finishSending()` 就是它（先把已接受的消息刷完）。
* **RST**：连接被粗暴重置。常见来源：①对端进程崩溃/被 kill；②向已关闭的端口发数据；③**`close()` 时接收缓冲区里还有没读的数据**——内核会发 RST 而不是 FIN，对端未读完的、已发出的数据可能被丢弃。所以"优雅关闭"要**先 `shutdownOutput`，等对端的 EOF，再 `close`**。
* EOF 恰好发生在**一帧中间**（读到了头和半个内容）= 流被截断，这是错误（`EOFException`），不是正常结束。

### 2.8 锁与条件变量（一段话版）

多个线程共享缓冲区，用一把 `ReentrantLock` 保护；"等一个条件成立"用 `Condition`：`while (!条件) cond.await(); ` ——必须是 `while` 不是 `if`（可能被虚假唤醒或条件又被别人改了）；改变条件的线程 `signalAll()`。**临界区里只做内存拷贝，不做系统调用**（系统调用可能睡很久，持锁睡会让所有人等）。详见 `study/10-java21/J16_concurrency_primitives.md`。为什么用 `ReentrantLock` 而不是 `synchronized`：在 JDK 21 的虚拟线程上，`synchronized` 里阻塞会**钉住**（pin）载体线程；`ReentrantLock` 不会（J10）。本实现的 I/O 线程是平台线程，但 `ReconnectingClient` 的管理线程是虚拟线程，所以统一用 `ReentrantLock`。

### 2.9 重连与指数退避

**为什么要退避**：对端宕机时，如果每 1 毫秒重试一次，既浪费 CPU，又在对端恢复的瞬间造成"惊群"——成千上万个客户端同时重连，把刚恢复的服务打死。**指数退避**：第 1 次等 `initial`，之后每次翻倍（封顶 `max`）；**抖动（jitter）**：在 `[0, 当前延迟]` 里随机取一个值（"全抖动"），让不同客户端的重试时刻分散开（AWS 架构博客「Exponential Backoff and Jitter」对几种抖动做过模拟比较）。成功连接后**重置**退避。

**重连后的语义（务必讲清楚）**：TCP 只保证**一条连接存续期间**的有序不丢。连接断了，已经进了旧连接的内核缓冲区、但对端还没读走的字节**可能丢**；你无法知道对端处理到哪里了。要不丢，需要**应用层的序号 + 确认 + 重传**（at-least-once），再加对端去重（effectively-once）。没有它，重连客户端只是 **at-most-once 的尽力而为**。

---

## 3. 从最笨的解法开始

```java
// 服务端：每个连接一个线程；把一次 read 当成一条消息
Socket s = server.accept();
new Thread(() -> {
    byte[] buf = new byte[1024];
    InputStream in = s.getInputStream();
    int n;
    while ((n = in.read(buf)) > 0) {
        queue.add(Arrays.copyOf(buf, n));          // queue 是 LinkedBlockingQueue：无界
    }
}).start();

// 客户端：
out.write(message);                                 // 假设"写出去了"
```

**它在哪些输入上错 / 慢**：

| 输入 | 暴露的问题 |
|---|---|
| 发 2 条消息，对方一次 `read` 收到 2 条粘在一起 | 被当成 1 条（粘包） |
| 一条 2,000 字节的消息，`buf` 只有 1,024 | 被切成两条（拆包） |
| 对方慢，我方一直发 | `LinkedBlockingQueue` 无界，内存无限涨；`OutputStream.write` 在内核缓冲区满时**阻塞**调用线程，没有"满了"的概念 |
| 1 万个连接 | 1 万个线程，每个栈 1 MB，上下文切换；`networking_basics.md` §8.1 的 C10K 问题 |
| 连接断开 | 线程默默退出，上层不知道；没有重连 |
| 对端关闭一半 | `read` 返回 -1 就退出，不区分"正常结束"和"消息中间被截断" |
| 恶意长度 | 如果你用 `readInt()` 后 `new byte[len]`，一个 4 字节包就能让你 OOM |

---

## 4. 一步一步改进

### 步骤 1：长度前缀成帧

**问题**：粘包 / 拆包。**想法**：`[len:4][payload]`。**为什么有效**：接收方读 4 字节知道要读多少，之后的字节一定属于这条消息。**新问题**：一次 `read` 可能只有半个头；要把"读到一半"的状态存起来 → 步骤 2。

### 步骤 2：增量解码器

**想法**：解码器是一个有状态的对象，`feed(bytes)` 喂任意长度的字节，`next()` 吐出完整的消息，不够就返回 `null`。状态 = 已收到但没凑成消息的字节，放在一个缓冲区里。测试：把一个流在**每一个**可能的切分点切开，结果必须相同（`decoderHandlesEverySplitPointOfAStream`）；逐字节喂（`decoderByteAtATime`）；随机切块（`decoderRandomChunkingRoundTrip`）。

### 步骤 3：缓冲区有界 → 环形缓冲区

**问题**：解码器的缓冲区如果可增长，对端发来一堆没凑成消息的字节，内存就无限涨。**想法**：用固定容量的 `ByteRing`；容量 ≥ `maxFrame + 4`（保证一条最大的消息总能放下，否则永远凑不齐——死锁）。`feed` 放不下的部分**不消费**，返回实际消费数——调用方必须先 `next()` 腾空间。**为什么环而不是 `byte[]` + `System.arraycopy` 前移**：前移每次 O(n)；环形只改 `head`，O(1)。

### 步骤 4：非阻塞 I/O + 一个 `Selector` 线程

**问题**：线程每连接一个，且 `write` 会阻塞调用线程。**想法**：应用线程只和两个内存缓冲区打交道（`offer` 写出站环、`poll` 读入站环），所有网络 I/O 在一个 I/O 线程里用 `Selector` 做。**为什么有效**：`offer`/`poll` 不会因为网络慢而阻塞；一个线程服务一条连接（本题只要求一条）也容易扩展到多条（同一个 `Selector` 注册多个通道）。

### 步骤 5：处理部分写

**问题**：`ch.write(buf)` 可能只写出一部分。**想法**：出站环里的字节先拷贝到一个中转缓冲区 `wbuf`；写出去多少就前进多少 `position`；剩下的留在 `wbuf` 里，下次 `OP_WRITE` 就绪时**继续写 `wbuf`**，写空了才从出站环再取。**这是新手最常漏掉的**：把 `write` 的返回值扔掉，或者写了一部分就丢弃剩余。

### 步骤 6：每轮循环重新计算兴趣集

**问题**：谁来打开 / 关闭 `OP_WRITE` / `OP_READ`？应用线程不能直接改（`SelectionKey.interestOps` 在别的线程上调用，行为取决于实现，且容易竞态）。**想法**：I/O 线程每轮循环顶部，**在锁内**看当前状态算出兴趣集：

```text
OP_READ  ⇐ 对端没关闭 且 入站环还有空位
OP_WRITE ⇐ 还没发 FIN 且 (wbuf 里还有数据 或 出站环非空)
```

应用线程改变了状态（`offer` 放进了数据、`poll` 腾出了空间、`close`）就调 `selector.wakeup()` 叫醒 I/O 线程，让它重算。**为什么有效**：所有"该关注什么"的决定都在一个地方、一个线程，没有竞态。

### 步骤 7：入站背压——满了就不读，`poll` 负责叫醒

**问题**：入站环满了还读，读出来的字节没地方放。**想法**：入站环满 ⟹ 兴趣集里去掉 `OP_READ`（内核缓冲区会填满，TCP 窗口缩到 0，对端被拖慢）；`poll` 取走一条后（腾出了空间）**必须 `wakeup()`**，I/O 线程才会重算兴趣集，重新打开 `OP_READ`。**这是个很容易漏的 bug**：漏了唤醒，I/O 线程睡在 `select()` 上、兴趣集是 0，不会醒，通道从此"卡住"（本 kit 的变异检查：删掉 `poll()` 里的 `wakeup`，测试 `spinningNonBlockingPollResumesAPausedReader` 在 20 秒后以「stalled after 3 messages」失败）。优化：用一个 `readPaused` 标志，只有"确实暂停了读"时才唤醒，省掉每次 `poll` 的 `wakeup` 系统调用。

### 步骤 8：EOF、截断与半关闭

* `read` 返回 -1：设 `peerClosed = true`（不再监听读）。此时如果缓冲区里有一截**不完整的帧**（`hasTruncatedTail()`）⟹ 错误（`EOFException`），通道关闭，但之前收齐的完整消息仍可 `poll`。
* `finishSending()`：状态变 `FINISHING`（之后 `offer` 抛异常）；I/O 线程等出站环和 `wbuf` 都空了，再 `shutdownOutput()` 发 FIN。本端已发 FIN 且对端也已 EOF ⟹ 通道自动关闭。
* 为什么不在 EOF 时立刻 `close`：对端可能只是 `finishSending`（半关闭），我们这边还有话要说（测试 `finishSendingFlushesThenPeerSeesDrained` 里服务端收完以后还回了 "bye"）。

### 步骤 9：并发设计——一把锁，系统调用在锁外

**问题**：应用线程（`offer`/`poll`）和 I/O 线程共享两个环和一堆标志。**想法**：一把 `ReentrantLock` 保护所有共享状态；`Condition changed` 用于 `poll(timeout)`、`offer(msg, timeout)`、`awaitClosed`——I/O 线程在"收到了数据"/"腾出了出站空间"/"状态变了"时 `signalAll()`。**临界区内只有内存拷贝**，`read`/`write`/`select` 全在锁外。**为什么不无锁**：这里的瓶颈是系统调用，不是锁；锁内工作是几十字节的拷贝。要做无锁 SPSC 环，见 ld01（那里是跨进程共享内存，没有系统调用）。

### 步骤 10：重连——pending 队列 + 退避 + 诚实的语义

`ReconnectingClient`：`offer` 总是先进有界的 `pending`（按"已编码字节"计，上限 = `cfg.outCapacity()`，和出站环同一口径）；管理线程连接成功后把 `pending` 按序搬进通道；通道断了 ⟹ 记下 `unsentBytes` 到 `abandonedBytes`（诚实：这些字节丢了）、丢弃旧通道、退避、重连。

---

## 5. 逐段讲参考解

### 5.1 `ByteRing`：回绕时拆成两段

```java
    public int write(ByteBuffer src) {
        int n = Math.min(src.remaining(), free());
        int tail = (head + size) % buf.length;
        int first = Math.min(n, buf.length - tail);
        src.get(buf, tail, first);
        src.get(buf, 0, n - first);
        size += n;
        return n;
    }
```

```java
    public int read(ByteBuffer dst) {
        int n = Math.min(dst.remaining(), size);
        int first = Math.min(n, buf.length - head);
        dst.put(buf, head, first);
        dst.put(buf, 0, n - first);
        head = (head + n) % buf.length;
        size -= n;
        return n;
    }
```

* `tail = (head + size) % buf.length` 是写入起点；`first = min(n, buf.length - tail)` 是从起点到数组末尾能放多少；剩下 `n - first` 从下标 0 开始。读同理。**两次 `src.get(...)` 之间 `src.position` 自动前进**。
* 满时 `n = 0`，`first = 0`，两次拷贝都是空操作；不需要特判。

### 5.2 `FrameDecoder.next`：只看头就拒绝

```java
    public byte[] next() {
        if (failed != null) throw failed;
        if (ring.size() < FrameCodec.HEADER) return null;
        int len = ring.peekInt();
        if (len < 0 || len > maxFrame) {
            failed = new FrameException("bad frame length " + len + " (maxFrame " + maxFrame + ")");
            throw failed;
        }
        if (ring.size() < FrameCodec.HEADER + len) return null;
        ring.skip(FrameCodec.HEADER);
        return ring.take(len);
    }
```

* `ring.size() < HEADER` ⟹ `null`（连头都没凑齐）。
* `peekInt()` 不消费，所以"头到了但负载没到"时什么都不改变，下次 `feed` 之后再看一遍。
* 非法长度立刻抛，且把异常存进 `failed`：之后每次调用都抛同一个异常（**粘性**）。
* 凑齐了才 `skip(HEADER)` + `take(len)`。

### 5.3 `TcpMessageChannel.offer` 与 `poll`

```java
    public boolean offer(byte[] msg) {
        lock.lock();
        boolean wasEmpty;
        try {
            requireSendable();
            wasEmpty = out.isEmpty();
            if (!FrameCodec.encode(out, msg, cfg.maxFrame())) return false;
        } finally {
            lock.unlock();
        }
        if (wasEmpty) selector.wakeup();     // out 非空时 I/O 线程已经在等 OP_WRITE，不必再唤醒
        return true;
    }
```

* `wasEmpty`：出站环**从空变非空**才需要唤醒 I/O 线程（环非空时 I/O 线程已经在等 `OP_WRITE` 了）。论证：设置兴趣集和这里读 `out.isEmpty()` 都在同一把锁里，所以不存在"I/O 线程刚算出兴趣集 = 无写、我们看到环非空因此没唤醒"的间隙。
* `IllegalStateException` 与 `false` 区分：`false` 是"暂时满了，稍后再来"，异常是"通道已经不能发了"。

```java
    public byte[] poll() {
        boolean wake;
        byte[] m;
        lock.lock();
        try {
            m = nextLocked();
            wake = m != null && readPaused;
            if (wake) readPaused = false;
        } finally {
            lock.unlock();
        }
        if (wake) selector.wakeup();
        return m;
    }
```

* `readPaused`：I/O 线程因入站环满而暂停读时置位；这里取出一条消息（腾出空间）后，清除它并在**锁外**调用 `wakeup()`。

```java
    public byte[] poll(long timeoutMs) throws InterruptedException {
        long nanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs);
        boolean wake = false;
        byte[] m;
        lock.lock();
        try {
            for (;;) {
                m = nextLocked();
                if (m != null || inboundFinishedLocked() || nanos <= 0) break;
                nanos = changed.awaitNanos(nanos);
            }
            if (m != null && readPaused) { readPaused = false; wake = true; }
        } finally {
            lock.unlock();
        }
        if (wake) selector.wakeup();
        return m;
    }
```

* `awaitNanos` 返回剩余时间；循环里每次先尝试取，再判断"不会再有消息"（`inboundFinishedLocked`），再判断超时。
* 条件变量的使用范式：`for(;;) { 先检查条件; 不满足就 await }`。

### 5.4 I/O 线程主循环

```java
    private void ioLoop() {
        try {
            for (;;) {
                int ops = 0;
                lock.lock();
                try {
                    if (state == State.CLOSED) break;
                    if (state == State.FINISHING && !finSent && out.isEmpty() && !wbuf.hasRemaining()) {
                        ch.shutdownOutput();                         // 发 FIN：对端 read 返回 -1
                        finSent = true;
                    }
                    if (finSent && peerClosed) { state = State.CLOSED; changed.signalAll(); break; }
                    readPaused = !peerClosed && in.free() == 0;
                    if (!peerClosed && in.free() > 0) ops |= SelectionKey.OP_READ;
                    if (!finSent && (wbuf.hasRemaining() || !out.isEmpty())) ops |= SelectionKey.OP_WRITE;
                } finally {
                    lock.unlock();
                }
                key.interestOps(ops);
                selector.select();                                   // 睡到：socket 就绪 或 selector.wakeup()
                if (selector.selectedKeys().remove(key)) {           // 只在本轮真的被选中时才看 readyOps（否则是上一轮的旧值）
                    if (key.isReadable()) doRead();
                    if (key.isWritable()) doWrite();
                }
            }
        } catch (Throwable t) {
            lock.lock();
            try { failLocked(t); } finally { lock.unlock(); }
        } finally {
            try { ch.close(); } catch (IOException ignored) { }
            try { selector.close(); } catch (IOException ignored) { }
            lock.lock();
            try { state = State.CLOSED; changed.signalAll(); } finally { lock.unlock(); }
        }
    }
```

* 循环顶部（锁内）：处理"该发 FIN 了吗"（`FINISHING` 且两个缓冲都空）；"全部结束了吗"（`finSent && peerClosed`）；然后算兴趣集。
* `key.interestOps(ops); selector.select();`：兴趣集为 0 时 `select()` 会一直睡到 `wakeup()`——这是预期的（比如没有数据要写，也不读）。
* `selectedKeys().remove(key)`：§2.3 的规则 4。
* 任何异常 → `failLocked(t)`；`finally` 里关闭 socket 和 selector，状态置 `CLOSED` 并 `signalAll`。

### 5.5 读与写

```java
    private void doRead() throws IOException {
        int room;
        lock.lock();
        try { room = in.free(); } finally { lock.unlock(); }
        if (room == 0) return;
        rbuf.clear();
        rbuf.limit(Math.min(rbuf.capacity(), room));
        int n = ch.read(rbuf);
        if (n < 0) {
            lock.lock();
            try {
                peerClosed = true;
                if (in.hasTruncatedTail()) failLocked(new EOFException("peer closed in the middle of a frame (" + in.buffered() + " bytes buffered)"));
                changed.signalAll();
            } finally {
                lock.unlock();
            }
        } else if (n > 0) {
            rbuf.flip();
            lock.lock();
            try {
                in.feed(rbuf);                                       // room >= n：一定吃得下
                changed.signalAll();
            } finally {
                lock.unlock();
            }
        }
    }
```

* `rbuf.limit(min(rbuf.capacity(), room))`：**读的量不超过入站环的空位**，所以 `in.feed(rbuf)` 一定吃得下，不会出现"读出来的字节放不下"。
* `n < 0`：EOF。`hasTruncatedTail()` 为真 ⟹ `failLocked(EOFException)`。

```java
    private void doWrite() throws IOException {
        for (int round = 0; round < 16; round++) {                   // 限制一轮最多写多少，别饿死读
            if (!wbuf.hasRemaining()) {
                lock.lock();
                try {
                    wbuf.clear();
                    out.read(wbuf);
                    wbuf.flip();
                    changed.signalAll();                             // out 腾出了空间：唤醒阻塞在 offer(msg, timeout) 的线程
                } finally {
                    lock.unlock();
                }
                if (!wbuf.hasRemaining()) return;
            }
            int n = ch.write(wbuf);                                  // 可能只写一部分，剩下的留在 wbuf 里，等下一次 OP_WRITE
            if (n == 0) return;
        }
    }
```

* 外层 `for` 限制一次最多 16 轮：避免出站环一直有数据时，写循环饿死读。
* `wbuf` 没写空就保持原样，等下次 `OP_WRITE`。`n == 0` 立刻返回（内核缓冲区满）。
* 每次从环里取走数据后 `changed.signalAll()`：唤醒阻塞在 `offer(msg, timeout)` 里等空间的线程。

### 5.6 重连

```java
    public long next() {
        long d = current;
        current = current > maxMs / multiplier ? maxMs : Math.min(maxMs, current * multiplier);
        return d;
    }
```

* `current > maxMs / multiplier ? maxMs : min(maxMs, current * multiplier)`：先用除法判断乘法会不会超过上限，**避免 `current * multiplier` 溢出**（`maxMs` 可以是 `Long.MAX_VALUE`，测试 `backoffCapsExactlyAndNeverOverflows`）。

```java
    private void run() {
        while (!isClosed()) {
            TcpMessageChannel ch;
            try {
                ch = TcpMessageChannel.connect(addr, cfg, 2_000);
            } catch (IOException e) {
                lock.lock();
                try { failedAttempts++; } finally { lock.unlock(); }
                if (!sleep(backoff.next())) return;
                continue;
            }
            lock.lock();
            try {
                if (closed) { ch.close(); return; }
                current = ch;
                connectCount++;
                backoff.reset();
            } finally {
                lock.unlock();
            }
            pump(ch);
            lock.lock();
            try {
                current = null;
                abandonedBytes += ch.unsentBytes();
            } finally {
                lock.unlock();
            }
            ch.close();
        }
    }
```

```java
    private void pump(TcpMessageChannel ch) {
        lock.lock();
        try {
            while (!closed && ch.isOpen() && !ch.isPeerClosed()) {
                while (!pending.isEmpty()) {
                    byte[] m = pending.peekFirst();
                    boolean accepted;
                    try {
                        accepted = ch.offer(m);
                    } catch (IllegalStateException channelDied) {
                        return;
                    }
                    if (!accepted) break;                // 通道的出站环满了：等一会儿再试
                    pending.pollFirst();
                    pendingBytes -= FrameCodec.HEADER + m.length;
                }
                try {
                    wake.await(10, TimeUnit.MILLISECONDS);   // 周期性醒来检查连接是否还活着 / 出站环是否腾出了空间
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        } finally {
            lock.unlock();
        }
    }
```

* `pump` 持有客户端锁，把 `pending` 队首的消息交给通道：被接受才 `pollFirst`；通道满了就 `break` 然后 `wake.await(10ms)` 周期性醒来再试（也借此检查连接是否还活着）。
* 通道断开的判断：`!ch.isOpen() || ch.isPeerClosed()`——对端 EOF 就当作断线（应用协议里没有半关闭）。
* `abandonedBytes += ch.unsentBytes()`：通道里还没写进 socket 的字节，丢了。

### 5.7 本机实测

`study/30-articles/examples/ld03/ChannelBench.java`（3 次运行）：

```text
throughput: 2,000,000 msgs x 32 B（含 4 B 头）, 中位数 86–114 ms      => 17.5 – 23.3 M msg/s（约 630–840 MB/s）
round-trip our channel  : p50 36.1 us, p99 46.5 us, p99.9 52.6 us, max 147–165 us
round-trip raw blocking : p50 12.4 us, p99 18.1 us, p99.9 23.0 us, max 59–121 us
backpressure: rings 4 KB/4 KB   -> sender accepted ~16,500 msgs (~593 KB) before a 200 ms stall; receiver drained the same count
backpressure: rings 64 KB/64 KB -> sender accepted ~18,200 msgs (~656 KB) before a 200 ms stall; receiver drained the same count
```

怎么读这些数字（诚实版）：

* **吞吐**（回环、32 字节、一个发送线程 + 一个接收线程）：每秒千万级条数，瓶颈是批量系统调用和两个线程的交接，不是协议。真实网络上吞吐受网卡和 RTT 限制。
* **往返延迟：我们的通道 p50 36 µs，裸阻塞 socket 乒乓 p50 12 µs。** 多出来的约 24 µs 就是**线程交接**的代价：一次往返里，应用线程 → I/O 线程（`wakeup` 一次系统调用 + 线程被唤醒）、I/O 线程 → 应用线程（`signalAll` + `unpark`）各发生两次。**这正是 sd03 里"热路径 run-to-completion、不要线程交接"的原因**，也是低延迟系统常常让应用线程自己轮询网卡的原因。这套通道为**吞吐和易用**设计，不是为 µs 级往返。（数字是这台 macOS 笔记本的回环，Linux 服务器上会不同；量级关系未在 Linux 上验证。）
* **背压**：请求 `SO_SNDBUF`/`SO_RCVBUF` = 4096，在这台 macOS 上读回来是发送 65,328 字节、接收约 0.5 MB（内核自行放大），所以**真正的缓冲主要在内核里**：发送端在被堵住之前能灌进 ~590–660 KB。把**出站环**从 4 KB 加到 64 KB，多接受约 1,700 条（≈ 60 KB，和预期一致）；但把**接收端入站环**加大**没有**多接受任何消息——读回的内核接收缓冲区同时变小了约 57 KB（约 465 KB 对约 523 KB）。我没有进一步解释这个现象。**教训：多层缓冲相加，总量由最大的那层（这里是内核）决定；想让背压早点生效，要有意地设小内核缓冲区（在 Linux 上手动设置 `SO_RCVBUF`/`SO_SNDBUF` 会关闭该套接字的自动调优，见 `man 7 tcp`；本机未验证）。**
* **接收方事后收到的条数 = 发送方接受的条数**（"equal: true"）：没丢、没重——这是测试断言的核心。

---

## 6. Java 21 特性小课

| 特性 | 旧写法（Java 8 风格） | 新写法（本题） | 编译器 / 运行时多做了什么；什么时候别用 |
|---|---|---|---|
| **虚拟线程**（[J10](../10-java21/J10_virtual_threads.md)） | `new Thread(this::run)` + 线程池管理；或回调式的 `CompletableFuture` 链来写"连接-等待-重试" | `Thread.ofVirtual().name("reconnecting-client-" + addr).start(this::run)`，里面写直线的阻塞代码 | 虚拟线程在阻塞 I/O / `Condition.await` 时卸载，不占平台线程。适合"很多个大部分时间在等"的任务（重连管理）。**不适合**热路径（调度开销和不确定性）；`synchronized` 里阻塞会钉住载体线程，所以用 `ReentrantLock` |
| **`ReentrantLock` + `Condition`**（[J16](../10-java21/J16_concurrency_primitives.md)） | `synchronized` + `wait()/notifyAll()` | `lock.lock(); try {...} finally {lock.unlock();}`；`Condition.awaitNanos` | 可有多个条件、可超时、虚拟线程友好；代价是必须手写 `try/finally` |
| **`record ChannelConfig`**（[J01](../10-java21/J01_record.md)） | 带 getter 的不可变类 + 构造器校验 | `record ChannelConfig(int maxFrame, int outCapacity, int inCapacity) { 紧凑构造器校验 }` | 配置对象天然适合 record；`static ChannelConfig of(int maxFrame)` 是工厂方法 |
| **`RandomGenerator`**（Java 17，`java.util.random`） | `Random rnd; rnd.nextInt(...)`（没有 `long` 范围版本，常写 `(long)(rnd.nextDouble()*bound)` 有偏差） | `rng.nextLong(cap + 1)`：在 `[0, cap]` 内均匀取 `long` | 接口统一了 `Random`、`SplittableRandom`、`ThreadLocalRandom`；测试里传带种子的 `Random` 就确定了 |
| **try-with-resources + `AutoCloseable`** | 手写 `finally` 关闭 | `try (var srv = new MessageServer(...); var c = TcpMessageChannel.connect(...))` | 反向关闭、抑制异常；`close()` 要幂等 |
| **`var`**（[J08](../10-java21/J08_var.md)） | `MessageServer srv = new MessageServer(...)` | 测试里 `var p = pair(CFG);` | 右边已写类型时 |
| **`Objects.checkFromIndexSize`** | 手写 `off < 0 \|\| len < 0 \|\| off + len > arr.length` | `Objects.checkFromIndexSize(off, len, src.length)` | 抛标准的 `IndexOutOfBoundsException`，并正确处理 `off + len` 溢出 |

### 虚拟线程版本的备选设计（题面的"备选"）

```java
// 每个连接两条虚拟线程：读线程、写线程；有界队列做缓冲；阻塞 I/O 写成直线代码
Thread.ofVirtual().start(() -> {                 // 读线程
    var in = Channels.newInputStream(ch);        // 或直接用 SocketChannel 的阻塞 read
    byte[] header = new byte[4];
    for (;;) {
        in.readNBytes(header, 0, 4);             // 阻塞到凑齐 4 字节；EOF 时抛 / 返回不足
        int len = ByteBuffer.wrap(header).getInt();
        if (len < 0 || len > maxFrame) throw new FrameException(...);
        byte[] payload = in.readNBytes(len);
        inbox.put(payload);                      // ArrayBlockingQueue：满了就阻塞 → 不再读 → TCP 窗口缩小，天然的入站背压
    }
});
Thread.ofVirtual().start(() -> {                 // 写线程
    for (;;) { byte[] m = outbox.take(); out.write(frame(m)); }   // 部分写由阻塞 write 自动处理（循环到写完）
});
```

* **优点**：没有 `Selector`、没有兴趣集、没有 `wbuf`、没有 `wakeup`；部分读 / 部分写由阻塞 API 内部循环处理；背压由有界阻塞队列自然提供。**代码量约为 NIO 版的三分之一**。
* **缺点**：每个连接两条线程（虚拟线程便宜，但调度仍有开销和抖动）；`offer` 的"满了返回 false"要靠 `outbox.offer(m)`（`ArrayBlockingQueue` 的非阻塞版本）按**消息数**而不是**字节数**限界；难以精细控制延迟。
* **怎么选**：`networking_basics.md` §9.4。连接数很大、对延迟不极端的服务 → 虚拟线程；需要把 CPU 绑核、批处理、极低延迟 → `Selector` 或更底层（内核旁路）。

---

## 7. 追问预演

### Q1：为什么用一个 `Selector` 线程，不是一个连接一个线程？

**思考**：先说 C10K，再说本题只有一条连接的意义。
**答案要点**：线程每连接一个：栈内存（默认 ~1 MB 虚地址）、调度与上下文切换，数千连接开始吃力；`Selector` 让一个线程服务大量连接，只在就绪时才干活。本题只要一条连接，但接口设计成可扩展：把多个通道注册到同一个 `Selector` 即可。JDK 21 的虚拟线程让"每连接一线程"重新变得便宜（备选设计），代价是延迟抖动。
**可以说**：「`Selector` 是为连接数大设计的；连接数小而延迟敏感时，也可以让一个线程忙等轮询——那是内核旁路的思路。」

### Q2：怎么做到无锁？

**答案要点**：应用线程 ↔ I/O 线程之间是单生产者-单消费者：出站环（应用写、I/O 读）和入站环（I/O 写、应用读）都可以做成 ld01 的 SPSC 环（`setRelease`/`getAcquire`，无 CAS）。但本实现还有：`close`/`finishSending` 状态、阻塞 `poll(timeout)` 的等待（需要 park/unpark 或条件变量）。无锁版本把"等待"换成忙等或 `LockSupport.park`。何时值得：每秒千万级条数且 CPU 争用可测量时；这里的临界区只是几十字节拷贝，锁不是瓶颈（瓶颈是 `wakeup` 与线程交接，见 §5.7）。
**可以说**：「先测量；这里的开销在线程交接，不在锁。」

### Q3：对端掉电了（没有 FIN、没有 RST），我怎么知道？

**答案要点**：TCP 不通知：连接看起来还在，你发的数据没人确认，内核重传直到超时（Linux 默认可长达十几分钟）。检测办法：①应用层心跳（定期发一条空消息，超时没回就判定死亡）——最可靠；②TCP keepalive（`SO_KEEPALIVE`，默认空闲 2 小时才探测，可调但粒度粗）；③读/写超时。检测到后：关闭 → `ReconnectingClient` 重连。
**可以说**：「TCP 层面'没消息'和'死了'不可区分，所以需要应用层心跳。」

### Q4：重连之后消息不丢吗？怎么做到不丢？

**答案要点**：本实现不保证（at-most-once 尽力而为，`abandonedBytes` 诚实记账）。要不丢：应用层序号（每条消息递增）+ 接收方周期性确认已收到的最大连续序号 + 发送方保留未确认消息（重传缓冲）；重连时握手交换"我收到哪了"，发送方从那里重发；接收方对序号去重。这就是 at-least-once + 去重 = effectively-once；FIX 会话层就是这么做的（序号 + 重传请求）。代价：发送方要保留未确认的消息（有界 + 满了向上背压）。
**可以说**：「TCP 的可靠性只在一条连接内。跨连接的可靠性是应用的事。」

### Q5：Nagle 和 `TCP_NODELAY`？

**答案要点**：Nagle 算法把小写合并，等 ACK 或凑够一个段再发，节省包数；与对端的**延迟确认**相撞会产生约 40 ms 停顿（写-写-读模式）。消息通道必须 `TCP_NODELAY`。我们自己已经在应用层批量（出站环 + 一次 `write` 多条），所以不需要 Nagle 替我们合并。详见 `networking_basics.md` §5。
**可以说**：「我自己做批处理，所以关掉 Nagle。」

### Q6：如果应用一直不调用 `poll()` 会怎样？

**答案要点**：入站环满 → 停止读 → 对端被拖慢（背压）。这是设计意图；但如果同一个线程既 `offer` 又 `poll`，而 `offer` 在等空间、对端在等我们读 → **死锁**。所以：收发在不同线程，或者用非阻塞 `offer`（返回 `false` 后去 `poll` 腾空间）。这也是"消息通道的使用者有责任持续消费"的契约。
**可以说**：「背压是双向的契约：我保证有界，你保证消费。」

### Q7：行情（可以丢）和订单（不能丢）的背压策略一样吗？

**答案要点**：不一样。订单：不能丢，满了就停止接收新单并报警（fail closed）。行情：陈旧的数据没价值，可以**丢弃旧的、保留新的**（conflation：同一品种只保留最新报价），或让消费者在落后时"跳到最新"。通道层提供的是"有界 + 向上游表达满"，策略在上层选。
**可以说**：「通道负责说'满了'，丢什么由业务决定。」

### Q8：为什么容量必须 ≥ `maxFrame + 4`？

**答案要点**：入站环必须能装下一条最大的完整消息；否则环里是半条消息、已经满了，无法继续读也凑不齐——死锁（测试 `minimalBuffersStillDeliverEverythingInOrder` 用恰好等于的最小容量验证）。出站同理：不满足则最大消息永远 `offer` 失败。
**可以说**：「容量要大于最大的原子单位。」

### Q9：边缘触发和水平触发（epoll）？

**答案要点**：Java NIO 的 `Selector` 在 Linux 上基于 epoll，对应用表现为**水平触发**：只要还有数据没读完，下次 `select` 仍然报告就绪。所以我们每次可以少读一点（受入站环空位限制）而不丢事件。边缘触发要求每次读到 `EAGAIN`，否则丢事件，C/C++ 里常见。
**可以说**：「NIO 给我们的是水平触发语义，所以可以放心地只读一部分。」

### Q10：TLS 怎么接进来？

**答案要点**：`SSLEngine` 的 `wrap`/`unwrap` 处于应用字节和网络字节之间：入站网络字节 → `unwrap` → 应用字节 → 喂给 `FrameDecoder`；出站应用字节 → `wrap` → 网络字节 → `wbuf`。难点：`unwrap` 可能需要更多输入（`BUFFER_UNDERFLOW`）、握手期间需要读写交替（`NEED_WRAP/NEED_UNWRAP/NEED_TASK`）。本结构（环 + 中转缓冲区 + I/O 线程）正好是放它的位置。
**可以说**：「TLS 是在字节流和成帧之间多一层有状态的转换。」

---

## 8. 常见误区

1. **以为一次 `read` = 一条消息**。→ 粘包/拆包。→ 长度前缀 + 增量解码器；测试在每个切分点切开（`decoderHandlesEverySplitPointOfAStream`）。
2. **忽略 `write` 的返回值 / 写了一部分就当写完**。→ 丢数据，且只在慢网络、大消息时偶发。→ 保留 `wbuf` 与位置，等 `OP_WRITE`（测试 `largeWriteIsSplitAcrossPartialWritesAndStaysIntact`，几 MB 的消息）。
3. **`OP_WRITE` 一直开着**。→ `select()` 立刻返回，CPU 100%。→ 只在有数据要写时开。
4. **入站不限界 / 满了还读**。→ OOM；或读出来的字节没处放。→ 入站环 + 满了关闭 `OP_READ`。
5. **暂停读之后没人叫醒**。→ 通道永久卡住（偶发、依赖时序）。→ `poll` 腾出空间后 `wakeup`。**两个 `poll` 版本都要**（测试里分别有阻塞版和自旋版）。
6. **忘了 `selectedKeys` 的语义**：不清除 / 读旧的 `readyOps`。→ 重复处理或误处理。→ `if (selectedKeys().remove(key))`。
7. **容量刚好小于最大帧 + 头**。→ 死锁。→ 构造器校验 `>= maxFrame + 4`。
8. **长度字段不校验**。→ 恶意 4 字节让你分配 2 GB。→ 看到头就校验，粘性失败。
9. **EOF 一律当正常结束**。→ 帧中间的 EOF 被当作"对端优雅关闭"，吞掉了半条消息。→ `hasTruncatedTail()` ⟹ `EOFException`。
10. **关闭时不管接收缓冲区里的数据**。→ `close()` 时内核发 RST，对端丢掉还没读走的数据。→ 优雅关闭：`shutdownOutput` → 等对端 EOF → `close`。
11. **测试里用 `Thread.sleep(100)` 判断"应该已经到了"**。→ 慢机器上偶发失败。→ 带截止时间的轮询（`Await.until`），失败信息写清楚在等什么。
12. **重连后假设消息不丢**。→ 见 Q4。

---

## 9. 自测题

**Q1（概念）**：为什么说"`read` 返回 5 字节"不代表什么？列出三种合法的"收到的块"划分方式，对应同一个 13 字节的字节流。

<details><summary>答案</summary>

TCP 不保留写的边界，`read` 返回多少取决于内核已收到多少、你的缓冲区多大、调度时机。13 字节可以是 `13`、`5+6+2`、`1×13`、`4+9` 等任意划分。正确的处理是把所有收到的字节喂给增量解码器，由它决定何时凑成了一整帧。
</details>

**Q2（计算）**：`maxFrame = 100`，`inCapacity = 104`。对端发来 3 条各 100 字节的消息（每条帧 104 字节），应用一直不 `poll`。入站环里最多有多少字节？为什么这时通道不会死锁？应用 `poll` 一条之后会发生什么？

<details><summary>答案</summary>

最多 104 字节（恰好一条完整帧）。I/O 线程发现 `free() == 0`，不再监听 `OP_READ`；第二、三条留在内核接收缓冲区 / 对端。不死锁是因为容量 ≥ `maxFrame + 4`：环里一定能装下至少一条完整帧，应用能 `poll` 走它。`poll` 之后环空出 104 字节，`readPaused` 为真 ⟹ `wakeup`，I/O 线程重算兴趣集，重新打开 `OP_READ`，读第二条。
</details>

**Q3（找 bug）**：下面这段 I/O 循环有什么问题？

```java
while (true) {
    selector.select();
    for (SelectionKey k : selector.selectedKeys()) {
        if (k.isReadable()) doRead();
        if (k.isWritable()) doWrite();
    }
}
```

<details><summary>答案</summary>

①没有 `selectedKeys().clear()`（或迭代器 `remove`）：key 一旦被选中会一直留在集合里，下一轮即使没就绪也会被处理（读旧的 `readyOps`）；②没有根据状态更新兴趣集：`OP_WRITE` 若一直开着会忙等，若从不开则永远写不出去；③没有处理 `wakeup`——应用线程 `offer` 之后无法叫醒 I/O 线程去写。
</details>

**Q4（设计）**：`ReconnectingClient.offer` 在断线期间返回 `true`，但随后进程崩溃，消息丢了。这违反了什么契约？怎么在文档里诚实地表达？怎么升级为"不丢"？

<details><summary>答案</summary>

`true` 只表示"进入了本进程的有界 pending 队列"，不是"对端收到"。文档要写清：at-most-once 尽力而为，进程崩溃/连接断开时已接受的消息可能丢失；`abandonedBytes` 统计已知丢失量。升级：持久化的发送队列（落盘/复制）+ 序号 + 对端确认 + 重传 + 去重，这样 `true` 才能表示"已持久化"，崩溃后可恢复。
</details>

**Q5（小编程）**：给 `Backoff` 加一个"稳定连接 N 秒后才重置"的行为（避免抖动的连接每次一连上就重置退避，造成快速重连风暴）。需要改哪些地方？

<details><summary>答案</summary>

`ReconnectingClient.run` 里连接成功时不立刻 `backoff.reset()`，而是记下 `connectedAt`；在 `pump` 返回（连接断开）后，若 `now - connectedAt >= stableAfter` 才 `reset()`，否则保留当前退避并继续增长。`Backoff` 本身不变。需要一个可注入的时钟（`LongSupplier nanoTime`）才能确定性地测试。
</details>

---

## 10. 延伸阅读

* W. Richard Stevens, *UNIX Network Programming, Vol. 1* —— 套接字、非阻塞 I/O、`select`/`poll`、半关闭与 `SO_LINGER` 的权威讲解。
* RFC 9293（TCP，2022 年对 RFC 793 的更新）、RFC 896（Nagle）、RFC 1122 §4.2.3.2（延迟确认）。
* `java.nio.channels.Selector` / `SelectionKey` / `SocketChannel` 的 Javadoc —— `wakeup()` 的粘性语义、`selectedKeys` 与 `readyOps` 的更新规则、`shutdownOutput`。
* Netty 的 `LengthFieldBasedFrameDecoder` 与 `ByteToMessageDecoder`（文档与源码）—— 工业级的"增量成帧 + 累积缓冲区 + 背压（auto-read 开关、水位线）"实现，对照本题的最小版本读。
* JEP 444（虚拟线程）与 JDK 21 的 `Thread.ofVirtual()` Javadoc；Ron Pressler 的相关文章 —— 为什么阻塞式写法重新可行。
* Marc Brooker, 「Exponential Backoff And Jitter」（AWS Architecture Blog）—— 几种抖动策略的模拟比较。
* Michael Nygard, *Release It!* —— 超时、断路器、舱壁、退避：连接管理的稳定性模式。
* 本 kit：`study/30-articles/ld01_spsc_channel.md`（共享内存 SPSC 环）、`study/00-foundations/networking_basics.md`（TCP / `Selector` / 虚拟线程）、`loop/rounds/04_sd/sd03_low_latency_trading_system/model_answer.md` §7.4（订单网关：会话序号、心跳、cancel-on-disconnect）。
