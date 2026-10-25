# ld03 · 异步 TCP 消息通道（Asynchronous TCP Message Channel）（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲（TCP、`poll(2)`、背压、半关闭用到时现讲）。口头回答用英文，这里的英文术语可以直接拿去说。示例都跑在回环接口（127.0.0.1）上，反映软件和内核的开销，不是网线。

## 1. 题目

两个程序之间只有一条 TCP 连接。TCP 给你的是一根**可靠、有序的字节水管**，不是消息流：发两条各 10 字节的消息，对方可能一次读到 20 字节，也可能先读到 13 字节、再读到 7 字节（切在消息中间）；`send` 在发送缓冲区快满时只写进去一部分（部分写，partial write）；对方读得慢，内核缓冲区装满，TCP 窗口缩到 0，你的 `send` 写不进去；连接还会断。要在字节流上做一个**有界**的消息接口：`offer(消息)` 发、`poll()` 收，满了就说「满了」，既不无限堆内存，也不阻塞死。「满」要一路传回去——**背压**（backpressure）：从对方应用，穿过两端的内核，传回调用 `offer` 的人。

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `ByteRing`、`FrameCodec`、`FrameDecoder` | 纯内存：字节环形缓冲区；4 字节大端长度前缀成帧；增量解码器 | 回绕时分两段拷贝；`write_all` 全有或全无；非法帧头只看头就报错；解码器自己也有界（入站背压） |
| 2 | `TcpMessageChannel`、`MessageServer` | 一条连接上的有界通道：一个 `poll(2)` I/O 线程 + 出站环 + 入站解码器；部分读写；EOF；`finish_sending`（半关闭）；`close` | 兴趣集（events）每轮重算；唤醒 I/O 线程；EOF 落在帧中间；半关闭语义 |
| 3 | （同上，行为） | 背压与有界性 | 暂停读之后谁来恢复；容量恰好 `max_frame + 4` 不死锁 |
| 4 | `Backoff`、`ReconnectingClient` | 指数退避；断线自动重连；断线期间有界的 pending 队列 | 「已经交给旧连接的消息会丢」的诚实语义；退避重置；`close` 时停止重连 |

共同约定：

* **帧格式**：`[len: int32 大端][payload: len 字节]`；`len` 的合法范围 `[0, max_frame]`，空负载合法。
* `ChannelConfig(max_frame, out_capacity, in_capacity)`：字节数；`out_capacity`、`in_capacity` 必须 `>= max_frame + 4`（否则一条最大的消息永远凑不齐 / 放不进），构造函数校验，违反抛 `std::invalid_argument`。
* 所有测试在 `127.0.0.1` 加内核分配的临时端口上跑。**正确性不能靠 `sleep` 的时序**；只允许用带截止时间的轮询等待「最终会发生」的事件。
* `offer` 返回前已经把字节拷进出站环；之后调用方修改自己的缓冲区不影响已发送的内容。
* 错误类型（接口的一部分）：`FrameException`（帧协议错误）、`StateError`（通道已关闭 / 已 `finish_sending`，对应 Java 的 `IllegalStateException`）、`EofError`（对端在帧中间关闭，对应 `EOFException`）、系统调用失败是 `std::system_error`（带 `errno`）。

## 2. Part 1：字节环、成帧、增量解码

### 2.1 `ByteRing`

和 ld01 的环不同：这个环**单线程**（调用方加锁），容量是**任意正整数**（不要求 2 的幂，下标用 `%`），只关心两件事：部分读写，和数据绕过数组末尾时拆成两段拷贝。

```cpp
std::size_t write(std::span<const std::uint8_t> src) {
    const std::size_t n = std::min(src.size(), free());          // 能写多少写多少
    const std::size_t tail = (head_ + size_) % buf_.size();
    const std::size_t first = std::min(n, buf_.size() - tail);   // 到数组末尾为止的第一段
    if (first != 0) std::memcpy(buf_.data() + tail, src.data(), first);
    if (n > first)  std::memcpy(buf_.data(), src.data() + first, n - first);   // 绕回开头的第二段
    size_ += n;
    return n;                                                     // 调用方自己把游标前进 n
}
```

