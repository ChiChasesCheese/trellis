# ld01 · 共享内存 SPSC 消息通道（Shared-Memory SPSC Channel）（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

一个生产者、一个消费者，中间一条有界的消息通道：满了要明确告诉生产者「满了」，消息不丢、不重、不乱序，生产者说「不会再有了」之后消费者能区分「暂时没有」和「永远没有了」。热路径上没有锁，也没有系统调用——两个线程（后来是两个进程）直接读写同一块内存。环形缓冲区（ring buffer）是这块内存的组织方式，内存序（memory order）决定另一边什么时候能看到你写的东西。

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `LongRing`（`LongQueue`） | 单线程环形缓冲区：`long long` 元素，容量是 2 的幂，自由增长的 head / tail 计数 | 空和满怎么区分；`& mask`；没有哨兵值 |
| 2 | `SpscLongRing` | 两个线程：`std::atomic` + release / acquire，cached index，`alignas` 防伪共享 | 为什么不要 CAS；每个内存序保护什么；怎么证明伪共享存在 |
| 3 | `MessageRing` | 字节数组上的变长消息：长度前缀、8 字节对齐、回绕（PAD 记录）、`finish` / `is_drained` | PAD 必须单独发布，否则死锁 |
| 4 | `SharedChannel` | 同一个环放进 `mmap` 的文件，两个进程各映射一份 | RAII 管理映射；跨进程测试（`fork`） |

共同约定：

* **满不是错误**：`offer` 返回 `false`。**空**：`LongQueue::poll()` 抛 `EmptyError`（`long long` 的每个取值都可能是合法消息，没有哨兵）；`MessageRing::poll()` 返回 `std::nullopt`。
* 容量必须是 2 的幂：`LongQueue` 系 `[1, 2^30]`，`MessageRing` 系 `[16, 2^30]`，否则抛 `std::invalid_argument`。
* 一个对象只扮演一种角色：生产者对象调 `offer` / `finish`，消费者对象调 `poll` / `is_drained`。`size()`、`bytes_pending()` 任何角色可调，结果是近似值。
* 异常是接口的一部分：`EmptyError`（`std::runtime_error`）、`StateError`（`std::logic_error`，对应 Java 的 `IllegalStateException`）。

```
LongRing r(4);
r.offer(10); r.offer(20); r.offer(30); r.offer(40);
r.offer(50);   // false  —— 满了，不覆盖
r.poll();      // 10
r.offer(50);   // true   —— 回绕到数组开头
r.size();      // 4
```

## 2. Part 1：`LongRing`

head 和 tail 是只增不减的计数（`std::uint64_t`）。元素个数 `tail - head`；槽位下标 `计数 & mask`（`mask = capacity - 1`）。

* **空** ⇔ `head == tail`，**满** ⇔ `tail - head == capacity`。如果 head / tail 存的是 `0..capacity-1` 的下标，`head == tail` 既可能是空也可能是满，只能多浪费一个槽位或另存一个 size；自由增长的计数让两种状态是两个不同的差值。
* `& mask` 代替 `% capacity`：除法几十个周期，按位与一个周期，对 2 的幂结果相同。
* 计数用**无符号**类型：无符号回绕有定义（`2^64` 个之后回到 0，每纳秒一次也要几百年），差值 `tail - head` 在回绕时仍然正确；有符号溢出是未定义行为（undefined behaviour，UB）。

```cpp
class LongRing final : public LongQueue {
public:
    explicit LongRing(int capacity) : buf_(check(capacity)), mask_(static_cast<std::uint64_t>(capacity) - 1) {}
    LongRing(const LongRing&) = default;             // 声明了拷贝 ⇒ 不会生成隐式移动（见下）
    LongRing& operator=(const LongRing&) = default;

    bool offer(long long value) override {
        if (tail_ - head_ == buf_.size()) return false;
        buf_[tail_ & mask_] = value;
        ++tail_;
        return true;
    }
    long long poll() override {
        if (head_ == tail_) throw EmptyError("ring is empty");
        return buf_[head_++ & mask_];
    }
    // ...capacity(), size(), is_empty()
private:
    std::vector<long long> buf_;
    std::uint64_t mask_, head_ = 0, tail_ = 0;
};
```

容量检查用 `std::has_single_bit`（`<bit>`，C++20）：`has_single_bit(x)` 当且仅当 `x` 恰有一位是 1，也就是 2 的幂；`capacity` 是 `int`，先判 `[1, 2^30]` 再转无符号，负数不会被误当成一个巨大的 2 的幂。

