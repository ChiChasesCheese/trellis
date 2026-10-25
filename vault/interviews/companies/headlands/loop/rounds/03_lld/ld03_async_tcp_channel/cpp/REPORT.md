# ld03 · 思路与追问（C++20 版）

这是一道设计加并发的题：代码量不小，但面试官真正在听的是你的设计决定——谁拥有什么、哪个线程做什么、消息边界怎么找、满了怎么办、怎么干净地关掉。下面按 Part 写四件事：怎么写、面试官在探什么（包括所有权、线程、成帧、背压、关闭这几类设计问题）、该说出口的那句话，以及 C++ 特有的坑。详细的推导、完整的 I/O 循环和自测题在讲义 [[ld03_async_tcp_channel_cpp]]。

## 30 秒版本

- **字节流不是消息流**：消息边界自己带，用 `[len:int32 大端][payload]`；`recv` 和 `send` 的部分完成是常态，不是异常。
- **线程模型**：一个 I/O 线程跑 `poll(2)` 循环，所有系统调用都在它里面、不持锁；应用线程只在一把互斥量下碰出站环和入站解码器。
- **有界**：出站环、内核缓冲区、入站环各有上限；满了 `offer` 返回 `false`，入站环满了就不再要求 `POLLIN`，窗口一路压回对端。
- **唤醒纪律**：谁腾出空间谁负责叫醒 I/O 线程（`poll` 腾入站空间，I/O 线程自己腾出站空间并通知 `offer(msg, timeout)`），唤醒用自管道，不会丢。
- **关闭与所有权**：`UniqueFd` 管描述符，`std::jthread` 声明在最后、析构先 `close()`；EOF 不等于关闭，EOF 落在帧中间是 `EofError`。
- **重连是 at-most-once**：交给旧连接的字节可能丢，计入 `abandoned_bytes()`；要不丢必须有序号、确认、重传。

## Part 1 · 字节环、成帧、增量解码

**写法**：`ByteRing` 用 `std::vector<std::uint8_t>` 加 `head_` 和 `size_`，位置是 `(head_ + offset) % capacity`，所以容量不必是 2 的幂。`write` / `read` 在数组末尾回绕时拆成两次 `memcpy`；`write_all` 先比 `free()`，放不下就什么都不写。关键一步是在分配之前检查：

```cpp
Bytes take(std::size_t n) {
    if (n > size_) throw StateError("take: not enough bytes");   // 先查，再 Bytes out(n)
    ...
}
```

`encode` 先判断 `free() >= 4 + payload.size()`，够了才写头加负载，这样环里不会留下半个头。`FrameDecoder::next` 只做三件事：`size_ < 4` 返回 `nullopt`；`peek_int()` 取长度，`len < 0 || len > max_frame` 立刻抛 `FrameException` 并置粘性失败标志；`size_ < 4 + len` 返回 `nullopt`，否则 `skip(4)` 再 `take(len)`。

**面试官在探什么**

1. **成帧**：为什么用长度前缀而不是分隔符？负载是任意字节，分隔符要转义；长度前缀让接收方知道还差多少字节，代价是流一旦失去同步就无法恢复。
2. **非法头为什么只看 4 字节**：`len = 0x7FFFFFFF` 永远凑不齐 2 GiB，等它就是死锁；先分配再检查则是被对端一个坏头打爆内存。粘性失败是因为流已经错位，「跳过这一帧」没有意义，唯一的恢复是重连。
3. **有界的入站**：`feed` 只消费放得下的部分、返回消费数。这是背压在最底层的样子：调用方必须先 `next()` 腾空间。为什么返回字节数而不是自己前进游标？`std::span` 是无状态的视图，游标由调用方用 `subspan` 前进。
4. **容量下限 `max_frame + 4`**：入站环比一帧小，则半帧在环里、环又满，永远凑不齐；出站环比一帧小，最大的消息永远放不进。所以 `ChannelConfig` 和 `FrameDecoder` 的构造函数就拒绝非法值。
5. **C++ 专属**：`take(static_cast<std::size_t>(-1))` 是 `2^64 − 1`，先 `Bytes out(n)` 会抛 `std::bad_alloc` / `length_error` 而不是 `StateError`；`peek_int(offset)` 里 `offset + 4` 也会回绕，要写成 `size_ < 4 || offset > size_ - 4`：先确认 `size_ ≥ 4`，减法就不会回绕。`ByteRing` 里是 `std::vector`，拷贝就是独立的深拷贝，没有别名问题。