* **返回写入的字节数**，调用方自己前进游标。Java 的 `ByteBuffer` 自带 `position`，调用后自动前进；C++ 的 `std::span` 只是一个视图，没有游标，所以接口返回数量，调用方用 `src.subspan(n)` 前进。
* `write_all` **全有或全无**：放不下就一个字节都不写。编码一帧时先写头再写负载，如果头写进去而负载放不下，环里就多了半个头，之后解码出的全是垃圾，所以 `encode` 先检查 `free() >= 4 + len`，再写。
* `peek_int(offset)`：大端读 `int32` 且**不消费**，下标取模处理回绕；返回有符号数（`0xFFFFFFFF` 是 `-1`）。
* `take(n)` / `skip(n)`：不足时抛 `StateError`，状态不变。

**先检查，后分配**。Java 的 `take(int n)` 先判 `n < 0`；C++ 用 `std::size_t`，负数不存在，但 `static_cast<std::size_t>(-1)` 是 `2^64 - 1`。如果写成

```cpp
Bytes take(std::size_t n) {
    Bytes out(n);              // 先分配 ⇒ n 巨大时 std::bad_alloc / std::length_error
    if (n > size_) throw StateError(...);
```

抛出的就是错误的异常类型（或者内存耗尽）。把 `require(n)` 放在 `Bytes out(n)` 之前。同样，`peek_int` 里 `offset + 4` 在 `offset` 接近 `SIZE_MAX` 时回绕成小数，要写成 `offset > size_ - 4`（先确认 `size_ >= 4`）。

### 2.2 `FrameCodec` 与 `FrameDecoder`

```cpp
static bool encode(ByteRing& out, std::span<const std::uint8_t> payload, int max_frame) {
    if (payload.size() > static_cast<std::size_t>(max_frame)) throw std::invalid_argument(...);   // 永远发不出去 ≠ 暂时满
    if (out.free() < HEADER + payload.size()) return false;                                       // 暂时满：不留半个头
    const auto n = static_cast<std::uint32_t>(payload.size());
    const std::uint8_t header[4] = {uint8_t(n >> 24), uint8_t(n >> 16), uint8_t(n >> 8), uint8_t(n)};
    out.write_all(header);  out.write_all(payload);
    return true;
}
```

解码器是增量的：字节可以按任意块到达（1 字节、半个头、两条半消息），`next()` 只在凑齐一整帧时返回：

```cpp
std::optional<Bytes> next() {
    if (failed_) throw *failed_;                                   // 粘性失败
    if (ring_.size() < HEADER) return std::nullopt;
    const std::int32_t len = ring_.peek_int();
    if (len < 0 || len > max_frame_) { failed_ = FrameException(...); throw *failed_; }   // 只看头就报错
    if (ring_.size() < HEADER + std::size_t(len)) return std::nullopt;
    ring_.skip(HEADER);
    return ring_.take(len);
}
```

* **非法帧头只看到 4 字节头就必须报错**：不能等 `len` 个字节凑齐（`2^31 - 1` 永远凑不齐，还会诱导你分配 2 GB）。报错后**粘性失败**：流已经失去同步，没有「跳过这一帧继续」。
* `feed` 是有界的：环里放不下的字节**不消费**，调用方要先 `next()` 腾空间再继续喂——这是入站背压在最低层的体现。
* `has_truncated_tail()`：完整的帧之后是不是还有一截不完整的尾巴？对端关闭时靠它判断流是不是被截断。非法头由 `next()` 报告，不算截断。
* `std::optional<Bytes>`：`nullopt` = 不够一帧；「持有空 vector」= 一条空消息。

## 3. Part 2：`TcpMessageChannel`

### 3.1 结构

```
 app thread       I/O thread
 offer ->[out ring]-> wbuf -> send()
 poll  <-[in ring] <- rbuf <- recv()
```

左边是应用线程，右边是 I/O 线程（一个 `poll(2)` 循环）。`offer` 把消息编码进出站环（`out ring`），I/O 线程把它搬到中转缓冲区 `wbuf` 再 `send`；反方向 `recv` 进 `rbuf`，喂给入站解码器（`in ring`），`poll` 从里面取整帧。

* **一个 I/O 线程**，所有系统调用（`recv`、`send`、`poll`）都在它里面，**不持有锁**。应用线程只碰两个有界缓冲区，持锁时间只够拷贝内存。
* **一把 `std::mutex` + 一个 `std::condition_variable`**。条件变量 `changed_` 通知所有等待者：入站环有新消息了、出站环腾出空间了、状态变成 Closed 了。
* **POSIX 的 `poll(2)`**，不是 `epoll` / `kqueue`：`poll` 在 Linux 和 macOS 上都有，一次监听少量描述符完全够用。`epoll`（Linux）/ `kqueue`（macOS、BSD）的优势在监听**成千上万个**连接时才显现。