### 2.1 移动之后的环

隐式生成的移动构造会把 `std::vector` 搬空，但 `mask_` 只是被拷贝：被移动过的环 `buf_` 为空、`mask_` 还是旧值，下一次 `offer` 就写越界。解决办法有两种：手写移动让被移动的对象成为合法的对象；或者像这里一样**只声明拷贝**——声明了拷贝构造 / 赋值就不会生成隐式移动，`std::move(r)` 退化成拷贝，原对象毫发无损。代价是多一次拷贝，对这个类（不在热路径上被搬来搬去）无所谓。这是「五法则」（rule of five）的一个具体后果：只要你的类有一个字段与另一个字段的值**相互依赖**，默认的逐字段移动就可能破坏不变量。

## 3. Part 2：`SpscLongRing`

### 3.1 为什么不需要锁，也不需要 CAS

`tail` 只有生产者写，`head` 只有消费者写：每个共享变量**只有一个写者**，不存在「两个人同时改同一个变量」，也就不需要比较并交换（compare-and-swap，CAS）。需要的只是两件事：

* **可见性**：一边写的值另一边最终看得到；
* **顺序**：先写数据、后发布 `tail`；先读完数据、后归还 `head`。

### 3.2 内存序

`std::atomic` 的每个操作可以带一个 `std::memory_order`。默认的 `seq_cst` 最强也最贵；这里只需要「发布」和「获取」：

```
生产者                         消费者
------                         ------
slot[i] = v          (1)
tail.store(t+1, release) (2)
                           t = tail.load(acquire)  (3)
                           v = slot[i]             (4)
                           head.store(h+1, release)(5)
```

* (2) release 保证 (1) 不会被重排到 (2) 之后；(3) acquire 保证 (4) 不会被重排到 (3) 之前；只要 (3) 读到了 (2) 写的值，(4) 就一定看到 (1) 写的数据。这叫 **synchronizes-with**。
* (5) release：消费者读完槽位才归还；生产者用 acquire 读到新的 `head` 之后才会覆盖这个槽，这样 (4) 的读一定发生在覆盖之前。

| 位置 | 序 | 理由 |
|---|---|---|
| 生产者 `tail_.store` | `release` | 把 (1) 的数据写**发布**出去 |
| 消费者 `tail_.load` | `acquire` | 与上面配对，之后才读数据 |
| 消费者 `head_.store` | `release` | 读完才归还槽位 |
| 生产者 `head_.load`（刷新 cached index） | `acquire` | 与上面配对，之后才覆盖槽位 |
| 生产者读自己的 `tail`、消费者读自己的 `head` | 普通读（私有副本） | 只有自己写，不需要原子 |

x86 的内存模型很强（TSO，store 不会越过 store），所以把 `release` 写成 `relaxed` 在 x86 上多半碰巧能跑。ARM / Apple M 是弱内存模型，同样的错误会立刻出现：把 `tail_.store` 改成 `relaxed`，测试在几千条消息内就读到旧值（`first mismatch at seq …`）。**在 x86 上跑通不代表内存序对**。

### 3.3 cached index

生产者每次 `offer` 都要知道「满了没」，原本得读一次 `head`——消费者一直在写它，这条缓存行总在消费者的核上，读它要跨核通信。办法：生产者保存一份旧的 `head`（`cached_head_`），**只有按旧值看是满的**才去读真正的 `head`。`head` 只增不减，旧值只会让生产者**低估**空位，绝不会高估，所以按旧值判断「有空位」永远安全。消费者缓存 `tail` 同理。稳态下每个线程每一批只碰一次对方的缓存行，而不是每条消息一次。

### 3.4 伪共享与 `alignas`

CPU 以缓存行（cache line，x86 是 64 字节，Apple M 是 128 字节）为单位搬运数据。两个线程分别写同一缓存行里的**不同**变量时，这一行在两个核之间来回失效，互相拖慢，叫**伪共享**（false sharing）。下面的程序量一量：

