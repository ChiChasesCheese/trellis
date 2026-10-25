# ld03 · 异步 TCP 消息通道（C++20 版）

行情进程和策略进程之间、订单网关和交易所之间，数据都走一条 TCP 连接。TCP 给你的是**可靠、有序的字节流**，不是消息流：两条各 10 字节的消息，对端可能一次 `recv` 到 20 字节，也可能先收到 13 字节再收到 7 字节；`send` 在发送缓冲区快满时只写进去一部分；对端读得慢，TCP 窗口缩到 0，你的 `send` 就写不出去。题目要你在字节流之上做一个**有界**的消息接口：`offer(消息)` 发、`poll()` 收，满了就说「满了」，既不无限堆内存，也不阻塞到死。C++ 版用 POSIX `poll(2)` 加一个 I/O 线程，线程、互斥量、socket 的生命周期靠 RAII（对象析构时自动释放资源）管理。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `net`）。

## 读题前你需要知道

- **套接字、Nagle、`TCP_NODELAY`**：套接字（socket）是内核给进程的网络端点。Nagle 算法把小包攒起来再发以省带宽，代价是延迟；低延迟场景用 `TCP_NODELAY` 关掉它。通道必须开 `TCP_NODELAY`。
- **非阻塞 I/O 与 `poll(2)`**：非阻塞套接字上的 `recv` / `send` 立刻返回，可能读写 0 字节或一部分；没有数据可读、缓冲区已满时返回 `-1`，`errno` 为 `EAGAIN`（这不是错误，是背压的开始）。`poll(2)` 让一个线程等待多个描述符的「可读 / 可写」事件，你每轮声明关心哪些事件。
- **自管道**（self-pipe）：I/O 线程阻塞在 `poll` 里时，别的线程要叫醒它，就往一个管道的写端写一个字节，I/O 线程同时监听管道的读端。starter 已经给出 `detail::WakePipe`。
- **环形缓冲区**（ring buffer）：固定容量的字节数组，头指针和大小决定数据位置，读写到数组末尾时回绕，一次拷贝要拆成两段。这里容量可以是任意正整数，不要求 2 的幂。
- **RAII 与 `std::jthread`**：`UniqueFd` 是只能移动的文件描述符包装，析构时 `close`；`std::jthread` 析构时自动 `join`，没 `join` 的 `std::thread` 析构会 `std::terminate`。

## 公共类型（starter 已给出）

```cpp
using Bytes  = std::vector<std::uint8_t>;
using Millis = std::chrono::milliseconds;

struct FrameException : std::runtime_error {};   // 字节流不符合帧协议（负长度、超过 max_frame），无法恢复
struct StateError     : std::logic_error   {};   // 对象状态不对：已关闭、已 finish_sending、take 的字节不够
struct EofError       : std::runtime_error {};   // 对端在帧的中间关闭，流被截断
// 参数非法 → std::invalid_argument；系统调用失败 → std::system_error（带 errno）

class UniqueFd;                                  // 只能移动，析构 close(fd)
struct Address { std::string host; std::uint16_t port; };   // IPv4；loopback(port) = 127.0.0.1
class ChannelConfig {                            // 单位：字节
public:
    ChannelConfig(int max_frame, int out_capacity, int in_capacity);
    static ChannelConfig of(int max_frame);      // 两个环都是 64 KiB
};
```

- `max_frame`：最大负载（不含 4 字节长度头）。`out_capacity`、`in_capacity` 必须 `>= max_frame + 4`，否则最大的消息永远放不进或永远凑不齐；构造函数对非法值抛 `std::invalid_argument`（`max_frame < 0` 同样）。
- **帧格式**：`[len: int32 大端][payload: len 字节]`。`len` 的合法范围 `[0, max_frame]`，空负载合法。
- starter 还给出 POSIX 管道代码：`detail::WakePipe`（`wake()` / `drain()`）、`detail::set_nonblocking`、`detail::kSendFlags`（防 `SIGPIPE`，见 Part 2）。
- 所有测试在 `127.0.0.1` 加内核分配的临时端口上跑。正确性从不靠 `sleep` 判断，只用带截止时间的轮询等待「最终会发生」的事件。

## Part 1 · 字节环、成帧、增量解码（纯内存）