### 3.2 唤醒 I/O 线程：自管道

I/O 线程阻塞在 `poll()` 里。应用线程 `offer` 了一条消息、`poll` 腾出了入站空间、`close` 了——这些都需要把它叫醒。办法是**自管道**（self-pipe trick）：建一个 `pipe`，I/O 线程的 `poll` 同时监听管道的读端；别的线程往写端写一个字节，`poll` 就返回。Java 的 `Selector.wakeup()` 做的是同一件事。

```cpp
struct WakePipe {
    UniqueFd read_end, write_end;                 // 两端都非阻塞
    void wake() const { const char b = 1; (void)::write(write_end.get(), &b, 1); }   // 管道满了(EAGAIN)也无所谓
    void drain() const { char buf[64]; while (::read(read_end.get(), buf, sizeof buf) > 0) {} }
};
```

用管道而不是 `eventfd`，是因为 macOS 没有 `eventfd`。唤醒是**水平触发、不会丢**的：即使 `wake()` 发生在 I/O 线程刚算完兴趣集、还没进入 `poll` 的缝隙里，字节已经躺在管道里，`poll` 立刻返回——所以「先改状态、后唤醒」不存在丢失唤醒（lost wake-up）的问题。

### 3.3 I/O 循环：每一轮重新计算兴趣集

```cpp
for (;;) {
    short events = 0;
    {   std::lock_guard lk(m_);
        if (state_ == Closed) break;
        if (state_ == Finishing && !fin_sent_ && out_.is_empty() && wpos_ == wlen_) { ::shutdown(fd, SHUT_WR); fin_sent_ = true; }
        if (fin_sent_ && peer_closed_) { state_ = Closed; break; }
        read_paused_ = !peer_closed_ && in_.free() == 0;
        if (!peer_closed_ && in_.free() > 0)                events |= POLLIN;    // 入站环有空位才读
        if (!fin_sent_ && (wpos_ < wlen_ || !out_.is_empty())) events |= POLLOUT;   // 有数据要写才关心「可写」
    }
    pollfd fds[2] = {{wake_fd, POLLIN, 0}, {sock_fd, events, 0}};
    ::poll(fds, events != 0 ? 2 : 1, -1);        // events == 0：连 socket 都不放进去
    if (fds[0].revents) wake_.drain();
    const short rev = events != 0 ? fds[1].revents : 0;
    if ((events & POLLIN)  && (rev & (POLLIN  | POLLHUP | POLLERR))) do_read();
    if ((events & POLLOUT) && (rev & (POLLOUT | POLLHUP | POLLERR))) do_write();
}
```

* **兴趣集每轮重算**，由当前状态决定。没数据要写时**不要**要求 `POLLOUT`：空的发送缓冲区永远「可写」，`poll` 会立刻返回，循环空转吃满一个核。
* **`events == 0` 时不把 socket 放进 `poll`**：对端关闭后系统会持续报告 `POLLHUP`（macOS 上对端关闭后 `poll` 返回 `POLLIN|POLLHUP`，而且每次都是），哪怕你没有要求。如果此时还把 socket 交给 `poll`，循环就空转了。
* **就绪不等于完成**：`POLLIN` 只是说「现在 `recv` 不会阻塞」，读到多少、是不是一整条消息，都另说。
* 暂停读：入站环满了 ⇒ 不要求 `POLLIN`，不再从内核取数据 ⇒ 内核接收缓冲区满 ⇒ TCP 窗口为 0 ⇒ 对端 `send` 写不出去。

### 3.4 部分读写

```cpp
void do_write() {
    for (int round = 0; round < 16; ++round) {          // 限制一轮最多写多少，别饿死读
        const std::uint8_t* from; std::size_t count;
        {   std::lock_guard lk(m_);
            if (wpos_ == wlen_) {                        // wbuf 空了 ⇒ 从出站环再装一批
                wlen_ = out_.read(wbuf_);  wpos_ = 0;
                changed_.notify_all();                   // 出站环腾出了空间：叫醒 offer(msg, timeout)
                if (wlen_ == 0) return;
            }
            from = wbuf_.data() + wpos_;  count = wlen_ - wpos_;
        }
        const ssize_t n = ::send(fd, from, count, kSendFlags);          // 锁外
        if (n < 0) { if (errno == EAGAIN || errno == EWOULDBLOCK) return; if (errno == EINTR) continue; throw_errno("send"); }
        { std::lock_guard lk(m_); wpos_ += n; }          // 没写完的留在 wbuf_，等下一次 POLLOUT
    }
}
```

