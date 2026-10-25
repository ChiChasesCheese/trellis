# ld01 · 共享内存 SPSC 消息通道（C++20 版）

行情进程把一条条消息交给策略进程：只有一个写者（生产者）、一个读者（消费者）；通道有界，满了要告诉写者而不是无限涨；消息不丢、不重、不乱序；生产者说「没有更多了」之后，消费者要能分清「暂时没有」和「永远没有了」。热路径上没有锁、没有系统调用，两个线程甚至两个进程直接读写同一块内存。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `spsc`）。C++ 版的重点是三件事：`std::atomic` 的内存序、对象在内存里的布局（对齐、缓存行）、以及 mmap 和文件描述符的 RAII。

## 读题前你需要知道

- **环形缓冲区**（ring buffer）：固定容量 `capacity`（2 的幂）的数组。`head`（读计数）和 `tail`（写计数）只增不减，槽位下标 = `计数 & (capacity - 1)`。`tail - head == 0` 是空，`== capacity` 是满，空和满是两个不同的差值，不用空一格。
- **release / acquire**：写者先写数据，再用 `store(release)` 发布 `tail`；读者用 `load(acquire)` 读 `tail`，之后读到的数据一定是写者在 release 之前写好的。弱内存序的 CPU（ARM、Apple M）上少了这对屏障，读者会看到新 `tail` 却读到旧数据；x86 上常常碰巧不出错。
- **缓存行与伪共享**（false sharing）：CPU 以缓存行为单位搬数据。两个线程各写同一缓存行里的不同变量，这一行在两核之间来回失效。把两组变量隔开至少一个缓存行（starter 里 `kCacheLine = 128`）。
- **`std::atomic_ref<T>`**（C++20）：对一块已有的普通内存做原子读写，不要求这块内存里放着 `std::atomic`。共享内存里的 `head / tail / closed` 就这样访问。它要求地址按 `T` 对齐。
- **`mmap(MAP_SHARED)`**：把同一个文件映射进两个进程，两边看到的是同一批物理页。

## 公共类型（starter 已给出）

```cpp
struct StateError : std::logic_error { using std::logic_error::logic_error; };   // 已结束的生产者、已关闭的通道、不是通道的文件
struct EmptyError : std::runtime_error { using std::runtime_error::runtime_error; }; // LongQueue 空时 poll
inline constexpr std::size_t kCacheLine = 128;
using Bytes = std::vector<std::uint8_t>;

class LongQueue {                       // Part 1 和 Part 2 共用的接口
public:
    virtual ~LongQueue() = default;
    virtual int capacity() const = 0;
    virtual int size() const = 0;
    virtual bool offer(long long value) = 0;   // 满了返回 false，不覆盖
    virtual long long poll() = 0;              // 空了抛 EmptyError
    virtual bool is_empty() const = 0;
    virtual bool is_full() const { return size() == capacity(); }
};
```

## 共同约定

- **满不是错误**：`offer` 返回 `false`。**空**：`LongQueue::poll()` 抛 `EmptyError`（每个 `long long` 都可能是合法消息，没有哨兵值）；`MessageRing::poll()` 返回 `std::nullopt`。
- 容量必须是 2 的幂：`LongQueue` 系 `[1, 2^30]`，`MessageRing` 系 `[16, 2^30]`；否则抛 `std::invalid_argument`。
- **角色**：一个对象只扮演一种角色。生产者调 `offer / finish`，消费者调 `poll / is_drained`；`size()`、`bytes_pending()` 任何角色可调，是近似值，限制在 `[0, capacity]`。

## Part 1 · `LongRing`（单线程环形缓冲区）

| 签名 | 要求 |
|---|---|
| `explicit LongRing(int capacity)` | 容量非法抛 `std::invalid_argument`；拷贝构造 / 拷贝赋值 starter 已声明为 `= default` |
| `int capacity() / size() const`、`bool is_empty() const` | `size = tail - head` |
| `bool offer(long long)` | 满了返回 `false`，不覆盖最旧的元素 |
| `long long poll()` | 空了抛 `EmptyError` |