```cpp
// Two counters updated by two threads: on one cache line they fight over it; on separate lines they do not.
// Build with -O2 and no sanitizers; the gap matters, not the absolute numbers.
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>

struct Adjacent { std::atomic<long long> a{0}, b{0}; };
struct Padded { alignas(128) std::atomic<long long> a{0}; alignas(128) std::atomic<long long> b{0}; };

template <class T> double run(T& c) {
    constexpr int iterations = 50'000'000;
    const auto t0 = std::chrono::steady_clock::now();
    {
        std::jthread x([&] { for (int i = 0; i < iterations; ++i) c.a.fetch_add(1, std::memory_order_relaxed); });
        std::jthread y([&] { for (int i = 0; i < iterations; ++i) c.b.fetch_add(1, std::memory_order_relaxed); });
    }
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}
int main() {
    for (int round = 0; round < 3; ++round) {
        Adjacent s; Padded p;
        std::cout << "same line: " << run(s) << " ms   separate lines: " << run(p) << " ms\n";
    }
}
```

在 Apple M 上典型输出是 `same line: 560 ms   separate lines: 66 ms`，差 8 倍左右。逻辑上两个线程没有任何共享，慢的完全是缓存一致性协议。

`alignas(N)` 加在**成员**上，C++ 就把这个成员放到 N 字节对齐的偏移，并且让整个类的对齐至少是 N（类的大小向上取整到 N 的倍数）。Java 没有这个关键字，要靠继承链里塞一堆 `long` 字段把热字段推开。`SpscLongRing` 的布局：

```cpp
std::vector<long long> buf_;       // 构造后只读：两个线程都读，没人写
std::uint64_t mask_;
alignas(kCacheLine) std::atomic<std::uint64_t> tail_{0};   // 生产者写的东西从新的一行开始
std::uint64_t producer_tail_ = 0;  // 生产者对自己 tail 的私有副本
std::uint64_t cached_head_ = 0;
alignas(kCacheLine) std::atomic<std::uint64_t> head_{0};   // 消费者写的东西从另一行开始
std::uint64_t consumer_head_ = 0;
std::uint64_t cached_tail_ = 0;
```

三点：

* 一个组里的字段（`tail_`、`producer_tail_`、`cached_head_`）都只被生产者线程**写**，放在同一行没问题；
* 只读字段（`buf_`、`mask_`）放在最前面，不会因为生产者每次写 `tail_` 而被无谓地失效；
* 类整体对齐到 `kCacheLine`，所以相邻的对象也不会和最后一个组共享缓存行。`std::make_unique<SpscLongRing>` 对过度对齐（over-aligned）类型自动用对齐版的 `operator new`（C++17 起）。

`kCacheLine` 为什么自己定义成 128，而不用 `std::hardware_destructive_interference_size`？这个常量由编译器给出，同一个编译器在不同的 `-mtune` 下可以给不同的值（GCC 在头文件里用它还会发 `-Winterference-size` 警告）；Apple clang 上它是 256，比真实的 128 保守得多。更重要的是 Part 3 / 4 的**布局要写进文件**，两个进程用不同编译器编译出不同的值就对不上了。所以：对象内部布局用 128 这样的固定常量，宁可在 x86 上多浪费一点。

### 3.5 代码

```cpp
bool offer(long long value) override {  // 仅生产者
    const std::uint64_t t = producer_tail_;
    if (t - cached_head_ == buf_.size()) {            // 按旧快照是满的 ⇒ 才读真正的 head
        cached_head_ = head_.load(std::memory_order_acquire);
        if (t - cached_head_ == buf_.size()) return false;
    }
    buf_[t & mask_] = value;                           // (1) 数据
    producer_tail_ = t + 1;
    tail_.store(t + 1, std::memory_order_release);     // (2) 发布
    return true;
}

long long poll() override {  // 仅消费者
    const std::uint64_t h = consumer_head_;
    if (h == cached_tail_) {                           // 按旧快照是空的 ⇒ 刷新
        cached_tail_ = tail_.load(std::memory_order_acquire);   // (3)
        if (h == cached_tail_) throw EmptyError("ring is empty");
    }
    const long long v = buf_[h & mask_];               // (4)
    consumer_head_ = h + 1;
    head_.store(h + 1, std::memory_order_release);     // (5)
    return v;
}

int size() const override {  // 任何线程，近似值：先读 head 再读 tail，tail 只增所以差不为负
    const std::uint64_t h = head_.load(std::memory_order_acquire);
    const std::uint64_t t = tail_.load(std::memory_order_acquire);
    return static_cast<int>(std::min<std::uint64_t>(t - h, buf_.size()));
}
```