* `send` 返回的 `n` 可能小于 `count`：**剩余部分和位置必须保留**（`wbuf_` 加 `wpos_` / `wlen_`），下一次 `POLLOUT` 继续。出站环是 `ByteRing`，数据先经一个 16 KiB 的中转缓冲区进入 socket。
* `wpos_` / `wlen_` 要在锁里读写，因为 `unsent_bytes()` 从别的线程读它们；C++ 里「大家都知道只有 I/O 线程改它」不算同步，TSan 会报数据竞争。
* `EAGAIN` / `EWOULDBLOCK`（内核缓冲区满）不是错误，是背压的开始。`EINTR` 是信号打断，重试。

读端同理：`recv` 的上限是 `min(rbuf 大小, 入站环的空位)`，读到的字节 `feed` 给解码器——空位够，所以一定吃得下。`recv` 返回 0 是 EOF。

### 3.5 EOF、半关闭、关闭

* **EOF（对端关闭）≠ 本端关闭**：`recv() == 0` ⇒ `peer_closed_ = true`。之后仍可 `poll` 剩余的完整消息，仍可 `offer`（**半关闭**，half-close）。`is_drained()` = 不会再有新消息且缓冲区里没有完整消息。
* **EOF 恰好落在一帧中间** ⇒ 流被截断：`failure()` 是 `EofError`，通道关闭，但之前收齐的完整帧仍可取。
* `finish_sending()`：之后 `offer` 抛 `StateError`；已接受的消息刷完后 `shutdown(SHUT_WR)`（发 FIN，对端的 `recv` 返回 0）；当本端已发 FIN **且**对端也关闭，通道自动关闭，`failure()` 为空。
* `close()`：立刻关闭，未发送的数据丢弃，唤醒所有阻塞的 `poll(timeout)` / `offer(msg, timeout)` / `await_closed`。幂等。
* I/O 线程退出时 `fd_.reset()`：对端要在通道**关闭**时就看到 EOF，不是等这个对象被销毁。

### 3.6 RAII：谁拥有什么

| 资源 | 谁拥有 | 怎么释放 |
|---|---|---|
| socket 描述符 | `UniqueFd`（移动专用的 RAII 类） | 析构 `close(fd)`；`wrap(UniqueFd, cfg)` 接管，抛异常时自动关闭 |
| 管道的两端 | `WakePipe` 里的两个 `UniqueFd` | 同上 |
| I/O 线程 | `std::jthread` 成员 | `close()` 里 `join`；析构函数先调 `close()` |
| 通道对象 | `std::unique_ptr<TcpMessageChannel>`（`connect` / `wrap` / `accept` 都返回它） | 离开作用域 ⇒ 析构 ⇒ `close()` |

关键约定：**线程必须先于它用到的成员销毁**。`io_thread_` 声明在所有成员的最后，析构函数体先调 `close()`（置 `Closed`、唤醒线程、`join`），成员才开始销毁——不然线程还在用 `mutex` 和 `ByteRing` 时它们已经没了。`close()` 里的 `join` 用 `std::call_once` 保护：两个线程同时 `close()`，第二个等第一个 `join` 完，而不是对同一个线程 `join` 两次（UB）。

通道**不可拷贝、不可移动**（有线程、互斥量、socket，线程里捕获了 `this`），所以到处是 `unique_ptr`。`static_assert(!std::is_move_constructible_v<TcpMessageChannel>)` 固定了这一点。

### 3.7 `failure()` 是 `std::exception_ptr`

Java 的 `failure()` 返回 `Throwable`。C++ 里异常不是对象，不能随手存起来；`std::exception_ptr` 是「一个被捕获的异常」的句柄，可以拷贝、跨线程传递：

```cpp
catch (...) { std::lock_guard lk(m_); fail_locked(std::current_exception()); }   // I/O 线程里捕获
// 另一个线程里检查类型：
try { std::rethrow_exception(ch.failure()); } catch (const EofError&) { /* 对端在帧中间关闭 */ }
```

### 3.8 SIGPIPE