| 签名 | 要求 |
|---|---|
| `explicit ByteRing(std::size_t capacity)` | 容量为 0 抛 `std::invalid_argument`；任意正整数容量都要能用 |
| `capacity() / size() / free() / is_empty()` | 容量、已用、剩余、是否为空 |
| `std::size_t write(std::span<const std::uint8_t>)` | 尽量多写，返回写入数；调用方自己用 `subspan` 前进游标 |
| `std::size_t read(std::span<std::uint8_t>)` | 尽量多读，返回读出数 |
| `bool write_all(std::span<const std::uint8_t>)` | 全有或全无：放不下就一个字节都不写，返回 `false` |
| `std::int32_t peek_int(std::size_t offset = 0) const` | 从队首偏移 `offset` 处按大端读 4 字节，不消费；不足 4 字节抛 `StateError` |
| `Bytes take(std::size_t n)` / `void skip(std::size_t n)` | 不足 `n` 字节抛 `StateError`，状态不变；`take(0)` 返回空 |
| `void clear()` | 清空 |
| `static bool FrameCodec::encode(ByteRing&, std::span<const std::uint8_t>, int max_frame)` | 放不下返回 `false`，环原样不动（不留半个头）；负载超过 `max_frame` 抛 `std::invalid_argument` |
| `FrameDecoder(int max_frame, int capacity)` | `capacity < max_frame + 4` 抛 `std::invalid_argument` |
| `std::size_t feed(std::span<const std::uint8_t>)` | 只消费放得下的部分，返回消费数，可能小于输入长度 |
| `std::optional<Bytes> next()` | 凑齐一帧返回它，否则 `nullopt`；非法帧头抛 `FrameException` |
| `has_frame() / buffered() / free() / has_truncated_tail()` | 见下 |

- `ByteRing(8)` 写入 `{1,2,3,4,5,6}`，`take(4)` 取走前 4 个，再写 5 个字节 `{7,8,9,10,11}`：只剩 2 + 4 = 6 个空位在两段，所以写入 5 个；这 5 个跨过数组末尾，要拆成两段拷贝，`size()` 为 7。
- `ByteRing(5)` 里已有 3 字节，`write_all` 3 个字节返回 `false` 且 `size()` 仍为 3；再 `write_all` 2 个字节返回 `true`。
- 数据起点在槽位 4、容量 6，字节为 `12 34 56 78 9A` 时，`peek_int()` 是 `0x12345678`，`peek_int(1)` 是 `0x3456789A`，`peek_int(2)` 抛 `StateError`；`FF FF FF FF` 读出 `-1`（符号位）。
- `encode(r, {10,20,30}, 100)` 写出 `00 00 00 03 0A 14 1E`；300 字节负载的头是 `00 00 01 2C`；空负载的头是 `00 00 00 00`。`ByteRing(10)` 已有 7 字节时，`encode` 2 字节负载（要 6）和空负载（要 4）都返回 `false`，`size()` 仍为 7。
- **非法帧头**（`len < 0` 或 `len > max_frame`）必须只看 4 字节头就报错：`max_frame = 10` 时头 `00 00 00 0B` 立刻抛 `FrameException`，不等 11 个字节；头 `7F FF FF FF` 同样立刻抛，不能去分配 2 GiB。报错后**粘性失败**：之后每次 `next()` 都抛，`has_frame()` 仍为 `true`（`next()` 会返回消息或抛异常）。
- `has_truncated_tail()`：完整帧之后还有一截不完整的尾巴（半个头，或头完整而负载不全）。非法头不算截断。`FrameDecoder(5, 9)` 能收下恰好 `max_frame` 的帧；`FrameDecoder(5, 8)` 抛 `std::invalid_argument`。
- `feed` 有界：`FrameDecoder(4, 12)` 一次只收 12 字节，`free()` 变 0；调用方先 `next()` 腾空间，再继续喂剩下的。
- 每个切分点测试：三条消息的字节流在每一个下标切成两块先后喂入，结果必须相同；逐字节喂入、随机切块（100 条 × 40 轮）也一样。
- 性能：100 万条 32 字节消息经环加解码器要在 2 秒内（`perf` 标签，不带 sanitizer 的 `-O2` 构建）。
- C++ 专属测试：`take(static_cast<std::size_t>(-1))`、`skip` 同样参数、`peek_int(static_cast<std::size_t>(-1))` 都必须抛 `StateError`，不能先分配 `2^64 − 1` 字节再失败，也不能因为 `offset + 4` 回绕而误判。`ByteRing` 拷贝后是独立缓冲区，改一份不影响另一份。

