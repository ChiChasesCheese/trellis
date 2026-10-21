# ld03 · 异步 TCP 消息通道：成帧、部分 I/O、背压、半关闭、重连 —— 讲义

> 读者：只会基本 Java，没学过网络编程、NIO、背压；TCP、Nagle、`Selector`、虚拟线程用到时现讲。所有数字来自回环接口（127.0.0.1），反映软件和内核开销，不是网线。

---

## 1. 问题是什么

### 1.1 用大白话

一个程序（行情网关）不停发**消息**，另一个（策略）接收，之间只有一条 TCP 连接。写一个小库，让两端只用两个方法：

```java
boolean offer(byte[] message)   // 发一条消息；"满了"就返回 false
byte[]  poll()                  // 收一条消息；没有就返回 null
```

难点全在"TCP 不是消息，是水管里的字节"：发两条消息对方可能收到"一条半"再"半条"（**消息边界不存在**）；网络慢时系统只肯接收一部分（**部分写**）；对方读得慢水管就满，要把"满"一路传回调用 `offer` 的人而非内存里无限堆积（**背压**）；连接会断。

关键词：**bounded**（每层有上限）、**local circular buffers**（一个放待发字节，一个放收到但没凑成消息的字节）、**partial-I/O framing**（部分读写时的成帧）。

### 1.2 手算：字节流上的两条消息

每条消息前加 **4 字节长度**（大端），后面是内容。发 `"AB"`（2 字节）和 `"CDE"`（3 字节），线上字节：

```text
消息1           消息2
00 00 00 02 41 42 | 00 00 00 03 43 44 45          共 13 字节（41 = 'A'，42 = 'B'，43 = 'C' …）
```

`read` 把这 13 字节切成任意几块，假设 `5 + 6 + 2`：

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

出站环 64 字节，每条帧 36 字节（4 + 32），对方一直不读：

```text
offer #1 → 环 36/64   true
offer #2 → 环 72 > 64 放不下 → false    ← 调用方知道"满了"，由它决定等 / 丢 / 降级
（I/O 线程把环里的字节写进内核发送缓冲区；对方不读，内核缓冲区也满了，write 返回 0；环不再被腾空）
```

对方开始读 → 内核缓冲区腾出空间 → `write` 又能写 → 出站环腾出空间 → `offer` 又返回 `true`。**"满"从对方应用穿过两端内核，一路传回我们的调用者。**

### 1.4 四个 Part

1. `ByteRing` + `FrameCodec` + `FrameDecoder`：纯内存，环形缓冲区、4 字节长度前缀、增量解码器。
2. `TcpMessageChannel` / `MessageServer`：一个 `Selector` I/O 线程，部分读写，EOF，半关闭。
3. 背压与有界性：入站环满了停止读；最小缓冲区压力测试。
4. `Backoff` + `ReconnectingClient`：指数退避，断线重连，断线期间有界 pending。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 TCP 是字节流，不是消息流

TCP 是一对**可靠、有序的字节管道**（不丢不重，先写先到），但**不保留**每次 `write` 的边界。否则会写出"一次 `read` = 一条消息"的代码，开发机上能跑，一上线偶发错乱。

```text
发送方的 write 调用:   [AAAA]   [BBBBBB]   [CC]
TCP 在线上的分段:      [AAAABB]  [BBBB]  [CC]        ← 由 MSS、拥塞窗口、Nagle 等决定，不是你决定
接收方的 read 调用:    [AAAABBBBBBCC] 一次读完    或   [AAAAB] [BBBBB] [BCC]    ← 同样不是你决定
```

### 2.2 成帧（framing）：自己给消息加边界

三种办法：**定长**（每条固定 N 字节，最简单但浪费，变长不行）；**分隔符**（以 `\n` 结尾，HTTP/1 头、Redis 旧协议；人可读，但内容里不能出现分隔符要转义，要逐字节扫描）；**长度前缀** `[长度][内容]`（二进制安全，解码只看头，可一次分配，但必须保护长度字段）。这里用长度前缀，4 字节**大端**（网络字节序，Java `ByteBuffer` 默认也是大端）。