对一个已经被对端重置（RST）的连接 `send`，内核向你的进程发 `SIGPIPE`，默认动作是**终止整个进程**。库代码不该这样。Linux 用 `send(fd, ..., MSG_NOSIGNAL)`；macOS 没有 `MSG_NOSIGNAL`，对 socket 设 `SO_NOSIGPIPE`。之后 `send` 返回 `-1` / `EPIPE`，通道失败（`failure()` 是 `std::system_error`）。测试里让对端用 `SO_LINGER{1, 0}` 关闭（发 RST）再持续 `offer`——进程活着走到最后就是断言。

### 3.9 `offer` 与 `poll` 的锁规则

```cpp
bool offer(std::span<const std::uint8_t> msg) {
    bool was_empty;
    {   std::lock_guard lk(m_);
        require_sendable();                                    // 已关闭 / 已 finish_sending ⇒ StateError
        was_empty = out_.is_empty();
        if (!FrameCodec::encode(out_, msg, cfg_.max_frame())) return false;
    }
    if (was_empty) wake_.wake();      // 出站环原来非空，I/O 线程已经在等 POLLOUT，不必再唤醒
    return true;
}
std::optional<Bytes> poll() {
    std::optional<Bytes> m;  bool wake = false;
    {   std::lock_guard lk(m_);
        m = next_locked();                                     // 坏帧头 ⇒ 通道失败并重新抛出 FrameException
        if (m && read_paused_) { read_paused_ = false; wake = true; }
    }
    if (wake) wake_.wake();           // 入站环原来满了、读被暂停：腾出空间后必须叫醒，否则永远不再读
    return m;
}
```

* **`poll` 要唤醒 I/O 线程**：它暂停读是因为入站环满，只有应用线程 `poll` 才能腾出空间，所以腾空间的人负责叫醒。非阻塞的 `poll()`（自旋调用）和带超时的 `poll(timeout)` 都要这样做，测试专门用一个自旋的 `poll()` 去验证。
* 系统调用（`wake()` 里的 `write`）放在锁外。
* `offer(msg, timeout)` / `poll(timeout)`：`condition_variable::wait_until(lock, deadline)` 加循环重查条件（防伪唤醒）。

## 4. Part 3：背压与有界性

**出站**：对端不读 ⇒ 内核发送缓冲区满 ⇒ `send` 返回 `EAGAIN` ⇒ 出站环渐满 ⇒ `offer` 返回 `false`。**接受过的每一条消息，在对端开始读之后必须按序、不丢、不重地到达**。

**入站**：应用不 `poll` ⇒ 入站环满 ⇒ I/O 线程不再要求 `POLLIN` ⇒ 内核接收缓冲区满 ⇒ TCP 窗口为 0 ⇒ 对端 `send` 写不出去。

**有界性**：出站环 + 内核缓冲区 + 入站环之外，没有任何随消息数增长的内存。

**最小缓冲区**：`in_capacity = out_capacity = max_frame + 4` 时仍然必须工作（2 万条随机长度的消息，每条都在环的回绕边界上被切开，入站环几乎一直是满的）——最容易暴露「暂停读之后没人恢复」。

测试里把内核缓冲区压到 4 KiB（`SO_SNDBUF` / `SO_RCVBUF`）让「内核缓冲区满」在几十 KB 内发生，这样不需要发送几百 MB 才看到背压。

行情（可以丢）和订单（不能丢）的策略不同：行情满了丢旧的、保新的（conflation）；订单满了必须告诉上游，让上游减速或失败。

## 5. Part 4：重连

### 5.1 `Backoff`

```cpp
long long next() {
    const long long d = current_;
    current_ = current_ > max_ / multiplier_ ? max_ : std::min(max_, current_ * multiplier_);   // 先除后乘：不溢出
    return d;
}
template <std::uniform_random_bit_generator G> long long next(G& rng) {     // 全抖动
    const long long cap = next();
    return std::uniform_int_distribution<long long>(0, cap)(rng);            // [0, cap]，含两端
}
```

* `100, 200, 400, 800, 1000, 1000 …`：指数增长，封顶。**比较 `current_ > max_ / multiplier_` 而不是先乘再比**：先乘会溢出（有符号溢出是 UB），上限设成 `LLONG_MAX` 时尤其会。
* **全抖动**（full jitter）：在 `[0, 当前上限]` 内均匀取值，避免大量客户端在同一时刻重连造成惊群（thundering herd）。随机数引擎由调用方传入（`std::uniform_random_bit_generator` 概念），测试可以固定种子。Java 的 `rng.nextLong(cap + 1)` 在 `cap == Long.MAX_VALUE` 时 `cap + 1` 溢出；`uniform_int_distribution<long long>(0, cap)` 的上界本来就是闭区间，没有这个问题。