`static_assert(std::atomic<std::uint64_t>::is_always_lock_free)`：如果这个类型在目标平台上不是真正的原子指令、而是藏着一把锁，编译就失败——「无锁」在编译期被验证。`std::atomic` 不可拷贝、不可移动（它的身份就是它的地址），所以 `SpscLongRing` 也不可拷贝、不可移动；测试里用 `static_assert` 固定住这一点。

## 4. Part 3：`MessageRing`

### 4.1 布局与记录

环建在一块 `std::span<std::byte>` 上（堆、共享内存、`mmap` 的文件都行）：

| 偏移 | 内容 |
|---|---|
| 0 | `magic`（`u64`，`"SPSCRING"`，**最后**用 release 写） |
| 8 / 12 | `capacity`（`u32`）/ `version`（`u32` = 1） |
| 128 | `head`（`u64`，只有消费者写） |
| 256 | `tail`（`u64`，只有生产者写） |
| 264 | `closed`（`u64`，`finish()` 后置 1） |
| 512 | 数据区，`capacity` 字节 |

记录 = `[len:int32][payload][补零到 8 字节对齐]`，总长 `(4 + len + 7) & ~7`。放不下**连续**的一整条时，先写一条 PAD 记录（`len = -1`）占满到数据区末尾，再从开头写真记录：一条记录不能被切成两半，读的人要拿到连续的字节。

### 4.2 `std::atomic_ref`：给「别人的内存」加原子访问

`head` / `tail` / `closed` 住在调用者给的一块**普通字节**里，不是 `std::atomic` 成员。C++20 的 `std::atomic_ref<T>` 就是为这个设计的：对一个已经存在的、对齐合格的 `T` 对象临时包一层原子接口。

```cpp
static std::atomic_ref<std::uint64_t> word(std::span<std::byte> seg, std::size_t off) {
    return std::atomic_ref<std::uint64_t>(*reinterpret_cast<std::uint64_t*>(seg.data() + off));
}
// 用法：
word(seg_, OFF_TAIL).store(t + rec, std::memory_order_release);
const auto t = word(seg_, OFF_TAIL).load(std::memory_order_acquire);
```

三条规矩：

* **对齐**：`atomic_ref<uint64_t>::required_alignment` 是 8（这台机器上），地址不满足就是 UB。所以 `init` / `attach` 一开始就检查 `seg.data()` 是否 8 字节对齐，不满足抛异常（`init` 抛 `std::invalid_argument`，`attach` 抛 `StateError`）。Java 的堆上 `byte[]` 段做 `long` 原子访问同样会出错，道理一样。
* **锁自由**：`static_assert(std::atomic_ref<std::uint64_t>::is_always_lock_free)`。放进**共享内存**的原子操作必须是真正的原子指令；如果是靠一把进程内的锁模拟的，另一个进程根本看不到这把锁，等于没有同步。
* **不要混用**：同一块内存在某个时刻要么都用 `atomic_ref` 访问，要么都不用；普通读写和原子访问并发是数据竞争。头部的 `capacity` / `version` 在 `magic` 被 release 发布之前写、被 acquire 读到 `magic` 之后读，所以用 `memcpy` 的普通访问是安全的。

### 4.3 PAD 要单独发布

```cpp
bool offer(std::span<const std::uint8_t> msg) {
    // ... 参数检查，rec = record_size(len)，t = tail_，idx = t & mask_，to_end = capacity - idx
    if (rec > to_end) {                       // 放不下连续的一整条：先单独发布一条 PAD，占满剩余部分
        if (!has_room(t, to_end)) return false;
        store32(seg_, HEADER_BYTES + idx, static_cast<std::uint32_t>(PAD));
        t += to_end;
        tail_ = t;
        word(seg_, OFF_TAIL).store(t, std::memory_order_release);
        idx = 0;
    }
    if (!has_room(t, rec)) return false;      // 真记录放不下 ⇒ false，但 PAD 已经发布
    std::memcpy(at + 4, msg.data(), len);     // payload
    store32(seg_, HEADER_BYTES + idx, len);   // 长度前缀
    tail_ = t + rec;
    word(seg_, OFF_TAIL).store(t + rec, std::memory_order_release);   // 发布
    return true;
}
```