**必须防御长度字段**：对端发来 `0x7FFFFFFF`（21 亿），若"看到长度就分配那么多字节再等"，一个恶意（或出 bug）的 4 字节就搞垮内存。所以①约定 `maxFrame`；②**只看到 4 字节头就检查**，超过立刻报错；③长度为负同样报错。报错后流已失去同步，只能断开重连，所以解码器"粘性失败"。

### 2.3 阻塞 vs 非阻塞 I/O、`Selector`

* **非阻塞**：`read` 没数据立刻返回 0；`write` 发送缓冲区满时返回 0 或只写一部分。
* **`Selector`**：一个线程盯着很多套接字，问内核"哪些就绪"；`select()` 睡眠直到有套接字就绪或别的线程 `selector.wakeup()`。
* **兴趣集**：`OP_READ`（有数据可读）、`OP_WRITE`（发送缓冲区有空位）。
* **规则 1：就绪 ≠ 完成**。`OP_READ` 只表示"现在读不会阻塞"，不表示"一条完整消息到了"。
* **规则 2：`OP_WRITE` 不要常开**。有空位它就一直就绪，`select()` 立刻返回，循环变 100% CPU 忙等。**只在"还有数据要写"时打开**，写完就关。
* **规则 3：谁改兴趣集**。只有 I/O 线程改；别的线程设状态 + `selector.wakeup()`，由 I/O 线程在循环顶部**重算**。`wakeup()` 是"粘性"的：当时没有 `select` 在进行，下次 `select` 立刻返回——不丢唤醒。
* **规则 4：`selectedKeys` 和 `readyOps`**。只有被选中 key 的 `readyOps` 是新鲜的；被 `wakeup` 叫醒时没有 key 被选中，`readyOps()` 可能是**上一轮旧值**。所以写 `if (selector.selectedKeys().remove(key)) { 看 readyOps }`。

### 2.4 `ByteBuffer` 的三个游标

`position`（下一个读/写位置）、`limit`（可操作区域末端）、`capacity`；写完要 `flip()` 才能读，读完要 `clear()` 或 `compact()` 才能再写。`ByteRing.write(src)` 从 `src.position` 读 `n` 字节并前进 `position`，`read(dst)` 反之。`allocateDirect` 的堆外缓冲区让 `SocketChannel` 读写少一次拷贝，两个 16 KB 中转缓冲区（`rbuf`、`wbuf`）用它。

### 2.5 环形缓冲区（字节版）

固定容量数组，读写位置到末尾绕回开头。`ByteRing` 是单线程字节环，容量任意正整数（用 `%` 而非 `& mask`）。变量 `head`（下一个读位置）和 `size`；写入位置 = `(head + size) % capacity`；回绕时一次拷贝拆成两段。

```text
容量 8，head=6，size=4（占用下标 6,7,0,1）：  [ 2 3 . . . . 0 1 ]    写入位置 (6+4)%8 = 2
读 4 字节：先读下标 6,7（尾部这一段），再读 0,1（开头这一段）
```

### 2.6 背压（backpressure）

下游处理不过来时让上游**慢下来**，而不是中间堆积。没有背压：快生产者 + 慢消费者 = 队列无限增长 = 内存耗尽或延迟爆炸。**每层缓冲区都要有上限，满了向上游表达"满了"。** 这里四层：

```text
 应用线程 ──offer──▶ [出站环 outCapacity] ──I/O线程 write──▶ [内核发送缓冲区] ══网络══▶ [内核接收缓冲区] ──I/O线程 read──▶ [入站环 inCapacity] ──poll──▶ 应用线程
      ▲ false 表示满了                          ▲ write 返回 0                         TCP 窗口缩小到 0               ▲ 满了就不再监听 OP_READ
```

入站环满 → I/O 线程不再读 → 内核接收缓冲区满 → TCP 向对端通告窗口 = 0 → 对端内核发送缓冲区满 → 对端 `write` 返回 0 → 对端出站环满 → 对端 `offer` 返回 `false`。**一个应用的"没空读"，穿过六层，变成另一个应用的"满了"。**Little 定律（L = λ·W）：缓冲区里的消息数 = 到达速率 × 停留时间，停留时间无上限则 L 无上限。

### 2.7 EOF、半关闭与 RST