- 空 ⇔ `head == tail`；满 ⇔ `tail - head == capacity`；不另存 size，不浪费槽位。
- 容量 4：依次放 10、20、30、40 都成功，再放 50 返回 `false`；`poll()` 得 10 之后放 50 成功（写到数组开头）。
- `LLONG_MIN`、`-1`、`0`、`LLONG_MAX` 都是合法消息，原样进出。
- 容量 1 的环：放一个、再放返回 `false`、取出，循环 10 轮都正确。
- 100 万轮「放 2 个、取 2 个」之后计数仍然正确；随机操作 20 万步，结果和 `std::deque` 模型逐步一致，`size()` 逐步相等。
- 单线程 1000 万次 `offer + poll` 在 2 秒内完成（`perf` 标签）。
- C++ 专属测试：拷贝出来的环和原环互相独立；`LongRing c = std::move(a)` 之后 `a` 仍是可以继续 `offer / poll` 的合法环（starter 的注释讲了为什么）。

## Part 2 · `SpscLongRing`（线程安全 + 性能）

| 签名 | 要求 |
|---|---|
| `explicit SpscLongRing(int capacity)` | 语义同 `LongRing`；拷贝 / 移动已被删除 |
| `bool offer(long long)`、`bool is_full() const` | 只许生产者线程调用 |
| `long long poll()`、`bool is_empty() const` | 只许消费者线程调用 |
| `int size() const` | 任何线程，近似值，始终在 `[0, capacity]` |

- 恰好一个生产者线程加一个消费者线程，按序、恰好一次；**不许用锁，也不许用 CAS**。`tail` 只有生产者写，`head` 只有消费者写。
- 写槽位，再 `tail.store(release)`；消费者 `tail.load(acquire)`，再读槽位，再 `head.store(release)`。
- cached index：生产者缓存一份旧的 `head`，只有按旧值看是满的才去读真正的 `head`；消费者缓存 `tail`，同理。
- 生产者写的成员和消费者写的成员各放在不同的缓存行（每组的第一个成员用 `alignas(kCacheLine)`）。
- 容量 2（几乎每条消息都回绕）传 20 万条、重复 10 次；容量 64 传 30 万条、重复 10 次；容量 1 传 10 万条。每条都必须按序、恰好一次到达。
- 「读到旧槽位」检测：每个值由序号算出（序号乘一个常数），消费者对每条核对；容量 8、20 万条、重复 10 次。改成 `relaxed` 之后，ARM 上很快出错。
- 观察线程不停调用 `size()` 的同时生产、消费，读到的值永远在 `[0, 16]`（容量 16）。
- 两线程传 1000 万条在 2 秒内完成（`perf` 标签，无 sanitizer 的 `-O2` 构建）。
- C++ 专属测试：`SpscLongRing` 不可拷贝、不可移动；`std::atomic<std::uint64_t>` 和 `std::atomic_ref<std::uint64_t>` 必须 lock-free（`static_assert`）；`alignof(SpscLongRing) >= kCacheLine` 且 `sizeof >= 2 * kCacheLine`，`std::make_unique<SpscLongRing>(8)` 得到的对象地址按 `kCacheLine` 对齐。
- 提示：starter 已经写明：成员的缓存行归属用 `alignas(kCacheLine)` 标在每组的第一个成员上。

## Part 3 · `MessageRing`（变长消息 + 回绕）

| 签名 | 要求 |
|---|---|
| `static std::size_t segment_bytes(int capacity)` | `HEADER_BYTES + capacity`；非法容量抛 `std::invalid_argument` |
| `static MessageRing init(std::span<std::byte>, int capacity)` | 建新环；容量非法、segment 太小、首地址不是 8 字节对齐，都抛 `std::invalid_argument` |
| `static MessageRing attach(std::span<std::byte>)` | 连接已有的环；magic / version / 尺寸 / 对齐不对抛 `StateError` |
| `int capacity() / max_payload() const` | `max_payload = capacity - 4` |
| `bool offer(std::span<const std::uint8_t>)` | 生产者：放不下返回 `false`；长度超过 `max_payload()` 抛 `std::invalid_argument`；`finish()` 之后抛 `StateError` |
| `void finish()` | 生产者：置 closed，可重复调用 |
| `std::optional<Bytes> poll()` | 消费者：没有消息返回 `nullopt`（遇到 PAD 就越过它） |
| `bool is_drained() const` | 生产者已 `finish` 且 `head` 追上了 `tail`（末尾残留的 PAD 也算） |
| `long long bytes_pending() const` | 已发布未消费的字节数，含 PAD |