**为什么 PAD 必须单独发布**：想象环是空的，`tail` 恰好停在离末尾 16 字节的地方，要放一条 60 字节的最大消息。PAD 要 16 字节，真记录要 64 字节，加起来 80 > 64。如果把「PAD + 记录」当整体判断，永远放不进去；而环是空的，消费者没有东西可读，也就不会前进——**死锁**。单独发布 PAD 之后：`offer` 返回 `false`，消费者调 `poll`、越过 PAD（返回 `nullopt`），`head` 追上 `tail`，下一次 `offer` 从偏移 0 开始，空环里一定放得下。代价是 `offer` 返回 `false` 时可能已经悄悄发布了一条 PAD，对消息序列没有影响。

`has_room` 就是 cached index：先用缓存的 `head` 判断，不够再读真正的 `head`（acquire）。

### 4.4 消费者与 drained

```cpp
std::optional<Bytes> poll() {
    std::uint64_t h = head_;
    while (true) {
        if (h == cached_tail_) {
            cached_tail_ = word(seg_, OFF_TAIL).load(std::memory_order_acquire);
            if (h == cached_tail_) return std::nullopt;
        }
        const auto idx = static_cast<std::uint32_t>(h & mask_);
        const auto len = static_cast<std::int32_t>(load32(seg_, HEADER_BYTES + idx));
        if (len == PAD) { h += capacity_ - idx; head_ = h; word(seg_, OFF_HEAD).store(h, std::memory_order_release); continue; }
        Bytes out(len);                             // 拷贝出来：之后立刻归还空间
        std::memcpy(out.data(), seg_.data() + HEADER_BYTES + idx + 4, out.size());
        h += record_size(len);
        head_ = h;
        word(seg_, OFF_HEAD).store(h, std::memory_order_release);   // 读完才归还
        return out;
    }
}
bool is_drained() const {
    if (word(seg_, OFF_CLOSED).load(std::memory_order_acquire) == 0) return false;   // 先读 closed
    return head_ == word(seg_, OFF_TAIL).load(std::memory_order_acquire);            // 再读 tail
}
```

* **`std::optional<Bytes>` 区分「没有消息」和「空消息」**：Java 用 `null` 表示没有、`byte[0]` 表示空消息；C++ 里 `nullopt` 与「持有空 vector 的 optional」是两个不同的值，类型本身把二者分开了。
* **`is_drained` 要先读 `closed` 再读 `tail`**：生产者是「先发布最后一次 `tail`，再置 `closed`」。消费者看到 `closed == 1` 就保证已经看到了最终的 `tail`；反过来读会漏掉最后几条消息。
* **末尾残留的 PAD**：`finish` 之后环里可能只剩一条孤零零的 PAD。`is_drained` 在消费者 `poll` 越过它之前是 `false`。
* **每次 `poll` 分配一个 `Bytes`**：热路径上这是一次 `malloc`。更接近 Aeron / Disruptor 的接口是 `poll_with(callback)`：回调直接拿到环里的 `std::span<const std::uint8_t>`，不拷贝，回调返回后才归还空间。追问里常问。

## 5. Part 4：`SharedChannel`

同一个环放进一个**内存映射文件**（memory-mapped file）。操作系统把文件的页缓存同时映射进两个进程的地址空间（`MAP_SHARED`），两边读写的是同一批物理页，热路径上没有 `read` / `write` 系统调用，也不拷贝。release / acquire 约束的是各自 CPU 和编译器的重排，缓存一致性由硬件保证，所以**跨进程时内存序仍然成立**。

### 5.1 RAII：文件描述符和映射

Java 有 `try-with-resources`，C++ 用析构函数。两个小类：

```cpp
class Fd {                     // 打开的文件描述符：离开作用域就 close
    explicit Fd(int fd);  ~Fd() { if (fd_ >= 0) ::close(fd_); }
    // 不可拷贝
};
class Mapping {                // 一块 mmap 区域：析构 munmap；可移动，被移动的对象是「空」
    Mapping(int fd, size_t size);  // mmap(…, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)，失败抛 std::system_error
    Mapping(Mapping&& o) noexcept : p_(std::exchange(o.p_, nullptr)), size_(std::exchange(o.size_, 0)) {}
    ~Mapping() { reset(); }
    void reset() noexcept { if (p_) ::munmap(p_, size_); p_ = nullptr; size_ = 0; }
};
```

`create` 与 `open`：