* 对端 `close()`（或 `shutdownOutput()`）→ 发 **FIN**；本端 `read` 返回 **-1**（EOF）。EOF 是"对端不会再发了"，**不等于"我也该关了"**：TCP 全双工，可只关一个方向（**半关闭**）；`shutdownOutput()` 本端不再发送但仍可接收，`finishSending()` 就是它（先刷完已接受的消息）。
* **RST**：连接被重置。原因：对端进程崩溃；向已关闭端口发数据；**`close()` 时接收缓冲区里还有没读的数据**——内核发 RST 而非 FIN，对端未读完的数据可能被丢。所以"优雅关闭"是**先 `shutdownOutput`，等对端 EOF，再 `close`**。
* EOF 恰在**一帧中间**（读到了头和半个内容）= 流被截断，是错误（`EOFException`），不是正常结束。

### 2.8 锁与条件变量

共享缓冲区用一把 `ReentrantLock` 保护；"等条件成立"用 `Condition`：`while (!条件) cond.await();`——必须 `while`（可能虚假唤醒或条件又被改）；改变条件的线程 `signalAll()`。**临界区只做内存拷贝，不做系统调用**（持锁睡让所有人等）。用 `ReentrantLock` 而非 `synchronized`：JDK 21 虚拟线程上 `synchronized` 里阻塞会**钉住**（pin）载体线程；`ReconnectingClient` 的管理线程是虚拟线程，所以统一 `ReentrantLock`。

### 2.9 重连与指数退避

对端宕机时每 1 毫秒重试，浪费 CPU，且对端恢复瞬间"惊群"——大量客户端同时重连把刚恢复的服务打死。**指数退避**：第 1 次等 `initial`，之后每次翻倍（封顶 `max`）；**抖动（jitter）**：在 `[0, 当前延迟]` 随机取值，分散重试时刻；成功后**重置**。

**重连后的语义（务必讲清楚）**：TCP 只保证**一条连接存续期间**的有序不丢。连接断了，已进旧连接内核缓冲区但对端没读走的字节**可能丢**，你不知道对端处理到哪。要不丢需**应用层序号 + 确认 + 重传**（at-least-once）加对端去重（effectively-once）；否则只是 **at-most-once 的尽力而为**。

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

**错 / 慢的输入**：

| 输入 | 暴露的问题 |
|---|---|
| 2 条消息被一次 `read` 收到 | 被当 1 条（粘包） |
| 2,000 字节消息，`buf` 只有 1,024 | 被切成两条（拆包） |
| 对方慢，我方一直发 | `LinkedBlockingQueue` 无界，内存无限涨；`write` 在内核缓冲区满时**阻塞**调用线程，无"满了"概念 |
| 1 万个连接 | 1 万个线程，每栈 1 MB（C10K 问题） |
| 连接断开 | 线程默默退出，上层不知道，没有重连 |
| 对端关闭一半 | `read` 返回 -1 就退出，分不清"正常结束"和"消息中间被截断" |
| 恶意长度 | `readInt()` 后 `new byte[len]`，一个 4 字节包就 OOM |

---

## 4. 一步一步改进

### 步骤 1：长度前缀成帧

`[len:4][payload]`：接收方读 4 字节知道读多少，之后字节一定属于这条消息。**新问题**：一次 `read` 可能只有半个头，要存"读到一半"的状态 → 步骤 2。

### 步骤 2：增量解码器

有状态对象：`feed(bytes)` 喂任意长度字节，`next()` 吐出完整消息，不够返回 `null`。验证：在**每个**切分点切开结果必须相同；逐字节喂；随机切块。

### 步骤 3：缓冲区有界 → 环形缓冲区

缓冲区可增长的话，对端发一堆没凑成消息的字节内存就无限涨。用固定容量 `ByteRing`，容量 ≥ `maxFrame + 4`（否则最大消息永远凑不齐——死锁）。`feed` 放不下的部分**不消费**，返回实际消费数，调用方必须先 `next()` 腾空间。用环不用 `arraycopy` 前移：前移每次 O(n)，环只改 `head`，O(1)。

### 步骤 4：非阻塞 I/O + 一个 `Selector` 线程