### 5.2 `ReconnectingClient`

```
 offer -> [pending] -> manager thread
          -> current channel -> network
 on failure: back off, reconnect
```

`offer` 先进有界的 `pending` 队列，管理线程把它搬进当前通道；连接失败或对端关闭时退避后重连，`pending` 里的消息留着。

后台一个管理线程（`std::jthread`）：连接 ⇒ 成功后把 `pending` 里的消息按序搬进当前通道 ⇒ 通道断开（`!is_open()` 或 `is_peer_closed()`）⇒ 丢掉旧通道 ⇒ 退避后重连。连接成功后 `backoff.reset()`，这样下一次断线从最短的等待开始。

* `offer` **永远先进 `pending`**（保证顺序），`pending` 有界：已编码字节（`4 + len` 之和）不得超过 `out_capacity`，放不下返回 `false`。断线期间 `offer` 仍然成功，直到装满。
* **诚实的语义**：已经交给旧通道（进了它的出站环 / 内核缓冲区）的消息，连接断掉时**可能丢失**。TCP 只保证连接存续期间的有序不丢，不保证对端应用处理了。要不丢，必须有应用层序号 + 确认 + 重传（至少一次，at-least-once，再加去重得到 effectively-once）。这个类是 at-most-once 的尽力而为，丢失字节数累计在 `abandoned_bytes()`。
* `poll()`：当前连接上的入站消息；断线期间 `nullopt`。**`current_` 是 `std::shared_ptr`**：应用线程在锁里拷贝一份指针，锁外去 `poll`；如果管理线程这时丢弃了旧通道，应用线程手里的拷贝保证它还活着，最后一个持有者析构。若是裸指针或 `unique_ptr` 引用，就是 use-after-free。
* `close()`：关闭当前通道、唤醒管理线程（睡眠退避是 `condition_variable::wait_for(..., [&]{ return closed_; })`，可以被打断）、之后不再重连、`offer` 抛 `StateError`、幂等。析构函数也调 `close()`，所以管理线程不会泄漏。

## 6. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| `Selector` + `SelectionKey.interestOps` | `poll(2)` + 每轮重算的 `events` | 同一件事：「等待一批描述符就绪」；`poll` 更简单，规模大了换 `epoll` / `kqueue` |
| `selector.wakeup()` | 自管道（`pipe` + 非阻塞读写端） | 没有现成的唤醒，管道可移植 |
| `ByteBuffer`（带 position / limit，要 `flip()`） | `std::span` + 返回字节数 | span 是无状态的视图，游标由调用方管理 |
| `ReentrantLock` + `Condition` | `std::mutex` + `std::condition_variable` | 对应物；等待要循环重查条件 |
| `Throwable failure()` | `std::exception_ptr` | 异常不是对象，用句柄存起来 |
| `IOException` | `std::system_error`（带 `errno`） | 系统调用失败的统一类型 |
| `EOFException` / `IllegalStateException` / `IllegalArgumentException` | `EofError` / `StateError` / `std::invalid_argument` | 标准库没有同名异常 |
| try-with-resources 关闭 socket、`Selector` | `UniqueFd` 析构；线程用 `std::jthread` | 异常安全靠对象生命周期 |
| 守护线程，`close()` 里 `join(2_000)` | `std::jthread` + `call_once` 的 `join` | C++ 线程对象销毁时还没 `join` 会 `std::terminate`；多个线程同时关闭要只 `join` 一次 |
| 垃圾回收保证对象还活着 | `std::shared_ptr` 持有当前通道 | 没有 GC，跨线程共享的对象要明确所有权 |
| 向 `SIGPIPE` 无感（JVM 忽略） | `MSG_NOSIGNAL` / `SO_NOSIGPIPE` | 默认会终止进程 |
| 虚拟线程 + 阻塞 I/O 的备选方案 | 没有对应物；备选是每连接一线程或协程 | C++20 有协程语言特性但没有标准的调度器 |
| `int` 长度，负数天然存在 | 无符号 `size_t` 要防止 `-1` 变成 `2^64-1` | 无符号让「负数」变成「巨大」，检查要在分配之前 |