```cpp
static SharedChannel create(const std::filesystem::path& file, int capacity) {
    const std::size_t size = MessageRing::segment_bytes(capacity);   // 先校验容量，再动文件
    Fd fd(::open(file.c_str(), O_RDWR | O_CREAT | O_TRUNC, 0644));
    if (fd.get() < 0) throw_errno("open");
    if (::ftruncate(fd.get(), size) != 0) throw_errno("ftruncate");  // 新增的部分全是 0
    Mapping map(fd.get(), size);                                     // 映射建好后 fd 可以关
    auto ring = MessageRing::init(map.span(), capacity);
    return SharedChannel(std::move(map), ring);
}
```

* **`attach` / `init` 抛异常时映射自动释放**：`Mapping` 是局部变量，栈展开时析构。Java 版要在 `catch` 里手写 `arena.close()`；这里没有清理代码，也就不会漏。这是 RAII 相对 `try / finally` 的核心优势。
* 容量非法 ⇒ `segment_bytes` 抛 `std::invalid_argument`，**先于** `open`，所以不会截断一个已有的文件。顺序决定了「失败不留痕迹」。
* 文件不存在 ⇒ `std::system_error`，其 `code()` 是 `std::errc::no_such_file_or_directory`（保存了 `errno`）；Java 对应 `NoSuchFileException`。太小 / 全零 / 随机内容 ⇒ `StateError`。
* `SharedChannel` 只能移动。被移动的、或调过 `close()` 的通道，`send` / `receive` 抛 `StateError`（映射已经没了，再访问就是段错误，所以必须在访问前检查）。

### 5.2 跨进程怎么测试

Java 要启动第二个 JVM（找 `java` 可执行文件、拼 classpath、`--enable-preview`……）。C++ 只要 `fork()`：子进程是父进程的完整副本，重新 `SharedChannel::open(path)` 得到**自己的**映射。

```cpp
const auto child = spawn_child([&] {
    auto mine = SharedChannel::open(file);            // 子进程自己 mmap 一次
    return consume(mine, n, child_deadline());        // "" = 成功，否则是错误描述
});
const auto err = produce(ch, n, child_deadline());    // 父进程同时生产
CHECK_EQ(err, "");
CHECK_EQ(join_child(child), "");
```

* 子进程的结论通过一个 `pipe` 传回，进程用 `_exit` 结束（不跑析构、不刷新父进程 stdio 缓冲区的副本）；
* 父进程用 `waitpid(WNOHANG)` 轮询加截止时间，超时 `kill(SIGKILL)`；两端的自旋循环都带截止时间——**任何一端挂死都不能让整个测试挂死**；
* 消息的长度和内容由序号决定（`make_msg(seq)`，`splitmix64`），收的人不需要额外信息就能校验「是不是第 seq 条」，丢、重、乱序、截断都会被抓到；
* `fork` 只复制调用它的那个线程：测试里所有线程都在测试结束前 `join`，`fork` 时进程里只有主线程，子进程不会继承到「持有锁的线程已经不存在」的状态。

三个用例：父生产 → 子消费；子生产 → 父消费；父先写完并销毁通道，子之后才启动再读（证明数据在文件里）。

## 6. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| `VarHandle.setRelease` / `getAcquire` | `std::atomic<T>::store(v, release)` / `load(acquire)` | 同一套 C++11 内存模型；`std::atomic` 在类型里，`atomic_ref` 用于别人的内存 |
| 继承链 + 填充 `long` 字段推开热字段 | `alignas(kCacheLine)` | 语言直接支持对齐；不用依赖「JVM 按继承顺序排字段」 |
| `MemorySegment` + `Arena` | `std::span<std::byte>` + 调用方负责内存 | span 只是视图，不拥有；生命周期由映射 / 分配方的 RAII 管 |
| `FileChannel.map` + `Arena.close()` | `mmap` + `munmap` 包在 `Mapping` 里 | 没有 GC 也没有 arena，释放靠析构函数 |
| `byte[]`，空环返回 `null` | `std::optional<std::vector<uint8_t>>` | 「没有」和「空」是两个不同的值，由类型保证 |
| `IllegalStateException` / `NoSuchElementException` | `StateError`（`logic_error`）/ `EmptyError`（`runtime_error`） | 标准库没有同名异常；自定义类型方便测试按类型断言 |
| `NoSuchFileException` | `std::system_error` + `errc::no_such_file_or_directory` | 系统调用失败带 `errno`，用 `error_code` 比较 |
| 有符号 `long` 计数溢出会回绕 | 必须用无符号：有符号溢出是 UB | C++ 把有符号溢出定义为未定义行为 |
| 启动子 JVM、拼 classpath | `fork()` + `pipe` + `waitpid` | 子进程直接继承地址空间；POSIX 专有 |
| `AutoCloseable` / try-with-resources | 析构函数（RAII） | 异常安全不靠 `finally`，靠对象生命周期 |
| 对象有引用语义，`LongRing` 赋值是共享 | 值语义：拷贝是独立的环 | C++ 的类默认是值；要想清楚拷贝和移动之后的状态（2.1） |