应用线程只与两个内存缓冲区打交道（`offer` 写出站环、`poll` 读入站环），网络 I/O 全在一个 I/O 线程里用 `Selector` 做，`offer`/`poll` 不因网络慢而阻塞；同一 `Selector` 注册多个通道即可扩展到多连接。

### 步骤 5：处理部分写

`ch.write(buf)` 可能只写出一部分。出站环字节先拷到 `wbuf`；写出多少就前进多少 `position`；剩下的留着，下次 `OP_WRITE` 就绪**继续写 `wbuf`**，写空了才从环再取。**新手最常漏**：扔掉 `write` 返回值，或写一部分就丢弃剩余。

### 步骤 6：每轮循环重新计算兴趣集

应用线程不直接改兴趣集（易竞态）。I/O 线程每轮顶部**在锁内**按状态算：

```text
OP_READ  ⇐ 对端没关闭 且 入站环还有空位
OP_WRITE ⇐ 还没发 FIN 且 (wbuf 里还有数据 或 出站环非空)
```

应用线程改变状态（`offer`、`poll` 腾出空间、`close`）就 `selector.wakeup()` 叫醒 I/O 线程重算；"该关注什么"的决定都在一个线程里，没有竞态。

### 步骤 7：入站背压——满了就不读，`poll` 负责叫醒

入站环满 ⟹ 兴趣集去掉 `OP_READ`（内核缓冲区填满，TCP 窗口缩到 0，对端被拖慢）；`poll` 取走一条（腾出空间）后**必须 `wakeup()`**，I/O 线程才会重算并重新打开 `OP_READ`。**很容易漏的 bug**：漏了唤醒，I/O 线程睡在 `select()` 上、兴趣集是 0，通道从此"卡住"（自旋 `poll()` 的消费者永远停在几条之后）。优化：`readPaused` 标志，只有"确实暂停了读"才唤醒，省掉每次 `poll` 的 `wakeup` 系统调用。

### 步骤 8：EOF、截断与半关闭

* `read` 返回 -1：`peerClosed = true`（不再监听读）。缓冲区里有一截**不完整的帧**（`hasTruncatedTail()`）⟹ 错误（`EOFException`），通道关闭，但之前收齐的完整消息仍可 `poll`。
* `finishSending()`：状态变 `FINISHING`（之后 `offer` 抛异常）；I/O 线程等出站环和 `wbuf` 都空了再 `shutdownOutput()` 发 FIN；本端已发 FIN 且对端也已 EOF ⟹ 自动关闭。
* 不在 EOF 时立刻 `close`：对端可能只是半关闭，我们这边还有话说。

### 步骤 9：并发设计——一把锁，系统调用在锁外

一把 `ReentrantLock` 保护两个环和所有标志；`Condition changed` 用于 `poll(timeout)`、`offer(msg, timeout)`、`awaitClosed`——I/O 线程在"收到数据"/"腾出出站空间"/"状态变了"时 `signalAll()`。**临界区内只有内存拷贝**，`read`/`write`/`select` 全在锁外。不无锁：瓶颈是系统调用不是锁（锁内是几十字节拷贝）；无锁 SPSC 环见 ld01。

### 步骤 10：重连——pending 队列 + 退避 + 诚实的语义

`offer` 总是先进有界 `pending`（按"已编码字节"计，上限 = `cfg.outCapacity()`）；管理线程连接成功后把 `pending` 按序搬进通道；通道断了 ⟹ `unsentBytes` 记入 `abandonedBytes`（诚实：这些字节丢了）、丢弃旧通道、退避、重连。

---

## 5. 逐段讲解法

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

`tail = (head + size) % buf.length` 是写入起点；`first = min(n, buf.length - tail)` 是起点到末尾能放多少，剩下 `n - first` 从下标 0 开始，读同理；两次 `src.get(...)` 之间 `position` 自动前进。满时 `n = 0`，两次拷贝都是空操作，不需特判。

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

`ring.size() < HEADER` ⟹ `null`。`peekInt()` 不消费，"头到了但负载没到"时什么都不改变，下次 `feed` 后再看。非法长度立刻抛并存进 `failed`：之后每次调用都抛同一异常（**粘性**）。凑齐了才 `skip(HEADER)` + `take(len)`。