### 布局

```
偏移    0  magic     u64   0x5350534352494E47 ("SPSCRING")，最后用 release 写
偏移    8  capacity  u32
偏移   12  version   u32   = 1
偏移  128  head      u64   消费者已消费的字节计数（只有消费者写）
偏移  256  tail      u64   生产者已发布的字节计数（只有生产者写）
偏移  264  closed    u64   生产者 finish() 后置 1
偏移  512  数据区    capacity 字节
```

记录 = `[len:int32][payload][补零到 8 字节对齐]`，总长 `(4 + len + 7) & ~7`。放不下连续的一整条时，先写一条 PAD 记录（`len = -1`）占满到数据区末尾，再从偏移 0 写真记录。`head / tail / closed` 通过 `std::atomic_ref<std::uint64_t>` 带显式内存序访问，数据字节是普通内存，靠 `tail` 的 release / acquire 保护。

### 具体行为

- 容量 64：`init` 之后另一个对象 `attach`，`capacity() == 64`、`max_payload() == 60`；生产者放 `"hello"`，消费者取得 `"hello"`，再取得 `nullopt`。
- 记录大小：空消息占 8 字节（64 字节的环恰好放 8 条空消息，第 9 条返回 `false`）；`len = 4` 也是 8 字节；`len = 5` 是 16 字节（4 条之后满）；`len = 12` 是 16 字节（4 条之后满，`bytes_pending() == 64`）。
- `len = max_payload()` 恰好占满空环；`max_payload() + 1` 抛 `std::invalid_argument`（永远放不下，不同于暂时满）。
- 回绕：容量 64，放两条 `len = 20`（各 24 字节，`tail = 48`），都取走（`bytes_pending() == 0`）。再放一条 `len = 20`：末尾只剩 16 字节 < 24，先发布 16 字节的 PAD，再从偏移 0 写 24 字节，`bytes_pending() == 16 + 24`。消费者 `poll` 一次直接得到这条消息。
- **PAD 单独发布**：同样放两条 `len = 20` 但不取走，再放第三条：PAD 放得下（剩 16 字节）、真记录放不下，返回 `false`，但此时 `bytes_pending() == 48 + 16`。消费者取走第一条之后，同一条消息再 `offer` 成功。
- 活性：在空环上，无论 `tail` 停在哪里，`offer(最大消息)` → 消费者越过 PAD → 再 `offer` 必须成功（500 轮随机位置）。
- drained：空但生产者没 `finish` 不算 drained；还有未读消息不算；`finish()` 之后 `offer` 抛 `StateError`。末尾残留 PAD 时，两条消息读完 `is_drained()` 仍为 `false`，再 `poll()`（返回 `nullopt`、越过 PAD）之后才为 `true`。
- `offer` 拷贝调用方的字节；`poll` 返回的 vector 归调用方，改它不影响环。
- 随机 30 万步，放入长度随机的消息、取出，结果和 `std::deque` 模型逐步一致，且 `bytes_pending() <= 256`；这个序列必须真的触发过满和回绕。
- 生产者线程和消费者线程（容量 256，每条 8 到 56 字节，由序号确定）传 2 万条，重复 10 次，按序、恰好一次、不损坏。
- 单线程 200 万条 24 字节的消息在 2 秒内（`perf`）；两线程 200 万条变长消息在 3 秒内（`perf`）。
- C++ 专属测试：
  - 「空消息」是持有空 vector 的 `optional`，「没有消息」是 `nullopt`，两者必须分得开。
  - 首地址偏移 4 字节的 segment：`init` 抛 `std::invalid_argument`，`attach` 抛 `StateError`；偏移 8 字节则可以用。
  - `offer` 接受任意连续字节区间：C 数组、`std::array`、`std::vector` 都能直接传。