## 7. 陷阱

1. **把 TCP 当消息流**：一次 `recv` 就是一条消息（2.1）。
2. **部分写后丢了剩余**：`send` 只写了一部分，其余没保留位置（3.4）。
3. **一直要求 `POLLOUT`**：没数据要写时 `poll` 立刻返回，循环空转（3.3）。
4. **暂停读之后没人恢复**：`poll()` 腾了空间却没叫醒 I/O 线程（3.9）。
5. **非法帧头等 `len` 个字节凑齐才报错**：永远等不到（2.2）。
6. **`encode` 先写头再检查空间**：环里留下半个头（2.2）。
7. **`take(n)` 先分配后检查**：`n` 巨大时抛了错误的异常（2.1）。
8. **在锁里做系统调用**：`send` / `recv` 阻塞时所有应用线程被卡住（3.4）。
9. **`wpos_` / `wlen_` 无锁读写**：数据竞争（3.4）。
10. **线程比成员活得长**：析构顺序错误，线程还在用已销毁的 `mutex`（3.6）。
11. **两个线程同时 `close()` 都 `join`**：对同一线程 `join` 两次（3.6）。
12. **忘记 `SIGPIPE`**：对端重置后第一次 `send` 杀死整个进程（3.8）。
13. **`ReconnectingClient::poll` 用裸指针**：管理线程丢弃旧通道时 use-after-free（5.2）。
14. **退避先乘后比**：上限很大时溢出（5.1）。
15. **重连后声称不丢消息**：已交给旧连接的消息可能丢（5.2）。
16. **用 `sleep` 判断正确性**：测试用带截止时间的轮询（1）。

## 8. 面试官会追问什么（senior）

**Q1. 为什么一个 I/O 线程，而不是一个连接一个线程？** 每个线程都有自己的栈和上下文切换的开销；一个线程监听上万个连接时，真正的成本是系统调用而不是线程。这个类每连接一个线程只是为了讲清楚结构；服务端会用一个事件循环管 N 个连接。

**Q2. `poll` 与 `epoll` / `kqueue`？** `poll` 每次调用把整个描述符数组交给内核，O(n)；`epoll` / `kqueue` 把兴趣集登记在内核里，返回就绪的那些，O(就绪数)。少量连接时没区别。

**Q3. 边缘触发和水平触发？** 水平触发（level-triggered，`poll` 和 `epoll` 默认）：只要还有数据没读完，每次都会报告就绪。边缘触发（edge-triggered，`EPOLLET`）：只在状态**变化**时报告一次，必须一直读到 `EAGAIN`，否则剩下的数据不会再有通知。这个类用水平触发：暂停读靠「不要求 `POLLIN`」，恢复靠重新要求。边缘触发要自己记住「还有数据没读」。

**Q4. 对端掉电了（没有 FIN、没有 RST），怎么知道？** 不会知道——TCP 在没有数据流动时不会探测。需要应用层心跳 + 空闲超时，或者开 TCP keepalive（`SO_KEEPALIVE`，默认间隔很长，可调）。

**Q5. 重连之后消息不丢吗？** 会丢。要不丢：每条消息带序号，对端周期性确认已收到的最大序号；重连后从对端的确认点重发；对端按序号去重。这样是 at-least-once 加去重。

**Q6. Nagle 和 `TCP_NODELAY`？** Nagle 算法把小包攒起来一起发以省带宽，代价是延迟（等上一个包的 ACK）。低延迟场景用 `TCP_NODELAY` 关掉；代价是小包多、头部开销大。需要时在应用层批量发送（一次 `send` 多条消息）。

**Q7. 应用一直不调用 `poll()` 会怎样？** 入站环满，I/O 线程停止读，内核缓冲区满，对端的 `send` 阻塞或返回 `EAGAIN`——慢消费者拖慢生产者，这是**设计上期望的**行为。如果不能容忍（行情），在上层丢旧的。

**Q8. 为什么容量必须 ≥ `max_frame + 4`？** 一条最大的消息连头带负载占 `max_frame + 4` 字节；入站环比它小，解码器永远凑不齐这一帧，读又被暂停，死锁；出站环比它小，这条消息永远放不进去。

**Q9. TLS 怎么接进来？** 在 `recv` / `send` 和环之间多一层：密文 ⇒ TLS 库解密 ⇒ 明文喂给 `FrameDecoder`。关键难点：TLS 库的读操作可能需要先**写**（握手、重协商），写操作可能需要先**读**，所以兴趣集不再只由「环有没有空位」决定。