### 5.3 `offer` 与 `poll`

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

* `wasEmpty`：出站环**从空变非空**才需唤醒 I/O 线程（非空时它已在等 `OP_WRITE`）。设置兴趣集和读 `out.isEmpty()` 在同一把锁里，不存在"I/O 线程刚算出无写、我们看到环非空因此没唤醒"的间隙。
* `IllegalStateException` 与 `false` 区分：`false` 是"暂时满了，稍后再来"，异常是"通道已不能发"。

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

`readPaused`：I/O 线程因入站环满暂停读时置位；这里取出一条消息后清除并在**锁外**调用 `wakeup()`。

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

循环里先尝试取，再判断"不会再有消息"（`inboundFinishedLocked`）和超时，`awaitNanos` 返回剩余时间。范式：`for(;;) { 先检查条件; 不满足就 await }`。

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

循环顶部（锁内）：该发 FIN 了吗（`FINISHING` 且两缓冲都空）；全部结束了吗（`finSent && peerClosed`）；然后算兴趣集（为 0 时 `select()` 睡到 `wakeup()`，预期）。`selectedKeys().remove(key)` 即规则 4。任何异常 → `failLocked(t)`；`finally` 关闭 socket 和 selector，状态置 `CLOSED`、`signalAll`。

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

`rbuf.limit(min(rbuf.capacity(), room))`：**读的量不超过入站环空位**，`feed` 一定吃得下。`n < 0` 即 EOF；`hasTruncatedTail()` 为真 ⟹ `failLocked(EOFException)`。

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

外层 `for` 最多 16 轮：避免出站环一直有数据时写循环饿死读。`wbuf` 没写空就保持原样等下次 `OP_WRITE`；`n == 0` 立刻返回（内核缓冲区满）。每次从环里取走数据后 `changed.signalAll()`：唤醒阻塞在 `offer(msg, timeout)` 里等空间的线程。

### 5.6 重连

```java
    public long next() {
        long d = current;
        current = current > maxMs / multiplier ? maxMs : Math.min(maxMs, current * multiplier);
        return d;
    }
```

`current > maxMs / multiplier ? maxMs : min(maxMs, current * multiplier)`：先用除法判断会不会超上限，**避免乘法溢出**（`maxMs` 可以是 `Long.MAX_VALUE`）。

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

`pump` 持客户端锁，把 `pending` 队首消息交给通道：被接受才 `pollFirst`；满了就 `break`，`wake.await(10ms)` 周期性醒来再试。断开判断 `!ch.isOpen() || ch.isPeerClosed()`（对端 EOF 当断线，应用协议无半关闭）；`abandonedBytes += ch.unsentBytes()`：没写进 socket 的字节，丢了。

### 5.7 数据（3 次运行）

```text
throughput: 2,000,000 msgs x 32 B（含 4 B 头）, 中位数 86–114 ms      => 17.5 – 23.3 M msg/s（约 630–840 MB/s）
round-trip our channel  : p50 36.1 us, p99 46.5 us, p99.9 52.6 us, max 147–165 us
round-trip raw blocking : p50 12.4 us, p99 18.1 us, p99.9 23.0 us, max 59–121 us
backpressure: rings 4 KB/4 KB   -> sender accepted ~16,500 msgs (~593 KB) before a 200 ms stall; receiver drained the same count
backpressure: rings 64 KB/64 KB -> sender accepted ~18,200 msgs (~656 KB) before a 200 ms stall; receiver drained the same count
```