**该说出口的话**：「TCP 是字节流，我用 4 字节大端长度前缀成帧；非法长度看到头就拒绝，不等负载；解码器容量有界，`feed` 只吃放得下的部分，这就是入站背压的最底层。」

## Part 2 · `TcpMessageChannel`（一条连接）

**写法**：

```
 应用线程                      I/O 线程（poll(2) 循环）
 offer ──▶ [出站环] ──▶ wbuf ──▶ send()
 poll  ◀── [入站环] ◀── rbuf ◀── recv()
         一把 mutex + 一个 condition_variable
```

I/O 循环每一轮在锁里重算兴趣集：入站环有空位且对端没关，才要求 `POLLIN`；`wbuf` 里还有剩余或出站环不空，才要求 `POLLOUT`；两者都没有时 `poll` 只放唤醒管道，不放 socket。然后在锁外 `poll`，被叫醒就 `drain` 管道，就绪才调 `do_read` / `do_write`。`do_write` 每次从出站环装一批进 16 KiB 的 `wbuf`，`send` 写了多少就把 `wpos_` 前进多少，没写完的留着等下一次 `POLLOUT`。`do_read` 的 `recv` 上限取 `min(rbuf 大小, 入站环空位)`，所以 `feed` 一定吃得下。

**面试官在探什么**

1. **线程与锁**：为什么系统调用不能放在锁里？`send` / `recv` 虽然非阻塞，但锁里做系统调用会拉长临界区，应用线程的 `offer` / `poll` 被拖慢；更重要的是持锁等待 I/O 线程的设计很容易死锁。锁里只做内存拷贝。
2. **为什么不一直要求 `POLLOUT`**：空的发送缓冲区永远「可写」，`poll` 立刻返回，循环空转吃满一个核。兴趣集由当前状态决定，每轮重算。`events == 0` 时连 socket 都不放进去，因为对端关闭后系统会持续报告 `POLLHUP`，也会让循环空转。
3. **唤醒与丢失唤醒**：别的线程往管道写一个字节，哪怕发生在 I/O 线程算完兴趣集、还没进入 `poll` 的缝隙里，字节已经躺在管道里，`poll` 立刻返回，所以「先改状态、后唤醒」不会丢。为什么 `offer` 只在出站环从空变非空时才唤醒？环原来非空，I/O 线程已经在等 `POLLOUT`，再唤醒只是多一次系统调用。
4. **就绪不等于完成**：`POLLIN` 只说明现在 `recv` 不会阻塞，读到多少、是不是一整帧，都另说；`send` 返回的 `n` 可能小于请求，剩余部分和位置必须保留。`EAGAIN` 不是错误，是背压的开始；`EINTR` 重试。
5. **`wpos_` / `wlen_` 为什么要在锁里读写**：`unsent_bytes()` 从别的线程读它们，C++ 里「大家都知道只有 I/O 线程改它」不算同步，ThreadSanitizer（线程检测器）会报数据竞争。
6. **EOF 与关闭**：`recv() == 0` 只说明对端不再发送，本端仍可 `offer`，已缓冲的完整消息仍可 `poll`（半关闭）。EOF 落在帧中间（`has_truncated_tail()` 为真）时，`failure()` 是 `EofError`，通道关闭，但之前收齐的帧仍可取。`finish_sending()` 是刷完后 `shutdown(SHUT_WR)`；本端已发 FIN 且对端也 EOF，通道自动关闭，`failure()` 为空。`close()` 是立刻关、丢数据、唤醒所有等待者、幂等。
7. **所有权**：描述符归 `UniqueFd`，管道两端是 `WakePipe` 里的两个 `UniqueFd`，`wrap(UniqueFd, cfg)` 接管，中途抛异常也不会漏。线程是 `std::jthread` 成员，**声明在所有成员的最后**：成员按声明的逆序销毁，线程最先被 `join`，这时互斥量和环都还活着；析构函数体先调 `close()`（置 `Closed`、叫醒线程、`join`）。`close()` 里的 `join` 用 `std::call_once`，两个线程同时 `close()` 时不会对同一个线程 `join` 两次（UB）。通道不可拷贝、不可移动（有线程、互斥量，线程捕获了 `this`），所以到处是 `std::unique_ptr`。
8. **`failure()` 为什么是 `std::exception_ptr`**：异常不是对象，不能随手存起来；`exception_ptr` 是一个被捕获异常的句柄，可以拷贝、跨线程传递，调用方用 `std::rethrow_exception` 加 `catch` 判断类型。I/O 线程里的 `catch (...)` 用 `std::current_exception()` 存下来，不能让异常逃出线程函数，否则 `std::terminate`。
9. **`SIGPIPE`**：对已被重置的连接 `send`，内核发 `SIGPIPE`，默认动作杀掉整个进程。Linux 用 `MSG_NOSIGNAL`，macOS 对 socket 设 `SO_NOSIGPIPE`（`detail::kSendFlags` 已给）；之后 `send` 返回 `EPIPE`，通道失败，`failure()` 是 `std::system_error`。
10. **为什么不是多线程/每连接两个线程**：每个线程有栈和切换成本；这里一条连接一个 I/O 线程是为了讲清结构，服务端会用一个事件循环管 N 个连接，连接数很大时 `poll` 每次要把整个数组交给内核（O(n)），换 `epoll` / `kqueue`。