## 7. 陷阱

1. **`release` 写成 `relaxed`**：x86 碰巧能跑，ARM 读到旧值（3.2）。
2. **`head == tail` 当作「空」，而计数取模存**：既可能空也可能满（2）。
3. **有符号计数**：溢出是 UB；用 `std::uint64_t`。
4. **默认移动构造**：`mask_` 与 `buf_` 相互依赖，被移动的环越界写（2.1）。
5. **热字段挤在同一缓存行**：生产者与消费者互相拖慢（3.4）；只读字段放在热字段后面，同样会被无谓失效。
6. **把 `std::hardware_destructive_interference_size` 写进共享内存布局**：不同编译器给不同的值（3.4）。
7. **把 PAD + 记录当整体判断**：死锁（4.3）。
8. **先读 `tail` 再读 `closed`**：漏掉最后几条消息（4.4）。
9. **`atomic_ref` 的地址不对齐，或对 `std::atomic` 之外的普通访问并发**：UB / 数据竞争（4.2）。
10. **映射 / 描述符泄漏**：`attach` 抛异常时没有 RAII 就会泄漏（5.1）。
11. **先 `open(O_TRUNC)` 再校验容量**：非法参数把已有文件截断（5.1）。
12. **`fork` 在多线程程序里**：子进程只有调用 `fork` 的那个线程，其他线程持有的锁永远不会被释放（5.2）。
13. **用 `sleep` 等对方**：测试要靠带截止时间的自旋，不是猜时序。

## 8. 面试官会追问什么（senior）

**Q1. 为什么 SPSC 不需要 CAS？** 每个共享变量只有一个写者：`tail` 只有生产者写、`head` 只有消费者写。CAS 解决的是「多个写者同时改同一个值」，这里不存在。只需要可见性和顺序，release / acquire 够了。

**Q2. release / acquire 具体保护了什么？去掉会怎样？** 保护的是「数据写入先于 `tail` 的发布」和「数据读取先于 `head` 的归还」。去掉：消费者可能看到新的 `tail` 却读到槽位里上一圈的旧值；生产者可能在消费者读完之前覆盖槽位。x86 上多半碰巧不出错，ARM 上几千条消息内就会。

**Q3. `seq_cst` 和 `acq_rel` 有什么差别？** `seq_cst` 在 acquire / release 之上再要求所有线程对**所有** `seq_cst` 操作看到同一个全局顺序。代价最明显的是 x86：release 的 store 就是一条普通 `mov`，`seq_cst` 的 store 要用 `xchg`（带隐含的全屏障）；ARM 上差别小一些。SPSC 只有两个线程、两对 release / acquire，不需要全局顺序，用 release / acquire 就够。

**Q4. 什么是伪共享？怎么证明？** 3.4 的程序：两个线程各自改自己的计数器，放在同一条缓存行里慢 8 倍左右。

**Q5. cached index 为什么安全？** 下标只增不减，旧值只会让对方看起来**更慢**，所以按旧值判断「有空位 / 有数据」绝不会误判；误判只会出现在相反方向（旧值说满、实际不满），那时再读一次真实值即可。

**Q6. 改成多生产者怎么办？** `tail` 变成 CAS 竞争，或者每个生产者一个环（SPSC 的 N 份副本，消费者轮询）。后者没有竞争，通常更快。或者像 Disruptor：先 CAS 预留一段区域，写完再按序发布。

**Q7. 零拷贝怎么做？** `claim` / `commit`（Aeron）：生产者向环申请一段连续区域（`std::span<std::byte>`），直接把消息写进去，再 `commit` 发布；消费者用回调拿到环里的 `span`，回调返回后才归还。省掉两次拷贝和 `poll` 里的分配。

**Q8. 消费者崩溃重启怎么办？** `head` 在文件里，重启后 `attach` 就能继续。但「处理了一半的消息」会被重复处理：下游要幂等，或者在处理完之后才推进 `head`（at-least-once）。