* **吞吐**（回环、32 字节、一发一收两线程）：每秒千万级条数，瓶颈是批量系统调用和线程交接，不是协议。
* **往返延迟：我们的通道 p50 36 µs，裸阻塞 socket 乒乓 p50 12 µs。** 多出的约 24 µs 是**线程交接**：一次往返里，应用线程 → I/O 线程（`wakeup` 系统调用 + 线程被唤醒）、I/O 线程 → 应用线程（`signalAll` + `unpark`）各两次。**这正是低延迟系统"热路径 run-to-completion、不要线程交接"的原因**，也是常让应用线程自己轮询网卡的原因。这套通道为**吞吐和易用**设计，不是 µs 级往返。（macOS 回环数字，Linux 会不同。）
* **背压**：请求 `SO_SNDBUF`/`SO_RCVBUF` = 4096，macOS 读回来发送 65,328 字节、接收约 0.5 MB（内核自行放大），**真正的缓冲主要在内核里**：发送端被堵住前能灌进 ~590–660 KB。**出站环**从 4 KB 加到 64 KB，多接受约 1,700 条（≈ 60 KB，符合预期）；但加大**接收端入站环****没有**多接受任何消息——读回的内核接收缓冲区同时变小约 57 KB，原因不明。**教训：多层缓冲相加，总量由最大那层（这里是内核）决定；想让背压早生效要有意设小内核缓冲区（Linux 上手动设置 `SO_RCVBUF`/`SO_SNDBUF` 会关闭自动调优）。**
* **接收方收到的条数 = 发送方接受的条数**（"equal: true"）：没丢没重——验证的核心。

---

## 6. Java 21 特性小课

| 特性 | 旧写法（Java 8 风格） | 新写法 | 多做了什么；什么时候别用 |
|---|---|---|---|
| **虚拟线程** | `new Thread(this::run)` + 线程池；或回调式 `CompletableFuture` 链写"连接-等待-重试" | `Thread.ofVirtual().name("reconnecting-client-" + addr).start(this::run)`，里面写直线阻塞代码 | 阻塞 I/O / `Condition.await` 时卸载，不占平台线程；适合"大部分时间在等"的任务（重连管理）。**不适合**热路径；`synchronized` 里阻塞会钉住载体线程 |
| **`ReentrantLock` + `Condition`** | `synchronized` + `wait()/notifyAll()` | `lock.lock(); try {...} finally {lock.unlock();}`；`Condition.awaitNanos` | 可多条件、可超时、虚拟线程友好；代价是手写 `try/finally` |
| **`record ChannelConfig`** | 带 getter 的不可变类 + 构造器校验 | `record ChannelConfig(int maxFrame, int outCapacity, int inCapacity) { 紧凑构造器校验 }` | 配置对象天然适合 record；`of(int maxFrame)` 是工厂方法 |
| **`RandomGenerator`**（Java 17） | `Random`（无 `long` 范围版本，常写有偏差的 `(long)(rnd.nextDouble()*bound)`） | `rng.nextLong(cap + 1)`：`[0, cap]` 内均匀取 `long` | 接口统一 `Random`、`SplittableRandom`、`ThreadLocalRandom`；带种子的 `Random` 即确定 |
| **try-with-resources / `var`** | 手写 `finally` 关闭；`MessageServer srv = new MessageServer(...)` | `try (var srv = new MessageServer(...); var c = TcpMessageChannel.connect(...))` | 反向关闭、抑制异常，`close()` 要幂等；`var` 只在右边已写类型时 |
| **`Objects.checkFromIndexSize`** | 手写 `off < 0 \|\| len < 0 \|\| off + len > arr.length` | `Objects.checkFromIndexSize(off, len, src.length)` | 抛标准 `IndexOutOfBoundsException`，并正确处理 `off + len` 溢出 |

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

* **优点**：没有 `Selector`、兴趣集、`wbuf`、`wakeup`；部分读写由阻塞 API 处理，背压由有界阻塞队列提供；**代码量约为 NIO 版的三分之一**。
* **缺点**：每连接两条线程（调度有开销和抖动）；"满了返回 false"靠 `ArrayBlockingQueue` 的 `outbox.offer(m)`，按**消息数**而非**字节数**限界；难精细控制延迟。
* **选择**：连接数很大、延迟不极端 → 虚拟线程；需绑核、批处理、极低延迟 → `Selector` 或内核旁路。

---

## 7. 追问预演

### Q1：为什么用一个 `Selector` 线程，不是一个连接一个线程？

C10K：每连接一线程，栈内存（~1 MB 虚地址）、调度与上下文切换，数千连接就吃力；`Selector` 让一个线程服务大量连接，只在就绪时干活。这里只一条连接，但多通道注册同一 `Selector` 即可扩展。虚拟线程让"每连接一线程"重新变便宜（备选设计），代价是延迟抖动。连接数小而延迟敏感时也可一个线程忙等轮询——内核旁路思路。