## Part 2 · `TcpMessageChannel`（一条连接）

| 签名 | 要求 |
|---|---|
| `static std::unique_ptr<TcpMessageChannel> connect(const Address&, const ChannelConfig&, Millis = 3000ms)` | 连接并起 I/O 线程；失败抛 `std::system_error` |
| `static std::unique_ptr<TcpMessageChannel> wrap(UniqueFd, const ChannelConfig&)` | 接管已连接的 socket |
| `bool offer(std::span<const std::uint8_t>)` | 非阻塞；`true` = 已编码进出站环；`false` = 暂时放不下 |
| `bool offer(std::span<const std::uint8_t>, Millis)` | 等到放得下（`true`）或超时（`false`） |
| `std::optional<Bytes> poll()` / `poll(Millis)` | 返回一整条消息，没有则 `nullopt`；带超时的版本会等 |
| `void finish_sending()` | 已接受的消息刷完后发 FIN（半关闭） |
| `void close()` | 立刻关，丢弃未发送数据，唤醒所有等待者，幂等 |
| `is_open() / is_peer_closed() / is_drained() / unsent_bytes()` | 状态查询 |
| `std::exception_ptr failure() const` | 失败原因，没有失败为空指针 |
| `bool await_closed(Millis)` | 等到通道关闭 |
| `Address local_address() / remote_address() const` | 关闭后调用抛 `StateError` |
| `MessageServer(std::uint16_t port, const ChannelConfig&)` | 监听 `127.0.0.1`，端口 0 = 临时端口；`port()` / `address()` |
| `std::unique_ptr<TcpMessageChannel> MessageServer::accept(Millis)` | 超时返回 `nullptr`；`close()` 幂等 |

- **结构要求**：一个 I/O 线程跑 `poll(2)` 循环；应用线程只碰出站环（装编码后的帧）和入站解码器，两者在同一把互斥量下；系统调用都在 I/O 线程里，不持锁（唤醒管道的 `write` 例外，它在锁外）。
- `offer`：负载超过 `max_frame` 抛 `std::invalid_argument`（通道不受影响）；通道已关闭、已 `finish_sending` 或已失败抛 `StateError`；放不下返回 `false`。放得下时消息保证按序写进 socket，除非连接失败。
- **部分写**：`send` 只写了一部分时，剩余数据和位置要保留，等下一次 `POLLOUT`。大消息测试：6 条各约 0.5–1 MiB 的消息，`ChannelConfig(1 << 20, 4 << 20, 2 << 20)`，对端读到的每条内容必须完全一致。
- **部分读**：裸 socket 逐字节发一条 20 字节的帧，收到头加前 6 字节时 `poll(100ms)` 必须返回 `nullopt`；一次 `send` 写入「两条半」时，前两条各自可取，第三条等剩余字节到齐才可取。
- **失败语义**：对端发来非法帧头，之前收齐的消息仍可取，之后 `poll` 抛 `FrameException`，`failure()` 就是它，`is_open()` 变 `false`，`offer` 抛 `StateError`。对端在帧中间关闭（发了 `be32(3) "abc"` 和 `be32(10) "xyz"` 就关）：`abc` 仍可取，通道关闭，`failure()` 是 `EofError`，`is_drained()` 为 `true`。
- **EOF 不是关闭**：对端关闭后 `is_peer_closed()` 为 `true`，但仍可 `poll` 剩余的完整消息，仍可 `offer`（半关闭）。`is_drained()` = 不会再有新消息且缓冲区里没有完整消息。
- `finish_sending()`：之后 `offer` 抛 `StateError`；2000 条消息先全部到达对端，然后对端的 `poll` 才返回 `nullopt`；本端已发 FIN **且**对端也关闭时，两端自动关闭且 `failure()` 为空。
- `close()` 唤醒阻塞中的 `poll(30'000ms)` 和 `offer(msg, 30'000ms)`（后者抛 `StateError`）；对端会看到 EOF。
- **永不 `SIGPIPE`**：对端用 `SO_LINGER{1, 0}` 关闭（发 RST）后，持续 `offer`，进程必须活着；通道失败，`failure()` 是 `std::system_error`。
- C++ 专属测试：`TcpMessageChannel` 不可拷贝也不可移动（`static_assert`），`MessageServer`、`ReconnectingClient` 不可拷贝，`UniqueFd` 不可拷贝但可 `noexcept` 移动；`UniqueFd` 移动后原对象为空，最后一个持有者析构时描述符恰好关闭一次；销毁 `unique_ptr<TcpMessageChannel>` 就等于 `close()`，对端能收到之前已发出的数据和 EOF；`remote_address()` 与对端的 `local_address()` 相等；绑定一个已被占用的端口抛 `std::system_error`。