**Q9. 为什么 `init` 最后才写 `magic`？** 看到 `magic` 的人通过 acquire 保证看到前面写的 `capacity` / `version`；`attach` 看不到 `magic` 就说明环还没建好，直接报 `StateError`。

**Q10. 共享内存里能放 `std::atomic` 吗？** 可以，前提是 `is_always_lock_free`，且对象在映射里被**构造**过（`new (p) std::atomic<T>`），或者用 `atomic_ref`。`std::vector`、`std::string`、指针不能放：它们的内容在各进程的地址空间里各有各的地址。

## 9. 自测

1. 容量 4 的 `LongRing`，`head = 6, tail = 10`，`size()` 是多少，下一次 `offer` 写到哪个槽位？
2. 为什么 `LongRing` 的计数要用 `std::uint64_t` 而不是 `long long`？
3. `SpscLongRing` 里，生产者为什么要读 `acquire` 的 `head`？去掉会怎样？
4. 为什么只读的 `buf_` / `mask_` 要放在最前面？
5. `std::atomic_ref<std::uint64_t>` 要求什么条件？不满足会怎样？
6. 空环，`capacity = 64`，`tail = 48`，要放 60 字节的消息。第一次 `offer` 返回什么、环里发生了什么？
7. `is_drained()` 为什么先读 `closed` 再读 `tail`？
8. `std::optional<Bytes>` 比 Java 的 `null` / `byte[0]` 好在哪里？
9. `create` 里先调用 `segment_bytes(capacity)`、后调用 `open`，顺序反过来会出什么问题？
10. `fork` 出的子进程为什么要重新 `open` 一次文件，而不是用父进程的 `SharedChannel` 对象？

<details><summary>答案</summary>

1. `size = 4`（满）；下一槽位是 `tail & 3 = 10 & 3 = 2`，但满了所以 `offer` 返回 `false`，不会写。
2. 有符号溢出是 UB（即使几乎不可能发生，编译器也可以据此优化出奇怪的结果）；无符号回绕有定义，且差值 `tail - head` 在回绕后仍然正确。
3. 为了和消费者的 `head_.store(release)` 配对：看到新 `head` 之后，消费者对该槽位的读一定已经完成，生产者覆盖它才安全。去掉（`relaxed`）会让生产者可能在消费者读完之前覆盖槽位。
4. 它们永远不变，两个线程都读。放在热字段后面，会和生产者每次写 `tail_` 失效的同一缓存行挤在一起；放在最前面单独占一行，就不会被反复失效。
5. 对象的地址按 `required_alignment` 对齐（`uint64_t` 是 8），类型必须是平凡可拷贝的；不满足是 UB。所以 `init` / `attach` 先检查 `seg.data()` 的对齐。
6. 末尾只剩 16 字节，真记录要 64 字节：先发布一条 16 字节的 PAD，`tail` 变成 64；真记录从偏移 0 开始需要 64 字节，但消费者还没读 PAD（`head` = 48），空位只有 48 字节，放不下，返回 `false`。消费者 `poll` 越过 PAD 返回 `nullopt`，`head` = 64，之后再 `offer` 才放得下。
7. 生产者先发布最后的 `tail`，再置 `closed`。先读 `closed` 看到 1，就保证后面读到的 `tail` 是最终值。反过来：先读到旧 `tail`，再看到 `closed`，会误以为已经读完。
8. `nullopt` 与「持有空 vector 的 optional」在类型层面就是两个值；`null` 与空数组靠约定区分，容易写错判断。
9. 若先 `open(O_TRUNC)`，非法容量会在抛异常之前就把已有的文件截断成空。
10. 子进程继承的是父进程地址空间的副本，其中的映射与父进程共享同一批物理页，但这样就没有测试到「另一个进程独立映射同一个文件」这个场景；重新 `open` 才模拟真实的两个独立进程（同时验证 `attach` 的校验）。

</details>

## 延伸阅读

* [std::memory_order](https://en.cppreference.com/w/cpp/atomic/memory_order)：release / acquire / seq_cst 的精确定义
* [std::atomic_ref](https://en.cppreference.com/w/cpp/atomic/atomic_ref)：对已有对象做原子访问的要求
* [std::hardware_destructive_interference_size](https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size)：缓存行常量及其可移植性问题
* [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html)：`MAP_SHARED` 与文件映射