### Q2：怎么做到无锁？

出站环（应用写、I/O 读）和入站环（I/O 写、应用读）都是 SPSC，可做成无锁环（`setRelease`/`getAcquire`，无 CAS）。但还有 `close`/`finishSending` 状态、阻塞 `poll(timeout)` 的等待（换成忙等或 `LockSupport.park`）。每秒千万级条数且 CPU 争用可测量才值得；这里临界区只是几十字节拷贝，瓶颈是 `wakeup` 与线程交接（§5.7）——先测量。

### Q3：对端掉电了（没有 FIN、没有 RST），怎么知道？

TCP 不通知：连接看似还在，你发的数据没人确认，内核重传直到超时（Linux 默认可长达十几分钟）。检测：①应用层心跳（定期发空消息，超时没回判定死亡）——最可靠；②TCP keepalive（`SO_KEEPALIVE`，默认空闲 2 小时才探测，粒度粗）；③读/写超时。检测到后关闭 → 重连。TCP 层面'没消息'和'死了'不可区分，需要应用层心跳。

### Q4：重连之后消息不丢吗？怎么做到不丢？

本实现不保证（at-most-once 尽力而为，`abandonedBytes` 诚实记账）。要不丢：应用层递增序号 + 接收方周期性确认已收到的最大连续序号 + 发送方保留未确认消息（重传缓冲）；重连时握手交换"我收到哪了"，发送方从那里重发，接收方按序号去重——at-least-once + 去重 = effectively-once；FIX 会话层就这么做。代价：发送方保留未确认消息（有界，满了向上背压）。TCP 的可靠性只在一条连接内，跨连接是应用的事。

### Q5：Nagle 和 `TCP_NODELAY`？

Nagle 把小写合并，等 ACK 或凑够一个段再发；与对端**延迟确认**相撞产生约 40 ms 停顿（写-写-读模式）。消息通道必须 `TCP_NODELAY`；我们已在应用层批量，不需要 Nagle。

### Q6：应用一直不调用 `poll()` 会怎样？

入站环满 → 停止读 → 对端被拖慢，是设计意图；但同一线程既 `offer` 又 `poll`，`offer` 等空间、对端等我们读 → **死锁**。所以收发在不同线程，或用非阻塞 `offer`（返回 `false` 后去 `poll`）。背压是双向契约：我保证有界，你保证消费。

### Q7：行情（可以丢）和订单（不能丢）背压策略一样吗？

不一样。订单不能丢，满了停止接收新单并报警（fail closed）。行情陈旧即无价值，可**丢旧留新**（conflation：同品种只保留最新报价）或让落后的消费者"跳到最新"。通道层提供"有界 + 向上游表达满"，丢什么由业务决定。

### Q8：为什么容量必须 ≥ `maxFrame + 4`？

入站环必须装得下一条最大完整消息；否则环里是半条消息且已满，无法继续读也凑不齐——死锁。出站同理：最大消息永远 `offer` 失败。

### Q9：边缘触发和水平触发（epoll）？

NIO `Selector` 对应用表现为**水平触发**：还有数据没读完，下次 `select` 仍报就绪，所以可少读一点（受入站环空位限制）而不丢事件。边缘触发要求读到 `EAGAIN`，否则丢事件。

### Q10：TLS 怎么接进来？

`SSLEngine` 的 `wrap`/`unwrap` 处于应用字节和网络字节之间：入站 → `unwrap` → 喂 `FrameDecoder`；出站 → `wrap` → `wbuf`。难点：`unwrap` 可能需更多输入（`BUFFER_UNDERFLOW`）、握手期间读写交替（`NEED_WRAP/NEED_UNWRAP/NEED_TASK`）。本结构（环 + 中转缓冲区 + I/O 线程）正是放它的位置：字节流和成帧之间多一层有状态转换。

---

## 8. 常见误区