## Part 3 · 背压与有界性

| 签名 | 要求 |
|---|---|
| （同 Part 2，测的是行为） | 接收方不读时 `offer` 最终返回 `false`；入站环满时停止读 socket；最小缓冲区也不死锁 |

- **出站**：对端不读 ⟹ 内核发送缓冲区满 ⟹ `send` 返回 `EAGAIN` ⟹ 出站环渐满 ⟹ `offer` 返回 `false`。测试把内核缓冲区压到 4 KiB，`ChannelConfig(256, 8 * 1024, 8 * 1024)` 下一直 `offer(msg, 200ms)`，必须在 200 万条之前被堵住；堵住之后对端开始读，**每条被接受的消息按序、不丢、不重地到达**，随后又能 `offer`。
- **入站**：应用不 `poll` ⟹ 入站环满 ⟹ I/O 线程不再要求 `POLLIN` ⟹ 内核接收缓冲区满 ⟹ 对端写不出去。应用 `poll` 腾出空间后，**必须唤醒 I/O 线程**恢复读。`poll()`（非阻塞）和 `poll(Millis)` 都要。
- **最小缓冲区**：`ChannelConfig(64, 68, 68)`（容量恰好 `max_frame + 4`）下，2 万条长度 4–64 的消息按序全部到达；每条几乎都在环的回绕处被切开。用自旋的非阻塞 `poll()` 消费 5000 条，也不能卡死。
- `ChannelConfig(64, 1024, 136)`：入站环只放得下两条消息，读方每 500 条停 20 ms，3000 条仍然全部按序到达，内存不增长。
- 被堵住的 `offer(msg, 20'000ms)` 在对端开始读之后必须成功。
- 有界性：出站环、内核缓冲区、入站环之外，不能有任何随消息数增长的内存。
- 性能：20 万条 32 字节消息经回环 5 秒内（`perf`）；5000 条双向同时收发、1 万条单向按序到达（`conc`）。

## Part 4 · 退避与重连

| 签名 | 要求 |
|---|---|
| `Backoff(long long initial, long long max, int multiplier)` | `initial <= 0`、`max < initial`、`multiplier < 1` 抛 `std::invalid_argument` |
| `long long next()` | `initial, initial·m, initial·m², …` 封顶 `max`，永不溢出 |
| `template <std::uniform_random_bit_generator G> long long next(G&)` | 全抖动：在 `[0, next()]` 上均匀取值（含两端） |
| `void reset()` | 重新从 `initial` 开始 |
| `ReconnectingClient(const Address&, const ChannelConfig&, Backoff)` | 起后台管理线程 |
| `bool offer(std::span<const std::uint8_t>)` | 先进有界的 pending 队列；`false` = 满了；`close` 之后抛 `StateError`；负载超过 `max_frame` 抛 `std::invalid_argument` |
| `std::optional<Bytes> poll()` | 当前连接上的入站消息；断线期间 `nullopt` |
| `is_connected() / connect_count() / failed_attempts() / abandoned_bytes() / pending_bytes()` | 统计与状态 |
| `void close()` | 关当前通道，不再重连，幂等 |