**Q10. 零拷贝？** `sendfile` / `splice`；`MSG_ZEROCOPY`；用户态把消息直接编码进出站环，避免中间 `std::vector`；入站用 `readv` 直接收进环的两段。

**Q11. `std::jthread` 相对 `std::thread` 好在哪里？** 析构时自动 `join`（`std::thread` 没 `join` 就析构会 `std::terminate`），并且带 `std::stop_token` 协作式取消。这里没有用 `stop_token`（线程阻塞在 `poll`，需要自管道唤醒），但自动 `join` 已经避免了最常见的错误。

## 9. 自测

1. 发 `"AB"` 和 `"CDE"` 两条消息，线上是哪 13 个字节？
2. `FrameDecoder` 收到 `00 00 00 0B`，`max_frame = 10`，`next()` 做什么？为什么不等 11 字节？
3. 为什么 `ByteRing::write` 返回字节数，而不是像 Java 的 `ByteBuffer` 那样自己前进游标？
4. 为什么没数据要写时不能要求 `POLLOUT`？
5. 入站环满了，I/O 线程停止监听 `POLLIN`。谁、在什么时候让它恢复？
6. `recv()` 返回 0 之后，通道还能 `offer` 吗？还能 `poll` 吗？
7. 对端在一帧的中间关闭，`failure()` 是什么？之前收齐的完整帧呢？
8. 为什么 `TcpMessageChannel` 的 `io_thread_` 要声明在所有成员的最后？
9. 为什么要对 socket 设 `MSG_NOSIGNAL` / `SO_NOSIGPIPE`？
10. `ReconnectingClient::poll` 为什么要把 `current_` 拷贝成 `shared_ptr` 再在锁外使用？
11. `Backoff(1, LLONG_MAX, 10)` 的 `next()` 为什么不会溢出？

<details><summary>答案</summary>

1. `00 00 00 02 41 42 00 00 00 03 43 44 45`（4 字节大端长度 + 内容，两条共 6 + 7 = 13 字节）。
2. 头里的长度 11 > `max_frame` = 10，立刻抛 `FrameException`，且之后每次 `next()` 都抛（粘性）。不等 11 字节：非法长度可能是 `2^31 - 1`，永远凑不齐。
3. `std::span` 是无状态的视图，不能被调用后"前进"；返回数量，由调用方用 `subspan(n)` 前进。这样接口也没有隐藏的副作用。
4. 空的发送缓冲区永远可写，`poll` 立刻返回，循环空转。兴趣集每轮根据「有没有数据要写」重算。
5. 应用线程：`poll()` / `poll(timeout)` 取走一条消息后，如果 `read_paused_` 为真就清除并 `wake()` 自管道；I/O 线程被叫醒，重新计算兴趣集，入站环有空位，重新要求 `POLLIN`。
6. 都可以：EOF 只说明对端不再发送（半关闭）；本端仍可发送，也仍可取走已缓冲的完整消息。
7. `EofError`，通道关闭；之前收齐的完整帧仍可 `poll` 取出。
8. 析构时成员按声明的**逆序**销毁：线程声明在最后，最先被销毁（`join`），这时 `mutex`、`ByteRing` 等还活着。反过来线程可能在它们销毁之后还在使用。
9. 对已被对端重置的连接 `send`，内核发 `SIGPIPE`，默认动作终止整个进程；设了之后 `send` 返回 `EPIPE`，通道正常失败。
10. 管理线程可能在应用线程使用旧通道时丢弃它；拷贝的 `shared_ptr` 保证通道对象在应用线程用完之前不会被销毁。在锁外调用 `poll` 是因为它可能阻塞（拿通道自己的锁）。
11. 先判断 `current_ > max_ / multiplier_`：成立就直接取 `max_`，不做乘法；不成立时 `current_ * multiplier_ <= max_`，也不会溢出。

</details>

## 延伸阅读

* [poll(2)](https://man7.org/linux/man-pages/man2/poll.2.html)：事件集、`POLLHUP` 与 `POLLERR` 的含义
* [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)：套接字 API 入门
* [std::exception_ptr](https://en.cppreference.com/w/cpp/error/exception_ptr)：跨线程传递异常
* [The C10K problem](http://www.kegel.com/c10k.html)：为什么需要事件循环
* [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)：全抖动