1. **以为一次 `read` = 一条消息**。→ 长度前缀 + 增量解码器；验证时在每个切分点切开。
2. **忽略 `write` 返回值 / 写一部分就当写完**。→ 慢网络、大消息时偶发丢数据。→ 保留 `wbuf` 与位置，等 `OP_WRITE`。
3. **`OP_WRITE` 一直开着**。→ CPU 100%。→ 只在有数据要写时开。
4. **入站不限界 / 满了还读**。→ OOM。→ 入站环 + 满了关 `OP_READ`。
5. **暂停读之后没人叫醒**。→ 通道偶发永久卡住。→ `poll` 腾出空间后 `wakeup`（阻塞版和自旋版都要验证）。
6. **忘了 `selectedKeys` 的语义**：不清除 / 读旧 `readyOps`。→ `if (selectedKeys().remove(key))`。
7. **容量刚好小于最大帧 + 头**。→ 死锁。→ 构造器校验 `>= maxFrame + 4`。
8. **长度字段不校验**。→ 恶意 4 字节让你分配 2 GB。→ 看到头就校验，粘性失败。
9. **EOF 一律当正常结束**。→ 吞掉半条消息。→ `hasTruncatedTail()` ⟹ `EOFException`。
10. **关闭时不管接收缓冲区里的数据**。→ 内核发 RST，对端丢掉未读数据。→ `shutdownOutput` → 等对端 EOF → `close`。
11. **用 `Thread.sleep(100)` 判断"应该已经到了"**。→ 慢机器偶发失败。→ 带截止时间的轮询。
12. **重连后假设消息不丢**。→ 见 Q4。

---

## 9. 自测题

**Q1（概念）**：为何"`read` 返回 5 字节"说明不了什么？给出同一个 13 字节流的三种合法划分。

<details><summary>答案</summary>

`read` 返回多少取决于内核已收到多少、缓冲区多大、调度时机。13 字节可以是 `13`、`5+6+2`、`1×13`、`4+9` 等任意划分。正确处理：全部喂给增量解码器，由它决定何时凑成一整帧。
</details>

**Q2（计算）**：`maxFrame = 100`，`inCapacity = 104`。对端发 3 条各 100 字节的消息（帧 104 字节），应用一直不 `poll`。入站环里最多多少字节？为何不死锁？`poll` 一条后会怎样？

<details><summary>答案</summary>

最多 104 字节（恰一条完整帧）。I/O 线程发现 `free() == 0` 不再监听 `OP_READ`，第二、三条留在内核 / 对端。不死锁因容量 ≥ `maxFrame + 4`：环里装得下一条完整帧，应用能 `poll` 走。`poll` 后 `readPaused` 为真 ⟹ `wakeup`，I/O 线程重算兴趣集、重开 `OP_READ`，读第二条。
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

①没有 `selectedKeys().clear()`（或迭代器 `remove`）：key 一旦被选中会一直留在集合里，下一轮即使没就绪也被处理（读旧 `readyOps`）；②没按状态更新兴趣集：`OP_WRITE` 一直开会忙等，从不开则写不出去；③没处理 `wakeup`——`offer` 之后无法叫醒 I/O 线程去写。
</details>

**Q4（设计）**：`ReconnectingClient.offer` 断线期间返回 `true`，随后进程崩溃，消息丢了。违反了什么契约？文档怎么诚实表达？怎么升级为"不丢"？

<details><summary>答案</summary>

`true` 只表示"进入了本进程的有界 pending 队列"，不是"对端收到"。文档要写清 at-most-once 尽力而为，崩溃/断开时已接受的消息可能丢，`abandonedBytes` 统计已知丢失量。升级：持久化发送队列 + 序号 + 对端确认 + 重传 + 去重，`true` 才能表示"已持久化"。
</details>

**Q5（小编程）**：给 `Backoff` 加"稳定连接 N 秒后才重置"（避免抖动连接一连上就重置造成重连风暴）。需改哪些地方？

<details><summary>答案</summary>

`run` 里连接成功时不立刻 `reset()`，记 `connectedAt`；`pump` 返回（断开）后若 `now - connectedAt >= stableAfter` 才 `reset()`，否则保留退避继续增长。`Backoff` 不变；需要可注入的时钟（`LongSupplier nanoTime`）才能确定性测试。
</details>

---

## 延伸阅读

* Stevens《UNIX Network Programming, Vol. 1》。