## Part 4 · `SharedChannel`（内存映射文件，两个进程）

| 签名 | 要求 |
|---|---|
| `static SharedChannel create(const std::filesystem::path&, int capacity)` | 新建或截断文件，大小 `segment_bytes(capacity)`，`mmap` 后 `MessageRing::init`；容量非法抛 `std::invalid_argument`，**且不碰文件** |
| `static SharedChannel open(const std::filesystem::path&)` | 映射已有文件并 `attach`；文件不存在抛 `std::system_error`（`errc::no_such_file_or_directory`）；太小、全零、随机内容抛 `StateError` |
| `bool send(std::span<const std::uint8_t>)`、`void finish()` | 生产者 |
| `std::optional<Bytes> receive()`、`bool is_drained() const` | 消费者 |
| `void close() noexcept` | 取消映射，可重复调用，文件留在磁盘上；之后（以及被移走之后）任何访问抛 `StateError` |

- 同一个文件 `create` 一次、`open` 一次，两边共享数据：文件大小等于 `segment_bytes(1024)`，一边 `send` 另一边 `receive`，`finish` 后另一边 `is_drained()`。
- 容量 64 的通道，`send(Bytes(12))` 能成功 4 次，第 5 次 `false`；对方 `receive` 一条之后又能 `send`。
- 生产者对象析构（取消映射）之后重新 `open`，积压的 20 条消息还在。
- `create(file, 100)` 抛 `std::invalid_argument`，不能留下新文件；对一个已有的 3 字节文件 `create(file, 1000)` 同样抛异常，文件内容原样保留。
- 跨进程测试用 `fork()` 起子进程，子进程自己重新 `open` 文件，结果通过 `pipe` 回传：
  - 父生产、子消费：10 万条，容量 16 KiB；
  - 子生产、父消费：10 万条，容量 4 KiB；
  - 父写完并析构后，子才启动再读 50 条（数据只可能来自文件）。
- 两端的自旋循环都带截止时间（20 秒）；子进程崩溃或超时，父进程能报告失败而不是挂死。
- C++ 专属测试：`SharedChannel` 不可拷贝，移动构造是 `noexcept`；被移走的对象 `send` 抛 `StateError`；移动赋值会先取消赋值目标原来的映射。

## 边界清单

- 容量：`0`、负数、`3`、`1000`、`2^30 + 1`、`INT_MAX`、`INT_MIN`；`MessageRing` 另有 `1`、`8`、`15`、`17`、`24`
- 满 / 空：满了 `offer` 不覆盖；空了 `poll` 抛 `EmptyError` / 返回 `nullopt`；容量 1；满 → 腾一个 → 回绕写入
- 值：`LLONG_MIN`、`-1`、`0`、`LLONG_MAX` 都是合法消息
- 消息：空消息、`len = 4`、`len = 5`、`len = max_payload()`、`max_payload() + 1`、含 `0xFF` 和 `0` 的二进制
- 回绕：末尾只剩 8 字节；剩的不够当前记录；PAD 已发布但真记录没挤进去；空环加最大消息，`tail` 在任意位置
- drained：空但没 `finish`；有消息没读完；末尾残留 PAD；`finish` 两次；`finish` 后 `offer`
- 内存：segment 太小；首地址偏移 4 字节；文件太小 / 全零 / 随机内容
- 进程：文件不存在；`close` 之后访问；关闭后重开仍有积压；子进程提前退出

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/03_lld/ld01_spsc_channel                 # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/03_lld/ld01_spsc_channel --tag part1
python3 tools/cpptest.py run   loop/rounds/03_lld/ld01_spsc_channel --tag conc      # 线程和进程的测试
python3 tools/cpptest.py run   loop/rounds/03_lld/ld01_spsc_channel --tag cpp       # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/03_lld/ld01_spsc_channel                 # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 多生产者：`tail` 变成 CAS 竞争，或者每个生产者一个环、消费者轮询。
- 零拷贝：生产者向环申请一段连续区域，直接写进去再提交；消费者用回调读，回调返回后才归还。
- 崩溃恢复：`head` 在文件里，消费者重启后接着读；处理到一半的消息会被重读，下游要幂等。