- `Backoff(100, 1000, 2)` 依次给出 `100, 200, 400, 800, 1000, 1000`；`Backoff(5, 100, 3)` 给出 `5, 15, 45, 100`，`reset()` 后回到 `5`；`Backoff(10, 1000, 1)` 恒为 `10`；`Backoff(7, 7, 2)` 恒为 `7`。
- `Backoff(1, LLONG_MAX, 10)` 调用 100 次，序列单调不减、全为正，最后恰好是 `LLONG_MAX`。
- 全抖动：`Backoff(10, 80, 2)` 配 `std::mt19937`，六次结果分别落在 `[0,10] [0,20] [0,40] [0,80] [0,80] [0,80]` 内，且不全等于上限。`Backoff(1, LLONG_MAX, 2)` 调用 70 次不能抛异常或溢出。
- 管理线程：连接 ⟹ 成功后把 pending 按序搬进当前通道 ⟹ 通道断开（`!is_open()` 或 `is_peer_closed()`）⟹ 丢掉旧通道 ⟹ 退避后重连。连接失败时 `failed_attempts()` 加一，连接成功时 `backoff` 重置。
- pending 有界：已编码字节（每条 `4 + len` 之和）不得超过 `cfg.out_capacity()`。`ChannelConfig(100, 500, 500)` 下，无人监听时 46 字节的消息（每条编码后 50 字节）恰好接受 10 条，`pending_bytes()` 为 500，再 `offer` 空消息也是 `false`。
- 服务端踢掉连接 ⟹ 客户端自动重连，继续收发；服务端整个下线 ⟹ 断线期间 5 条 `offer` 仍然成功，同一端口重新上线后，这 5 条按序全部到达；`close()` 之后服务端再等 150 ms 也不会有新连接。
- 失败几次后连上，再被踢，重连应当从最短退避开始（`Backoff(5, 2000, 4)`，1500 ms 内重连成功）。
- **诚实的语义**：已交给旧通道（进了它的出站环或内核缓冲区）的消息，连接断掉时可能丢失；丢失字节数累计在 `abandoned_bytes()`。这是 at-most-once 的尽力而为。
- C++ 专属测试：销毁 `ReconnectingClient` 等于 `close()`：管理线程不泄漏，之后也不再重连；服务端能看到 EOF。

## 边界清单

- 环：容量 1、2、7、16、100 的随机读写对照 `std::deque` 模型；写满再写；回绕分两段；`write_all` 放不下一字节不写；`peek_int` 跨回绕、符号位；`take` / `skip` / `peek_int` 传 `static_cast<std::size_t>(-1)`
- 成帧：空负载；恰好 `max_frame`；`max_frame + 1`；负长度；`0x7FFFFFFF`；字节逐个到达；每个切分点；解码器满了 `feed` 返回部分；容量恰好 `max_frame + 4`
- 截断：半个头；头完整负载不全；完整帧后接半个头；非法头不算截断
- 通道 I/O：空消息、最大消息、几 MiB 大消息（部分写）、1 万条按序、双向各 5000 条、裸 socket 逐字节发送、一次写入「两条半」
- 错误：非法帧头；对端在帧中间关闭；对端发 RST；`close` 后 `offer`；`close` 唤醒阻塞的 `poll(30'000ms)` 和 `offer(msg, 30'000ms)`；绑定已占用端口
- 半关闭：`finish_sending` 后 `offer` 抛；对端先收齐全部再看到 EOF；对端仍能回话；双方都 `finish_sending` ⟹ 两端关闭且 `failure()` 为空
- 背压：不读 ⟹ `offer` 最终 `false` 且有界；读了之后全部按序到达；容量 `max_frame + 4` 压力；自旋 `poll()` 恢复暂停的读
- 退避：封顶；`reset`；`LLONG_MAX` 上限；`multiplier = 1`；全抖动范围；非法参数
- 重连：pending 有界；离线时 `offer` 成功；`close` 后不再重连；退避重置

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/03_lld/ld03_async_tcp_channel          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/03_lld/ld03_async_tcp_channel --tag part1
python3 tools/cpptest.py run   loop/rounds/03_lld/ld03_async_tcp_channel --tag io      # 真实 socket 的测试
python3 tools/cpptest.py run   loop/rounds/03_lld/ld03_async_tcp_channel --tag cpp     # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/03_lld/ld03_async_tcp_channel               # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 虚拟线程 / 线程池 + 阻塞 I/O：每个连接两个线程，代码更直，规模受限。
- 一个 `poll` / `epoll` / `kqueue` 循环管 N 个连接（回显服务器），再追问边缘触发与水平触发。
- 应用层序号加确认加重放：at-least-once，加去重得到 effectively-once。
- 心跳与空闲超时：检测对端掉电造成的半开连接。
- TLS：握手阶段读操作可能需要先写，兴趣集不再只由环的空位决定。