**该说出口的话**：「一个 I/O 线程做所有系统调用、不持锁；应用线程只在一把锁下碰两个有界缓冲区。兴趣集每轮根据状态重算，没数据要写就不要求 `POLLOUT`。线程声明在最后，析构先 `close()`，所以线程比它用到的成员先死。」

## Part 3 · 背压与有界性

**写法**：没有新类，是 Part 2 里几个标志的配合。`do_read` 之前，I/O 循环在锁里设 `read_paused_ = !peer_closed_ && in_.free() == 0`，为真就不要求 `POLLIN`。`poll()` 和 `poll(timeout)` 取走一条消息后，如果 `read_paused_` 为真就清掉它并 `wake_.wake()`（`wake` 在锁外调用）。出站方向，`do_write` 把环里的字节装进 `wbuf` 时对 `changed_` 做 `notify_all`，叫醒阻塞在 `offer(msg, timeout)` 里的线程。

**面试官在探什么**

1. **背压怎么穿过内核**：入站环满 ⟹ 不要求 `POLLIN` ⟹ 内核接收缓冲区满 ⟹ TCP 窗口为 0 ⟹ 对端 `send` 返回 `EAGAIN` ⟹ 对端出站环渐满 ⟹ 对端 `offer` 返回 `false`。每一层都有上限，没有一层在悄悄堆内存。
2. **暂停之后谁来恢复**：谁腾出入站空间，谁负责叫醒。`poll()`（非阻塞，自旋调用）和 `poll(timeout)` 都要这样做；漏掉前者，自旋消费者会在几条消息之后永远卡住。
3. **为什么最小容量 `max_frame + 4` 也不死锁**：每条消息都在环边界被切开，入站环几乎一直是满的，只要每次 `recv` 的上限是环的空位，满了就暂停、`poll` 腾出空间就恢复，数据总能前进。
4. **`offer` 返回 `false` 到底表示什么**：只表示「现在放不下」。I/O 线程可能还没来得及腾出空间，所以要判断真的堵死了，应该等一段时间（测试里是 200 ms）仍然放不下。不能把 `false` 当成永久失败。通道已不可用才是 `StateError`，两者必须区分。
5. **消费者不 `poll` 会怎样**：入站环满，对端被拖慢，这是设计意图。同一个线程既在等 `offer` 的空间、又不去 `poll`，而对端也这样，就会死锁。所以接口约定：收和发放在不同线程，或者用非阻塞的 `offer`。
6. **行情和订单的策略一样吗**：不一样。订单不能丢，满了就停止接收并报警（fail closed）；行情可以合并（conflation），只保留最新值。通道只负责报告「满了」，丢什么由业务决定。
7. **`TCP_NODELAY`**：必须开。应用层已经批量（出站环加一次 `send` 发多条），不需要 Nagle；开着 Nagle 再碰上延迟确认（delayed ACK），小消息会被拖慢。

**该说出口的话**：「每层都有上限，满了向上游说『满了』：入站环满就不要求 `POLLIN`，窗口压到 0，对端 `send` 写不出去，`offer` 返回 `false`。谁腾出空间谁叫醒 I/O 线程，否则暂停就变成永久卡死。」

## Part 4 · 退避与重连

**写法**：`Backoff::next` 先除后乘，不溢出：

```cpp
long long next() {
    const long long d = current_;
    current_ = current_ > max_ / multiplier_ ? max_ : std::min(max_, current_ * multiplier_);
    return d;
}
```

`next(rng)` 取 `next()` 的结果当上限，用 `std::uniform_int_distribution<long long>(0, cap)`，上界本来就是闭区间，所以 `cap == LLONG_MAX` 也不需要写 `cap + 1`。`ReconnectingClient` 的管理线程（`std::jthread`）：连接 ⟹ 成功就 `backoff.reset()`、把 pending 按序搬进当前通道 ⟹ 发现 `!is_open()` 或 `is_peer_closed()` ⟹ 把已交给旧通道的字节计入 `abandoned_bytes()`、丢掉旧通道 ⟹ 退避等待后重连。退避的睡眠用 `condition_variable::wait_for(..., 谓词)`，`close()` 可以打断它。

**面试官在探什么**

1. **为什么不先乘再比**：`current_ * multiplier_` 在上限接近 `LLONG_MAX` 时会溢出，有符号溢出是 UB（编译器可以假设它没发生），UBSan 一触发就终止。
2. **全抖动解决什么**：很多客户端同时断线，如果都按同样的时刻重连，服务端会被同时冲击（惊群，thundering herd）；在 `[0, 当前上限]` 内均匀取值把它们错开。随机数引擎由调用方传入，测试可以固定种子。
3. **pending 为什么要有界、计 `4 + len`**：断线期间 `offer` 仍然成功，保证顺序，但内存不能无限涨；按编码后的字节计，和出站环的单位一致，上限 `out_capacity`。`ChannelConfig(100, 500, 500)` 下每条 46 字节负载编码后 50 字节，恰好 10 条。
4. **语义要诚实**：已经进了旧通道出站环或内核缓冲区的消息，连接断掉时可能丢；TCP 只保证连接存续期间有序不丢，不保证对端应用处理了。要不丢必须有应用层序号加确认加重传（at-least-once），再加去重得到 effectively-once。这个类是 at-most-once 的尽力而为，丢失字节记在 `abandoned_bytes()`。
5. **`current_` 为什么是 `std::shared_ptr`**：应用线程在锁里拷贝一份指针，锁外去 `poll`；管理线程此时可能丢弃旧通道。裸指针或引用就是 use-after-free，拷贝的 `shared_ptr` 让最后一个持有者负责析构。锁外调用是因为 `poll` 会拿通道自己的锁、可能阻塞。
6. **何时重置退避**：连接成功就重置，这样下次断线从最短的等待开始；测试里 `Backoff(5, 2000, 4)` 失败几次后连上、被踢，重连必须在 1500 ms 内发生。
7. **关闭**：`close()` 置标志、关当前通道、`notify` 打断退避睡眠、幂等；析构函数也调 `close()`，管理线程不泄漏；`close()` 里 `join` 前判断不是管理线程自己，并用 `std::call_once` 保证只 `join` 一次。
8. **半开连接**：对端机器掉电，既没有 FIN 也没有 RST，TCP 在没有数据流动时不会探测。需要应用层心跳加空闲超时，`SO_KEEPALIVE` 的默认间隔太长。

**该说出口的话**：「`offer` 永远先进有界的 pending，保证顺序；已经交给旧连接的字节可能丢，我记在 `abandoned_bytes()` 里，这是 at-most-once。要不丢必须加序号、确认、重传。退避先除后乘防溢出，连上就重置。」

## C++ 专属的坑

- **`take` / `skip` / `peek_int` 先分配后检查**：`static_cast<std::size_t>(-1)` 变成 `2^64 − 1` → 抛的是 `bad_alloc` 或进程被杀，不是 `StateError` → 先比 `n > size_`，再分配。
- **线程声明在成员前面**：线程在 `mutex` 和环之前被构造，析构时它们先于线程销毁 → 线程还在用已销毁的对象 → 把 `std::jthread` 声明在最后，构造函数里最后才启动它，析构函数体先 `close()`。
- **两个线程同时 `close()` 都 `join`**：对同一个线程 `join` 两次是 UB → 用 `std::call_once` 保护，第二个调用者等第一个 `join` 完。
- **忘记 `SIGPIPE`**：对端重置后第一次 `send` 就杀死整个进程 → 每次 `send` 带 `kSendFlags`（macOS 上对 socket 设 `SO_NOSIGPIPE`）。
- **`std::thread` 成员忘了 `join`**：析构时 `std::terminate` → 用 `std::jthread`，或 RAII 保证每条路径都 `join`。
- **异常逃出线程函数**：`std::terminate` → I/O 线程和管理线程最外层 `catch (...)` 存成 `exception_ptr`。
- **`wpos_` / `wlen_` 无锁读写**：别的线程读 `unsent_bytes()` 时是数据竞争 → 锁里读写。
- **`ReconnectingClient::poll` 用裸指针**：管理线程丢弃旧通道时 use-after-free → 锁里拷贝 `shared_ptr`，锁外使用。
- **退避里写 `current_ * multiplier_ > max_`**：先乘溢出（有符号溢出是 UB） → 改成 `current_ > max_ / multiplier_` 再取 `max_`。
- **全抖动写成 `cap + 1`**：`cap == LLONG_MAX` 时溢出 → `uniform_int_distribution<long long>(0, cap)` 是闭区间，直接传 `cap`。
- **用 `sleep` 判断消息「应该已经到了」**：慢机器上偶发失败 → 带截止时间的轮询，只用来等「最终会发生」的事件。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 事件循环 | `Selector` + `interestOps` | `poll(2)` + 每轮重算的 `events` |
| 唤醒 I/O 线程 | `selector.wakeup()` | 自管道（`WakePipe`，一个字节） |
| 缓冲区 | `ByteBuffer`（`position` / `limit`，要 `flip()`） | `std::span` 加返回字节数，游标由调用方管 |
| 锁与等待 | `ReentrantLock` + `Condition` | `std::mutex` + `std::condition_variable`，等待要循环重查条件 |
| 失败原因 | `Throwable failure()` | `std::exception_ptr`，`rethrow_exception` 后 `catch` |
| 异常类型 | `IOException` / `EOFException` / `IllegalStateException` / `IllegalArgumentException` | `std::system_error`（带 `errno`）/ `EofError` / `StateError` / `std::invalid_argument` |
| 资源释放 | try-with-resources、GC | `UniqueFd` 的析构；`std::jthread`；对象析构就是 `close()` |
| 跨线程共享对象 | GC 保证存活 | `std::shared_ptr` 持有当前通道，必须明确所有权 |
| 线程生命周期 | 守护线程，`close()` 里限时 `join` | `std::jthread` 声明在最后，`std::call_once` 保证只 `join` 一次 |
| `SIGPIPE` | JVM 忽略 | `MSG_NOSIGNAL` / `SO_NOSIGPIPE` |
| 负数长度 | `int` 天然有负数 | 无符号 `size_t` 会把 `-1` 变成 `2^64 − 1`，检查在分配之前 |
| 备选方案 | 虚拟线程加阻塞 I/O | 没有对应物；每连接一线程，或协程（无标准调度器） |
