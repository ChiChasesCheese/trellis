# hc13 · 定长内存池（Fixed-Size Memory Pool）（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

低延迟系统（行情网关、撮合引擎）不希望在热路径上调用 `new` / `malloc`：分配器要找空闲块、可能加锁、可能向操作系统要内存，耗时**不稳定**，表现为偶发的尾延迟毛刺（tail latency）。常见做法是启动时一次性准备好 `capacity` 个等大的块，运行时只在池里「借」（allocate）和「还」（free）。

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `IndexPool` | 块 = `int` 编号；`allocate` / `free`；重复归还与非法编号检测；O(1) | 链表指针和「是否在用」放进同一个 `vector<uint32_t>` |
| 2 | `GenPool` | handle = `uint64_t`（高 32 位版本号 + 低 32 位槽位）；检测 use-after-free 与 ABA | 位运算打包、符号扩展、版本号回绕 |
| 3 | `ArenaOrderPool` | 一块对齐的内存（arena），32 字节定长记录 | 对齐、placement 构造、生命周期（关闭 / 移动后） |
| 4 | `ConcurrentPool` | 线程安全：无锁 Treiber 栈 + 带 tag 的原子 head | ABA、内存序（memory order）、并发 double-free |

共同约定：

* **池满不是错误**：`allocate()` 返回 `NONE`（`IndexPool::NONE = -1`；handle 池是全 1 的 `uint64_t`），不抛异常。
* **归还返回 `FreeResult`**：`Freed`（成功）、`DoubleFree`（这块当前不在使用中：已经还过，或 handle 已陈旧）、`Invalid`（根本不是这个池发出的编号：越界、`NONE`、全零 handle、从没发过的版本号）。不用 `bool`，因为「你重复归还」和「你传了个不属于这个池的东西」是两种不同的 bug；也不直接抛异常，因为并发里两个线程同时 `free` 同一块，输的那个是正常竞争，不是程序错误。
* 容量必须在 `[1, 1 << 28]`，否则构造函数抛 `std::invalid_argument`。
* **分配顺序**：初始依次 `0, 1, 2, …`；归还的块放在链头，所以「最后归还的最先被再分配」（LIFO，对缓存友好）。

```
IndexPool p(2);
p.allocate();    // 0
p.allocate();    // 1
p.allocate();    // NONE (-1)
p.free(0);       // Freed
p.free(0);       // DoubleFree
p.free(7);       // Invalid
p.allocate();    // 0   （LIFO）

GenPool g(1);
auto a = g.allocate();   // 0x0000'0001'0000'0000   index 0, generation 1
g.free(a);               // Freed
auto b = g.allocate();   // 0x0000'0003'0000'0000   同一槽位，generation 3
g.free(a);               // DoubleFree  （旧 handle 动不了新主人的块）
```

### 1.1 池到底省了什么

下面的程序模拟行情网关：窗口里同时有 10 万个订单在用，每来一条消息就顶掉最老的一个。A 组每条消息 `new` 一个，B 组用 `IndexPool` 的 `free` + `allocate` 复用槽位。

```cpp
// A fixed-size pool vs new / delete for objects that live a short while in a sliding window.
// The pool is a free list threaded through a vector of indices.  Build with -O2 and no sanitizers.
#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

struct Order { long long id, px; int qty, side; };

class IndexPool {
public:
    explicit IndexPool(std::uint32_t n) : next_(n), slots_(n) {
        for (std::uint32_t i = 0; i < n; ++i) next_[i] = i + 1 < n ? i + 1 : kEnd;
    }
    std::uint32_t allocate() { const auto i = head_; head_ = next_[i]; return i; }
    void free(std::uint32_t i) { next_[i] = head_; head_ = i; }
    Order& at(std::uint32_t i) { return slots_[i]; }
private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    std::vector<std::uint32_t> next_;
    std::vector<Order> slots_;
    std::uint32_t head_ = 0;
};

int main() {
    constexpr int window = 100'000, messages = 20'000'000;
    long long sink = 0;
    {
        std::vector<std::unique_ptr<Order>> live(window);
        const auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < messages; ++i) live[static_cast<std::size_t>(i % window)] = std::make_unique<Order>(Order{i, 18950 + (i & 63), 100 + (i & 7), i & 1});
        const auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        for (const auto& o : live) sink += o->qty;
        std::cout << "new / delete per message: " << ms << " ms\n";
    }
    {
        IndexPool pool(window);
        std::vector<std::uint32_t> live(window);
        for (auto& h : live) h = pool.allocate();
        const auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < messages; ++i) {
            auto& h = live[static_cast<std::size_t>(i % window)];
            pool.free(h);
            h = pool.allocate();
            pool.at(h) = Order{i, 18950 + (i & 63), 100 + (i & 7), i & 1};
        }
        const auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        for (auto h : live) sink += pool.at(h).qty;
        std::cout << "pool free / allocate:     " << ms << " ms\n";
    }
    std::cout << "(checksum " << sink << ")\n";
}
```

```text
new / delete per message: 162.879 ms
pool free / allocate:     23.4967 ms
(checksum 20700000)
```

池的好处是**稳定**（没有「偶尔很慢的一次」）和**局部性**（槽位在一个连续数组里，一条 64 字节的缓存行带进好几条记录）。代价是：用后释放（use-after-free）不再是崩溃，而是**逻辑错误**——这就是后面 Part 2 的 handle 版本号要解决的。

## 2. Part 1：`IndexPool`

### 2.1 空闲链表（free list）藏在数组里

块用 `int` 编号 `0..capacity-1` 表示。不另开一个链表结点，而是用一个 `vector<uint32_t> next_`：

* `next_[i]` = 链表里 i 后面的那个空闲块（块 i 空闲时；链表末尾是 `kEnd`）。
* `next_[i]` = `kAllocated`（块 i 正在使用时）。
* `head_` = 第一个空闲块（没有空闲块时是 `kEnd`）。

| 操作 | `head_` | `next_` | 备注 |
|---|---|---|---|
| 容量 4，刚创建 | 0 | `[1, 2, 3, END]` | |
| `allocate()` → 0 | 1 | `[ALLOC, 2, 3, END]` | |
| `allocate()` → 1 | 2 | `[ALLOC, ALLOC, 3, END]` | |
| `free(0)` | 0 | `[2, ALLOC, 3, END]` | 0 插在链头，指向 2 |
| `allocate()` → 0 | | | LIFO：刚还的先出来 |

为什么一个数组同时当「链表指针」和「是否在用」：空闲的块不需要保存别的数据，在用的块不需要链表指针，两个状态互斥。省内存，也少一次缓存未命中。`kAllocated = 0xFFFFFFFE` 不可能是合法下标（容量 ≤ 2^28）。

`allocate` / `free` 都只改头结点和一两个数组元素：**O(1)**，不扫描。构造是 O(capacity)，可以。

**重复归还不能把块插进链表两次**：`free` 先看 `next_[b] != kAllocated` → `DoubleFree`。否则同一块会被分给两个人。

### 2.2 一次无符号比较同时拒绝负数和过大

`free(int block)` 收到的是 `int`。`static_cast<std::uint32_t>(block)` 之后，`-1` 变成 `0xFFFFFFFF`（很大），`b >= next_.size()` 一次比较就把「负数」和「超出容量」都挡住了：`INT_MIN`、`INT_MAX`、`-1` 都是 `Invalid`。

### 2.3 移动之后的对象

编译器生成的移动构造函数对 `uint32_t head_` 只是**拷贝**，而 `vector` 被搬空了。被移动的池 `a` 还留着旧的 `head_`，下一次 `a.allocate()` 就会读 `next_[head_]`——对着空 vector 越界读（AddressSanitizer 会报）。所以这里手写移动：搬走之后把原对象恢复成一个**合法的空池**（`capacity() == 0`，`allocate()` 返回 `NONE`，`free(x)` 返回 `Invalid`）。拷贝是深拷贝，由默认拷贝构造给出。

### 2.4 代码（类型 + Part 1）

```cpp
#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <memory>
#include <new>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

namespace pool {

/// Result of returning a block.  Not a bool: "you freed it twice" and "this was never mine" are different bugs.
///   Freed       success
///   DoubleFree  the block is not in use right now: already returned, or the handle is stale
///   Invalid     not issued by this pool at all: out of range, NONE, all-zero handle, a generation never issued
enum class FreeResult { Freed, DoubleFree, Invalid };

/// The pool's "illegal state" error (Java: IllegalStateException): stale handle, double free through freeOrThrow, closed pool.
struct StateError : std::logic_error {
    using std::logic_error::logic_error;
};

/// 24 bytes of payload per order (the arena adds an 8-byte header per slot: 32 bytes in total).
struct Order {
    long long id, px;
    int qty, side;
    friend bool operator==(const Order&, const Order&) = default;
};
inline constexpr Order kZeroOrder{0, 0, 0, 0};

inline constexpr int kMaxCapacity = 1 << 28;

inline void check_capacity(int capacity) {
    if (capacity < 1 || capacity > kMaxCapacity) throw std::invalid_argument("capacity: " + std::to_string(capacity));
}

/// Blocks are int ids 0..capacity-1.  The free list lives INSIDE one std::vector<uint32_t>:
///   next_[i] = the next free block after i   (i is free; end of list = kEnd)
///   next_[i] = kAllocated                    (i is in use)
/// One word per block is both the list link and the "in use" flag: a free block has no use for anything else, and a block in
/// use has no use for a link.  Initially next_[i] = i + 1, so blocks come out as 0, 1, 2, ...; free() pushes on the head,
/// so the most recently freed block is allocated next (LIFO: still warm in the cache).  All operations O(1).
class IndexPool {
public:
    static constexpr int NONE = -1;
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit IndexPool(int capacity) {
        check_capacity(capacity);
        const auto n = static_cast<std::uint32_t>(capacity);
        next_.resize(n);
        for (std::uint32_t i = 0; i + 1 < n; ++i) next_[i] = i + 1;
        next_[n - 1] = kEnd;
        head_ = 0;
        available_ = n;
    }
    IndexPool(const IndexPool&) = default;
    IndexPool& operator=(const IndexPool&) = default;
    /// A moved-from pool must be a valid EMPTY pool: the defaulted move would leave head_ pointing into a vector that is gone.
    IndexPool(IndexPool&& o) noexcept : next_(std::move(o.next_)), head_(o.head_), available_(o.available_) { o.reset_empty(); }
    IndexPool& operator=(IndexPool&& o) noexcept {
        if (this != &o) {
            next_ = std::move(o.next_);
            head_ = o.head_;
            available_ = o.available_;
            o.reset_empty();
        }
        return *this;
    }

    int capacity() const { return static_cast<int>(next_.size()); }
    int available() const { return static_cast<int>(available_); }

    /// A free block, or NONE when the pool is exhausted (a full pool is a normal state, not an error).
    int allocate() {
        const std::uint32_t block = head_;
        if (block == kEnd) return NONE;
        head_ = next_[block];
        next_[block] = kAllocated;
        --available_;
        return static_cast<int>(block);
    }

    FreeResult free(int block) {
        // One unsigned comparison covers both "negative" and "too large": -1 becomes 0xFFFFFFFF.
        const auto b = static_cast<std::uint32_t>(block);
        if (b >= next_.size()) return FreeResult::Invalid;
        if (next_[b] != kAllocated) return FreeResult::DoubleFree;
        next_[b] = head_;
        head_ = b;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_allocated(int block) const {
        const auto b = static_cast<std::uint32_t>(block);
        return b < next_.size() && next_[b] == kAllocated;
    }

    /// Like free(), but failure throws: double free -> StateError, invalid block -> std::invalid_argument.
    void free_or_throw(int block) {
        switch (free(block)) {
            case FreeResult::Freed: return;
            case FreeResult::DoubleFree: throw StateError("block not allocated (double free?): " + std::to_string(block));
            case FreeResult::Invalid: throw std::invalid_argument("block out of range: " + std::to_string(block));
        }
    }

private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    static constexpr std::uint32_t kAllocated = 0xFFFFFFFEu;  // no valid index can be this large (capacity <= 2^28)

    void reset_empty() noexcept {
        next_.clear();
        head_ = kEnd;
        available_ = 0;
    }

    std::vector<std::uint32_t> next_;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};
```

`free_or_throw`：`DoubleFree` → `StateError`（C++ 里没有 `IllegalStateException`，这是自己的 `std::logic_error` 子类），`Invalid` → `std::invalid_argument`。`switch` 覆盖了 `enum class` 的全部枚举值，漏写一个编译器会警告。

**面试官的潜台词**：Part 1 做完会问「你怎么知道一个块是不是已经还过？」——不另开 `vector<bool>`，用链表数组本身的哨兵值。再问「A 还了块、B 借走了同一块、A 又还一次呢？」——Part 1 做不到：下标没有身份，A 的旧下标会把 B 的块还掉。这引出 Part 2。

## 3. Part 2：`GenPool`——带版本号的 handle

让每次「借」都发出一个**不同**的 handle：同一个槽位每次被借出，handle 里的**版本号**（generation）都变。旧 handle 的版本号和槽位当前版本号对不上，就知道它陈旧了。

```
handle = generation << 32 | index          （uint64_t，高 32 位版本号，低 32 位槽位）
gens_[i] 偶数 = 槽位空闲，奇数 = 在用；allocate 和 free 各把它 +1
handle 有效  ⇔  index < capacity  且  版本号是奇数  且  等于 gens_[index]
```

* `free` 的判定顺序：下标越界或版本号为偶数 → `Invalid`；版本号为奇数但和槽位当前版本不同 → `DoubleFree`；否则 `Freed`。
* `0` 和 `NONE`（全 1）永远无效：版本号 0 是偶数；全 1 的下标 `0xFFFFFFFF` 超出容量。
* 为什么用「奇偶」而不是「只涨」：Part 4 要用**一次 CAS** 完成「在用 → 空闲」的切换，并发重复归还只能有一个赢家。

场景（容量 1）：`a = allocate()`（generation 1）→ `free(a)`（generation 变 2）→ `b = allocate()`（generation 3，同一个槽位）→ `free(a)`：`a` 的版本号 1 ≠ 槽位当前的 3 → `DoubleFree`，`b` 安全。

### 3.1 无符号回绕是有定义的

版本号用 `std::uint32_t`：无符号加法**回绕（wraparound）是 C++ 定义好的行为**。有符号 `int` 溢出是未定义行为（UB）——Java 的 `int` 回绕是语言保证的，C++ 不是，这是移植时最容易犯的错。`2^32` 是偶数，所以回绕之后奇偶性不变：从 `0xFFFFFFFE` 起，第一次分配得到 `0xFFFFFFFF`（奇数 = 在用），归还回绕成 `0`（偶数 = 空闲），再分配得到 `1`。代价：同一个槽位被分配 `2^31` 次以后，一个极老的 handle 才可能「撞上」——实际可忽略。

### 3.2 打包与符号扩展

`index` 是 `std::uint32_t`，`generation` 是 `std::uint32_t`，都先 `static_cast<std::uint64_t>` 再移位/相或：**无符号**扩宽补零。如果 `index` 是有符号 `int`，`static_cast<std::uint64_t>(-1)` 是 `0xFFFFFFFFFFFFFFFF`——高 32 位全是 1，把版本号冲掉：

```cpp
// Packing (generation, index) into a uint64_t: widen the index as UNSIGNED, or a high bit smears over the generation.
#include <cstdint>
#include <iostream>

int main() {
    const std::uint32_t generation = 5;
    const int index = -1;  // imagine a corrupted or sentinel index

    const std::uint64_t wrong = (static_cast<std::uint64_t>(generation) << 32) | static_cast<std::uint64_t>(index);  // int -> uint64_t sign-extends
    const std::uint64_t right = (static_cast<std::uint64_t>(generation) << 32) | static_cast<std::uint32_t>(index);

    std::cout << std::hex;
    std::cout << "sign-extended: 0x" << wrong << "  generation reads back as 0x" << static_cast<std::uint32_t>(wrong >> 32) << "\n";
    std::cout << "unsigned:      0x" << right << "  generation reads back as 0x" << static_cast<std::uint32_t>(right >> 32) << "\n";
}
```

```text
sign-extended: 0xffffffffffffffff  generation reads back as 0xffffffff
unsigned:      0x5ffffffff  generation reads back as 0x5
```

### 3.3 代码

```cpp
/// Handles carry a generation, so a stale handle is recognised even after its slot has been handed to someone else.
///   handle = generation << 32 | index          (a std::uint64_t)
///   gens_[i] even = slot free, odd = slot in use; allocate and free each add 1
/// Valid <=> index < capacity && generation odd && generation == gens_[index].
/// Unsigned 32-bit generations wrap around in a DEFINED way (a signed int would be undefined behaviour); 2^32 is even, so the
/// parity rule survives the wrap.
class GenPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit GenPool(int capacity) : GenPool(capacity, 0u) {}
    /// initial_generation must be even (every slot starts free); tests use it to start close to the 32-bit wrap.
    GenPool(int capacity, std::uint32_t initial_generation) {
        check_capacity(capacity);
        if ((initial_generation & 1u) != 0) throw std::invalid_argument("initial_generation must be even");
        const auto n = static_cast<std::uint32_t>(capacity);
        gens_.assign(n, initial_generation);
        next_.resize(n);
        for (std::uint32_t i = 0; i + 1 < n; ++i) next_[i] = i + 1;
        next_[n - 1] = kEnd;
        head_ = 0;
        available_ = n;
    }

    /// Pack.  Both inputs are already unsigned 32-bit, so there is no sign extension to undo (with a signed int index,
    /// (uint64_t)index would smear 1-bits over the generation).
    static constexpr std::uint64_t handle(std::uint32_t index, std::uint32_t generation) noexcept {
        return (static_cast<std::uint64_t>(generation) << 32) | index;
    }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static constexpr std::uint32_t generation_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }

    int capacity() const { return static_cast<int>(gens_.size()); }
    int available() const { return static_cast<int>(available_); }

    std::uint64_t allocate() {
        const std::uint32_t index = head_;
        if (index == kEnd) return NONE;
        head_ = next_[index];
        const std::uint32_t g = ++gens_[index];  // even -> odd
        --available_;
        return handle(index, g);
    }

    FreeResult free(std::uint64_t h) {
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= gens_.size() || (g & 1u) == 0) return FreeResult::Invalid;
        if (gens_[index] != g) return FreeResult::DoubleFree;
        gens_[index] = g + 1;  // odd -> even
        next_[index] = head_;
        head_ = index;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_live(std::uint64_t h) const {
        const std::uint32_t index = index_of(h), g = generation_of(h);
        return index < gens_.size() && (g & 1u) == 1 && gens_[index] == g;
    }

private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    std::vector<std::uint32_t> gens_, next_;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};
```

`GenPool::handle` 等三个函数是 `constexpr` 的，所以打包规则可以用 `static_assert` 在编译期检查。

## 4. Part 3：`ArenaOrderPool`——一块对齐的内存

Java 版用 FFM 的 `Arena` / `MemorySegment` 在堆外（GC 看不到）分配一整块内存，再用 `MemoryLayout` / `VarHandle` 读写字段。C++ 没有 GC，所以「堆外」不是卖点，但这一题的核心仍然成立：**一次分配、连续布局、定长记录、字段不靠手算偏移**。C++ 的对应物：

| Java（FFM） | C++ |
|---|---|
| `Arena.allocate(bytes, 64)` | `std::aligned_alloc(64, bytes)`，用 `unique_ptr` + 自定义删除器管理 |
| `MemoryLayout.structLayout(...)` + `VarHandle` | 一个带 `alignas(32)` 的 `struct Slot`，`static_assert` 检查 `sizeof` / `offsetof` |
| 内存已清零 | 用 placement 构造（`std::uninitialized_value_construct_n`）创建并清零记录 |
| `close()`，之后访问抛异常 | `close()` 释放 arena；之后（或被移动之后）所有操作抛 `PoolClosed` |

### 4.1 记录布局与对齐

每个槽位是 32 字节：

| 偏移 | 字段 | 类型 | 说明 |
|---|---|---|---|
| 0 | `gen` | uint32 | 版本号（偶数空闲 / 奇数在用，同 GenPool） |
| 4 | `next` | uint32 | 空闲链表的下一个槽位（只在空闲时有意义） |
| 8 | `id` | int64 | `Order` 的四个字段（只在使用时有意义；`allocate` 时清零） |
| 16 | `px` | int64 | 同上 |
| 24 | `qty` | int32 | 同上 |
| 28 | `side` | int32 | 同上 |

* 把 `gen` 和 `next` 也放进槽位：空闲链表和版本号跟着数据走，没有第二个数组。
* `struct alignas(32) Slot`：每条记录 32 字节对齐，arena 起点 64 字节对齐 → **一条缓存行恰好放两条记录，没有记录跨缓存行**。
* `std::aligned_alloc(alignment, size)` 要求 `size` 是 `alignment` 的整数倍，所以容量 1（32 字节）、3（96 字节）要**向上取整**到 64 的倍数，否则是错误调用。
* `aligned_alloc` 给的是**原始字节**，里面还没有 `Slot` 对象；`std::uninitialized_value_construct_n(slots, n)` 在这些字节上用 placement new 构造对象（值初始化 = 清零）。`Slot` 是平凡可拷贝、平凡析构的，所以释放时直接 `std::free`，不需要逐个调析构函数——`static_assert` 把这个前提写在代码里。
* 释放用 `std::unique_ptr<void, FreeDeleter>`（`FreeDeleter` 调 `std::free`）：构造函数中途抛异常也不会泄漏。

```cpp
// One aligned arena, records created in it with placement construction, freed with std::free through a unique_ptr.
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <new>

struct alignas(32) Slot {
    std::uint32_t gen;
    std::uint32_t next;
    long long id, px;
    int qty, side;
};
static_assert(sizeof(Slot) == 32 && alignof(Slot) == 32);

struct FreeDeleter { void operator()(void* p) const noexcept { std::free(p); } };

int main() {
    constexpr std::size_t count = 3;                       // 3 * 32 = 96 bytes: NOT a multiple of 64
    constexpr std::size_t bytes = count * sizeof(Slot);
    constexpr std::size_t rounded = (bytes + 63) / 64 * 64;  // aligned_alloc requires size % alignment == 0
    std::cout << "requested " << bytes << " bytes, allocating " << rounded << "\n";

    std::unique_ptr<void, FreeDeleter> arena(std::aligned_alloc(64, rounded));
    if (!arena) throw std::bad_alloc();
    auto* slots = static_cast<Slot*>(arena.get());
    std::uninitialized_value_construct_n(slots, count);   // the Slot objects now exist, all fields zero

    std::cout << "arena address % 64 = " << reinterpret_cast<std::uintptr_t>(slots) % 64 << "\n";
    for (std::size_t i = 0; i < count; ++i)
        std::cout << "slot " << i << " address % 64 = " << reinterpret_cast<std::uintptr_t>(&slots[i]) % 64 << ", id = " << slots[i].id << "\n";
    // Two slots share each 64-byte cache line (offsets 0 and 32): the pair is read with one cache miss.
}
```

```text
requested 96 bytes, allocating 128
arena address % 64 = 0
slot 0 address % 64 = 0, id = 0
slot 1 address % 64 = 32, id = 0
slot 2 address % 64 = 0, id = 0
```

### 4.2 API 设计也是内存管理

提供 `put(h, id, px, qty, side)`（四个标量）而不只是 `put(h, const Order&)`；`px(h)` / `qty(h)` 读单个字段，而不总是 `get(h)` 复制整个 `Order`。热路径上调用方不需要构造任何临时对象。`get` 返回的是**拷贝**：改它不会改池里的数据。

### 4.3 生命周期：关闭、移动

* `close()` 幂等；析构函数调用它；先 `close()` 再析构不会重复 `free`（`unique_ptr::reset` 之后指针为空）。
* 被移动的池是**关闭状态**：`slots_` 被置空，之后任何操作抛 `PoolClosed`（`StateError` 的子类）；移动**前**签发的 handle 在新对象里仍然有效（槽位内存没动，只是换了主人）。
* 拷贝被删除：两个对象不能共享同一块 arena。
* 这个池不是线程安全的；把它交给另一个线程时，交接本身要有同步（`std::async` 的启动、`join`、互斥锁都算）。

### 4.4 代码

```cpp
/// The pool owns ONE aligned allocation (the "arena") holding capacity records of 32 bytes:
///     offset  0  gen   uint32   even free / odd in use (as in GenPool)
///     offset  4  next  uint32   free-list link (meaningful while free)
///     offset  8  id    int64  \.
///     offset 16  px    int64   | the Order payload (zeroed on allocate)
///     offset 24  qty   int32   |
///     offset 28  side  int32  /
/// The arena starts on a 64-byte boundary and a record is 32 bytes with 32-byte alignment, so no record straddles two cache
/// lines and two records fill exactly one.  std::aligned_alloc gives raw bytes; the records are then created in them with
/// std::uninitialized_value_construct_n (placement construction, which also zeroes them) so the objects really exist.
/// Not thread-safe; it may be handed to another thread when the hand-off itself is synchronised.
struct PoolClosed : StateError {
    using StateError::StateError;
};

class ArenaOrderPool {
public:
    static constexpr int MAX_CAPACITY = kMaxCapacity;
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr std::size_t kAlignment = 64;

    explicit ArenaOrderPool(int capacity) {
        check_capacity(capacity);
        capacity_ = static_cast<std::uint32_t>(capacity);
        bytes_ = static_cast<std::size_t>(capacity_) * sizeof(Slot);
        // std::aligned_alloc requires the size to be a multiple of the alignment.
        const std::size_t rounded = (bytes_ + kAlignment - 1) / kAlignment * kAlignment;
        void* raw = std::aligned_alloc(kAlignment, rounded);
        if (raw == nullptr) throw std::bad_alloc();
        arena_.reset(raw);  // from here on the unique_ptr frees it, whatever happens below
        slots_ = static_cast<Slot*>(raw);
        std::uninitialized_value_construct_n(slots_, capacity_);
        for (std::uint32_t i = 0; i < capacity_; ++i) slots_[i].next = i + 1 < capacity_ ? i + 1 : kEnd;
        head_ = 0;
        available_ = capacity_;
    }
    ArenaOrderPool(const ArenaOrderPool&) = delete;
    ArenaOrderPool& operator=(const ArenaOrderPool&) = delete;
    /// A moved-from pool is closed: every operation that needs the arena throws PoolClosed.
    ArenaOrderPool(ArenaOrderPool&& o) noexcept
        : arena_(std::move(o.arena_)), slots_(std::exchange(o.slots_, nullptr)), capacity_(std::exchange(o.capacity_, 0)),
          bytes_(std::exchange(o.bytes_, 0)), head_(o.head_), available_(std::exchange(o.available_, 0)) {}
    ArenaOrderPool& operator=(ArenaOrderPool&& o) noexcept {
        if (this != &o) {
            arena_ = std::move(o.arena_);
            slots_ = std::exchange(o.slots_, nullptr);
            capacity_ = std::exchange(o.capacity_, 0);
            bytes_ = std::exchange(o.bytes_, 0);
            head_ = o.head_;
            available_ = std::exchange(o.available_, 0);
        }
        return *this;
    }
    ~ArenaOrderPool() { close(); }

    int capacity() const { return static_cast<int>(capacity_); }
    int available() const { return static_cast<int>(available_); }
    /// Bytes in use by records (size_t: capacity * 32 can exceed 2^31).
    std::size_t byte_size() const { return bytes_; }
    static constexpr std::size_t record_bytes() { return sizeof(Slot); }
    /// Address of the arena (for alignment checks); 0 when closed.
    std::uintptr_t base_address() const { return reinterpret_cast<std::uintptr_t>(slots_); }

    std::uint64_t allocate() {
        require_open();
        const std::uint32_t index = head_;
        if (index == kEnd) return NONE;
        Slot& s = slots_[index];
        head_ = s.next;
        ++s.gen;  // even -> odd
        s.id = 0;  // the previous owner's data must not leak to the next one
        s.px = 0;
        s.qty = 0;
        s.side = 0;
        --available_;
        return handle(index, s.gen);
    }

    FreeResult free(std::uint64_t h) {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= capacity_ || (g & 1u) == 0) return FreeResult::Invalid;
        Slot& s = slots_[index];
        if (s.gen != g) return FreeResult::DoubleFree;
        s.gen = g + 1;  // odd -> even
        s.next = head_;
        head_ = index;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_live(std::uint64_t h) const {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        return index < capacity_ && (g & 1u) == 1 && slots_[index].gen == g;
    }

    /// Hot-path write: four stores, no object is created.
    void put(std::uint64_t h, long long id, long long px, int qty, int side) {
        Slot& s = live_slot(h);
        s.id = id;
        s.px = px;
        s.qty = qty;
        s.side = side;
    }
    void put(std::uint64_t h, const Order& o) { put(h, o.id, o.px, o.qty, o.side); }

    /// Zero-copy reads of one field.
    long long px(std::uint64_t h) const { return live_slot(h).px; }
    int qty(std::uint64_t h) const { return live_slot(h).qty; }
    /// Convenience copy of the whole payload (not for the hot path).
    Order get(std::uint64_t h) const {
        const Slot& s = live_slot(h);
        return Order{s.id, s.px, s.qty, s.side};
    }

    /// Release the arena now.  Idempotent; the destructor calls it too.
    void close() noexcept {
        arena_.reset();
        slots_ = nullptr;
        available_ = 0;
    }
    bool closed() const { return slots_ == nullptr; }

    static constexpr std::uint64_t handle(std::uint32_t index, std::uint32_t generation) noexcept { return GenPool::handle(index, generation); }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return GenPool::index_of(h); }
    static constexpr std::uint32_t generation_of(std::uint64_t h) noexcept { return GenPool::generation_of(h); }

private:
    struct alignas(32) Slot {
        std::uint32_t gen;
        std::uint32_t next;
        long long id;
        long long px;
        int qty;
        int side;
    };
    static_assert(sizeof(Slot) == 32 && alignof(Slot) == 32, "two records per 64-byte cache line, none straddling");
    static_assert(offsetof(Slot, id) == 8 && offsetof(Slot, px) == 16 && offsetof(Slot, qty) == 24 && offsetof(Slot, side) == 28);
    static_assert(std::is_trivially_copyable_v<Slot> && std::is_trivially_destructible_v<Slot>, "the arena is freed without running destructors");

    struct FreeDeleter {
        void operator()(void* p) const noexcept { std::free(p); }
    };

    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;

    void require_open() const {
        if (slots_ == nullptr) throw PoolClosed("pool is closed");
    }
    Slot& live_slot(std::uint64_t h) {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= capacity_ || (g & 1u) == 0 || slots_[index].gen != g) throw StateError("stale or invalid handle: " + std::to_string(h));
        return slots_[index];
    }
    const Slot& live_slot(std::uint64_t h) const { return const_cast<ArenaOrderPool*>(this)->live_slot(h); }

    std::unique_ptr<void, FreeDeleter> arena_;
    Slot* slots_ = nullptr;
    std::uint32_t capacity_ = 0;
    std::size_t bytes_ = 0;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};
```

## 5. Part 4：`ConcurrentPool`——无锁 Treiber 栈

### 5.1 从零推出 Treiber 栈

空闲链表就是一个栈：`push` = 还，`pop` = 借。单线程时 `head = next[head]`。多线程时要让「读 head、读 next、写 head」**原子**，又不想用锁。

**CAS（compare-and-swap）**：`compare_exchange(expected, desired)` 原子地做「如果 `head == expected` 就把 `head` 改成 `desired` 并返回 `true`；否则把当前值写回 `expected`、返回 `false`」。于是：

```cpp
pop():
  loop {
    h = head;  i = idx(h);
    if (i == EMPTY) return NONE;
    n = next[i];
    if (CAS(head, h -> n)) return i;
  }
push(i):
  loop {
    h = head;  next[i] = idx(h);
    if (CAS(head, h -> i)) return;
  }
```

失败说明别的线程动了 head，重新读、重试。没有锁：一个线程被挂起不会拖住别人——这是 **lock-free**（系统整体总有线程在前进）；不是 wait-free（单个线程可能一直失败重试）。

### 5.2 ABA 问题与 tag

线程 A 读到 `head = X`、`next[X] = Y`，然后被切走。线程 B 弹出 `X`、弹出 `Y`、再把 `X` 压回去：`head` 又是 `X`，但 `Y` 现在被 B **拿着在用**。A 醒来 `CAS(head, X → Y)`：`head` 还是 `X`，成功！`Y` 被装进空闲链表，下一次 `allocate` 把 `Y` 又发给别人——两个线程拿到同一块。

```cpp
// The ABA problem on a lock-free free list, replayed step by step on ONE thread so that the interleaving is exactly the unlucky one.
// Thread A starts a pop and is suspended; thread B pops two slots and pushes the first one back; thread A resumes.
#include <cstdint>
#include <iostream>
#include <vector>

constexpr std::uint32_t EMPTY = 0xFFFFFFFFu;

struct Stack {
    std::vector<std::uint32_t> next;
    std::uint64_t head;  // high 32 bits: tag, low 32 bits: top slot
    bool use_tag;

    static std::uint64_t pack(std::uint32_t tag, std::uint32_t index) { return (static_cast<std::uint64_t>(tag) << 32) | index; }
    std::uint32_t top() const { return static_cast<std::uint32_t>(head); }
    std::uint32_t tag() const { return static_cast<std::uint32_t>(head >> 32); }
    std::uint64_t next_head(std::uint32_t index) const { return pack(use_tag ? tag() + 1 : 0, index); }

    explicit Stack(bool tagged) : next{1, 2, EMPTY}, head(pack(0, 0)), use_tag(tagged) {}  // list: 0 -> 1 -> 2

    std::uint32_t pop() {
        const std::uint32_t i = top();
        head = next_head(next[i]);
        return i;
    }
    void push(std::uint32_t i) {
        next[i] = top();
        head = next_head(i);
    }
    // compare-and-swap, written out
    bool cas(std::uint64_t expected, std::uint64_t desired) {
        if (head != expected) return false;
        head = desired;
        return true;
    }
};

void replay(bool tagged) {
    Stack s(tagged);
    // Thread A: begins pop().  Reads head (slot 0) and next[0] (= 1).  Then it is suspended before the CAS.
    const std::uint64_t seen_head = s.head;
    const std::uint32_t a_slot = s.top(), a_below = s.next[a_slot];

    // Thread B: pop() -> slot 0, pop() -> slot 1 (B now owns both), then push(0) back.
    const std::uint32_t b0 = s.pop(), b1 = s.pop();
    s.push(b0);
    std::cout << (tagged ? "with tag   " : "without tag") << ": B owns slot " << b1 << "; free list top is slot " << s.top() << ", next[0] = " << s.next[0] << "\n";

    // Thread A resumes: CAS(head: seen -> slot a_below).  Looks unchanged if the head is only the slot number.
    const bool ok = s.cas(seen_head, Stack::pack(tagged ? s.tag() + 1 : 0, a_below));
    if (ok)
        std::cout << "   A's CAS SUCCEEDED -> head = slot " << s.top() << ", which B still owns: the next allocate hands slot " << s.top() << " out twice\n";
    else
        std::cout << "   A's CAS failed (the tag moved from " << (seen_head >> 32) << " to " << s.tag() << "): A re-reads and retries\n";
}

int main() {
    replay(false);
    replay(true);
}
```

下面是把这个交错在**一个线程**里按步骤重放的结果：

```text
without tag: B owns slot 1; free list top is slot 0, next[0] = 2
   A's CAS SUCCEEDED -> head = slot 1, which B still owns: the next allocate hands slot 1 out twice
with tag   : B owns slot 1; free list top is slot 0, next[0] = 2
   A's CAS failed (the tag moved from 0 to 3): A re-reads and retries
```

**解法：tag（版本计数）**。`head` 不只存槽位，还存一个每次成功 `push` / `pop` 都 +1 的计数：`head = tag << 32 | index`，一个 64 位原子整数。B 的三次操作把 head 从 `(t, X)` 变成 `(t+3, X)`，A 的 CAS 看到的整个 64 位值不同，失败，重读。tag 是 `uint32_t`，会回绕——需要恰好 2^32 次操作发生在 A 的两次读之间才会撞上，实际可忽略；测试里把初始 tag 设在 `0xFFFFFFF0`，在多线程竞争下跨过回绕点，验证回绕是有定义的、CAS 照常工作。

### 5.3 并发 double-free：对版本号做 CAS

两个线程同时 `free` 同一个 handle：先把槽位的版本号用 `compare_exchange_strong(g → g+1)` 从「奇（在用）」推进到「偶（空闲）」，**只有一个线程能成功**（返回 `Freed` 并负责把槽位压回链表）；另一个看到版本号已变 → `DoubleFree`。槽位只会进空闲链表一次。

### 5.4 内存序（memory order）

C++ 的原子操作默认是 `seq_cst`（最强，最慢）。我们只需要「发布」和「获取」：

| 位置 | 序 | 为什么 |
|---|---|---|
| `allocate`：读 `head_` 和 CAS | `acquire` | 与 `push` 的 `release` CAS 配对：`push` 里 `next_[i]` 的写入，对读到这个 `head` 的线程可见 |
| `free`：压回链表的 CAS | 成功 `release`，失败 `relaxed` | `release` 把前面对 `next_[i]` 的写**发布**出去；失败时只用返回的新 `h` 的数字，不读它指向的数据 |
| `next_[i]` 的读写 | `relaxed` | 读到过期值没关系：`next_[i]` 变过，`head_` 的 tag 就变过，CAS 会失败 |
| 分配后写新版本号 | `release` store | 槽位已被本线程独占；`is_live` 用 `acquire` 读 |
| 版本号的 CAS（`free`） | 成功 `acq_rel` | 既要看到前主人的写，又要把「我已归还」发布出去 |
| `in_use_` 计数 | `relaxed` | 只是统计，不用来同步别的数据 |

`compare_exchange_weak` 允许**伪失败**（没有竞争也可能返回 `false`），在循环里没关系，在 ARM（LL/SC 实现）上比 `strong` 便宜；`strong` 用在没有循环的地方（`free` 里对版本号的那一次）。

**为什么 `next_` 也要是 `std::atomic`**：`allocate` 读 `next_[i]` 的同时，另一个线程可能正把 `i` 重新压回去，写 `next_[i]`。同一内存位置、一个读一个写、没有 happens-before = **数据竞争（data race）= UB**。用 `relaxed` 原子就合法了，而且在 ARM / x86 上几乎不花钱。

### 5.5 缓存行

`head_` 和 `in_use_` 各占一条缓存行（`alignas(64)`）：所有线程都在改它们，不能和别的数据（比如 `vector` 的控制块）挤在一条缓存行里，否则别的线程读那些数据时也会被拖慢。伪共享的代价：

```cpp
// Two counters updated by two threads: in the same cache line they fight over it ("false sharing"); on separate lines they do not.
// Build with -O2 and no sanitizers.  The numbers depend on the machine; the gap is what matters.
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>

struct Shared { std::atomic<long long> a{0}, b{0}; };                     // a and b in one 16-byte neighbourhood
struct Padded { alignas(64) std::atomic<long long> a{0}; alignas(64) std::atomic<long long> b{0}; };  // 64 bytes apart

template <class T> double run(T& counters) {
    constexpr int iterations = 20'000'000;
    const auto t0 = std::chrono::steady_clock::now();
    {
        std::jthread x([&] { for (int i = 0; i < iterations; ++i) counters.a.fetch_add(1, std::memory_order_relaxed); });
        std::jthread y([&] { for (int i = 0; i < iterations; ++i) counters.b.fetch_add(1, std::memory_order_relaxed); });
    }
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    Shared s;
    Padded p;
    std::cout << "same cache line:      " << run(s) << " ms\n";
    std::cout << "separate cache lines: " << run(p) << " ms\n";
}
```

```text
same cache line:      273.92 ms
separate cache lines: 27.4313 ms
```

`in_use_` 是所有线程共同加减的一个计数器，本身就是争用热点：真实系统会按线程分片计数（Java 的 `LongAdder`）。`available()` 并发进行中是近似值，所有线程静止后是精确值。

### 5.6 代码

```cpp
/// Thread-safe pool: any thread may allocate, any thread may free.  The free list is a Treiber stack.
///
///   head_  one std::atomic<uint64_t>:  high 32 bits = tag (+1 on every successful push/pop), low 32 bits = top slot (kEmpty = none)
///   next_  next_[i] = the slot below i; std::atomic<uint32_t> too, because a popper may read next_[i] while another thread is
///          re-pushing i: with a plain uint32_t that is a data race (undefined behaviour)
///
///   push(i):  loop { h = head; next[i] = idx(h);            CAS(head, h -> (tag(h)+1, i)) }
///   pop():    loop { h = head; i = idx(h); n = next[i];     CAS(head, h -> (tag(h)+1, n)) }
///
/// Why the tag (ABA): thread A reads head = X, next[X] = Y and is suspended.  B pops X, pops Y, pushes X back.  head is X again, so
/// A's CAS(X -> Y) succeeds, but Y is in use by B: the free list now hands out Y a second time.  With the tag, B's three operations
/// moved head from (t, X) to (t+3, X) and A's CAS fails.
///
/// Handles follow GenPool.  free() first flips the slot's generation from odd g to g + 1 with a CAS: when two threads free the same
/// handle exactly one CAS wins (Freed), the other sees the generation moved (DoubleFree), and the slot enters the list once.
///
/// Memory orders:
///   * head_ load + CAS on pop: acquire.  It pairs with the release CAS of the push that made the slot visible, so the pusher's
///     store to next_[i] happens-before the popper's read of it.  (Later pops are read-modify-writes in the release sequence.)
///   * head_ CAS on push: release (publishes next_[i]); failure order relaxed, the loop just retries with the fresh value.
///   * next_ accesses: relaxed.  A stale value is harmless: if next_[i] changed, head_'s tag changed too and the CAS fails.
///   * gens_: the popper owns the slot exclusively, so it stores the new generation with release (readers acquire in is_live);
///     free's CAS is acq_rel.
class ConcurrentPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit ConcurrentPool(int capacity, std::uint32_t initial_tag = 0) : gens_(checked(capacity)), next_(gens_.size()) {
        const auto n = static_cast<std::uint32_t>(capacity);
        for (std::uint32_t i = 0; i < n; ++i) {
            gens_[i].store(0, std::memory_order_relaxed);
            next_[i].store(i + 1 < n ? i + 1 : kEmpty, std::memory_order_relaxed);
        }
        head_.store(pack(initial_tag, 0), std::memory_order_release);
    }

    int capacity() const { return static_cast<int>(gens_.size()); }
    /// Approximate while other threads are running; exact once they are quiet.
    int available() const { return capacity() - in_use_.load(std::memory_order_relaxed); }
    /// True when the tagged head compiles to a real atomic instruction rather than a hidden lock.
    static bool head_is_lock_free() { return std::atomic<std::uint64_t>::is_always_lock_free; }

    std::uint64_t allocate() {
        std::uint64_t h = head_.load(std::memory_order_acquire);
        for (;;) {
            const std::uint32_t index = index_of_head(h);
            if (index == kEmpty) return NONE;
            const std::uint32_t below = next_[index].load(std::memory_order_relaxed);
            // On failure compare_exchange_weak reloads `h` (with the failure order) and we go around again.  "Weak" may fail
            // spuriously, which is fine inside a loop and cheaper on LL/SC machines such as ARM.
            if (head_.compare_exchange_weak(h, pack(tag_of(h) + 1, below), std::memory_order_acquire, std::memory_order_acquire)) {
                const std::uint32_t g = gens_[index].load(std::memory_order_relaxed) + 1;  // we own the slot: even -> odd
                gens_[index].store(g, std::memory_order_release);
                in_use_.fetch_add(1, std::memory_order_relaxed);
                return GenPool::handle(index, g);
            }
        }
    }

    FreeResult free(std::uint64_t handle) {
        const std::uint32_t index = GenPool::index_of(handle), g = GenPool::generation_of(handle);
        if (index >= gens_.size() || (g & 1u) == 0) return FreeResult::Invalid;
        std::uint32_t expected = g;
        if (!gens_[index].compare_exchange_strong(expected, g + 1, std::memory_order_acq_rel, std::memory_order_relaxed)) return FreeResult::DoubleFree;
        in_use_.fetch_sub(1, std::memory_order_relaxed);
        std::uint64_t h = head_.load(std::memory_order_relaxed);
        for (;;) {
            next_[index].store(index_of_head(h), std::memory_order_relaxed);
            if (head_.compare_exchange_weak(h, pack(tag_of(h) + 1, index), std::memory_order_release, std::memory_order_relaxed)) return FreeResult::Freed;
        }
    }

    bool is_live(std::uint64_t handle) const {
        const std::uint32_t index = GenPool::index_of(handle), g = GenPool::generation_of(handle);
        return index < gens_.size() && (g & 1u) == 1 && gens_[index].load(std::memory_order_acquire) == g;
    }

private:
    static constexpr std::uint32_t kEmpty = 0xFFFFFFFFu;
    static constexpr std::uint64_t pack(std::uint32_t tag, std::uint32_t index) noexcept { return (static_cast<std::uint64_t>(tag) << 32) | index; }
    static constexpr std::uint32_t tag_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }
    static constexpr std::uint32_t index_of_head(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static std::size_t checked(int capacity) {
        check_capacity(capacity);
        return static_cast<std::size_t>(capacity);
    }
    static_assert(std::atomic<std::uint64_t>::is_always_lock_free && std::atomic<std::uint32_t>::is_always_lock_free);

    std::vector<std::atomic<std::uint32_t>> gens_;
    std::vector<std::atomic<std::uint32_t>> next_;
    alignas(64) std::atomic<std::uint64_t> head_{0};  // its own cache line: not shared with the vectors' control blocks
    alignas(64) std::atomic<int> in_use_{0};          // and the counter on another one
};

}  // namespace pool
```

构造时 `initial_tag` 默认 0，只是给测试用来逼近回绕点。`static_assert(std::atomic<std::uint64_t>::is_always_lock_free)`：如果这个类型在目标平台上不是真正的原子指令而是藏着一把锁，编译就失败——「无锁」在编译期被验证。

## 6. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| 堆外 `Arena` / `MemorySegment` 避开 GC | `std::aligned_alloc` + `alignas` 的 `struct` | 没有 GC，重点变成对齐、布局、生命周期 |
| `MemoryLayout` + `VarHandle` 读写字段 | 普通结构体成员 + `static_assert(offsetof)` | 编译器按布局生成访问代码 |
| `int` 版本号回绕（语言保证） | `uint32_t` 回绕（有定义）；`int` 溢出是 UB | 必须用无符号类型 |
| handle 是 `long`，要 `& 0xFFFFFFFFL` 防符号扩展 | `uint64_t`，索引/版本号都是 `uint32_t` | 无符号扩宽补零，类型本身防错 |
| `IllegalStateException` | `StateError`（`std::logic_error` 子类）、`PoolClosed` | 标准库没有同名异常 |
| `VarHandle.compareAndSet` / `getAcquire` / `setOpaque` | `std::atomic` + 显式 `std::memory_order` | 同一套 C11/C++11 内存模型，`opaque` ≈ `relaxed` |
| `next[]` 用 opaque 访问 | `vector<atomic<uint32_t>>` + `relaxed` | 普通数组元素被并发读写是数据竞争（UB） |
| `LongAdder` | 单个 `atomic<int>`（`relaxed`） | 标准库没有分片计数器；这里是争用热点 |
| 虚拟线程压测 | 多批短命的 `std::jthread` | C++ 没有虚拟线程 |
| 被移动 / 拷贝不存在 | 手写移动：被移动的池是合法的空池/关闭状态 | C++ 有值语义，必须想清楚「被移动之后」 |
| `new` 慢是因为 GC 压力 | `new` 慢是因为分配器的锁 / 碎片 / 系统调用 | 同样的目标，不同的原因 |

## 7. 陷阱

1. **重复归还把块插进链表两次**：之后同一块发给两个人（2.1）。
2. **用 `int` 表示版本号**：回绕是 UB（3.1）。
3. **打包时有符号下标符号扩展**：冲掉版本号（3.2）。
4. **有符号 `int` 直接和 `size_t` 比较**：`-1` 会被悄悄转成巨大的无符号数，碰巧挡得住，但这是靠隐式转换碰运气（还有符号比较警告）。显式 `static_cast<uint32_t>` 之后比一次，意图清楚。
5. **默认移动构造**：被移动的池带着旧的 `head_`（2.3）。
6. **`aligned_alloc` 的大小不是对齐的整数倍**（4.1）。
7. **只 `malloc` 不构造对象**就读写：对象生命周期没开始。用 placement 构造。
8. **没有清零载荷**：上一个主人的数据泄漏给下一个人。
9. **Treiber 栈没有 tag**：ABA（5.2）。
10. **`next_` 是普通数组**：并发读写是数据竞争（5.4）。
11. **内存序全写 `relaxed`**：`next_` 的值没有被发布，popper 可能读到未初始化的链接。全写 `seq_cst` 不会错，但慢——先对再快。
12. **`compare_exchange_weak` 没放进循环**：伪失败被当成真失败。
13. **tag 和 head 分成两个原子变量**：两次读之间可能被改，必须是**一个** 64 位整体。

## 8. 面试官会追问什么（senior）

**Q1. 为什么要池？** 分配器耗时不稳定（锁、碎片、系统调用）；池的 `allocate`/`free` 是常数时间、可预测，而且槽位连续，局部性好。

**Q2. C++ 里的标准做法呢？** `std::pmr`：`std::pmr::monotonic_buffer_resource`（只增长，整体释放）、`std::pmr::unsynchronized_pool_resource`（按大小分档的池，非线程安全）、`std::pmr::synchronized_pool_resource`（线程安全）；容器用 `std::pmr::vector` 等。自己写池是为了固定容量、可预测、能放进共享内存。

**Q3. placement new 和对齐？** `new (ptr) T(args)` 在已有内存上构造对象；`ptr` 必须满足 `alignof(T)`；`std::aligned_alloc` / `operator new(size, std::align_val_t)` 提供对齐内存。`alignas` 指定类型对齐；`alignas(64)` 让数据独占缓存行。

**Q4. 每线程缓存（per-thread cache）是什么？** 每个线程从全局池一次批量取 N 个块放在自己的本地列表，分配/释放先走本地（无原子操作、无争用），本地空了/满了再批量和全局池交换。吞吐能翻几十倍；丢掉的保证：块被「困」在某个线程的缓存里，其它线程可能看到池「满」而实际有空闲；`available()` 更不精确；线程退出要归还；公平性/LIFO 顺序不再成立。

**Q5. Treiber 栈的内存回收？** 这里的槽位在固定数组里，永不释放，所以没有「释放内存后还有人读」的问题（那是通用无锁结构要用 hazard pointer / epoch / RCU 解决的）；tag 只处理 ABA。

**Q6. lock-free 和 wait-free 的区别？** lock-free：系统整体总有线程在前进，单个线程可能饿死；wait-free：每个线程在有限步内完成。这里的 CAS 重试循环是 lock-free。

**Q7. `compare_exchange_weak` 和 `strong`？** weak 可能无竞争也失败，必须放循环里，某些架构上更快；strong 只在真的不相等时失败。

**Q8. 这个池能放进共享内存做 IPC 吗？** 可以：用下标（而不是指针）做链接，这正是 `IndexPool` / handle 的设计；arena 放进 `mmap` / `shm_open` 的内存，各进程把它映射到不同地址，下标仍然有效。原子变量在共享内存里要求 `is_always_lock_free`（否则可能是进程私有的锁）。

## 9. 自测

1. `IndexPool::free(-1)` 为什么返回 `Invalid`，实现里只做了一次比较？
2. 被移动的 `IndexPool` 为什么要手写移动构造？
3. `GenPool` 里版本号为什么偶数 = 空闲、奇数 = 在用？
4. `handle(index, generation)` 里如果 `index` 是 `int` 的 `-1`，会发生什么？
5. `std::aligned_alloc(64, 96)` 有什么问题？
6. 为什么 `Slot` 要有 `static_assert(std::is_trivially_destructible_v<Slot>)`？
7. Treiber 栈为什么需要 tag？tag 放在哪里？
8. `allocate` 里读 `next_[index]` 用 `relaxed`，为什么不会读到错的值而出问题？
9. `free` 的两个线程同时释放同一个 handle，怎么保证只有一个成功？

<details><summary>答案</summary>

1. `static_cast<std::uint32_t>(-1) == 0xFFFFFFFF`，不小于容量，和超出上界的情况一样被一次 `b >= size` 拒绝。
2. 默认移动对 `head_`、`available_` 只是拷贝，被移动后 `next_` 是空的而 `head_` 仍是旧值，下一次 `allocate` 读 `next_[head_]` 越界。手写移动把原对象恢复成合法的空池。
3. 这样「在用 → 空闲」是 `g → g+1`，并发版本里一次 CAS 就能完成状态切换且只有一个赢家；无符号回绕后奇偶性不变（2^32 是偶数）。
4. `static_cast<std::uint64_t>(-1)` 符号扩展成全 1，高 32 位（版本号）被冲成全 1，handle 面目全非。应该用无符号 32 位的下标。
5. `aligned_alloc` 要求 size 是 alignment 的整数倍（96 不是 64 的倍数），行为不合规；要向上取整到 128。
6. arena 是用 `std::free` 释放的，不会逐个调用析构函数；这只有在对象是平凡析构时才合法。
7. ABA：head 被改回原值但中间状态已变（弹出、再压回），CAS 误以为没变。tag 与槽位一起放进同一个 64 位原子整数，每次成功操作 +1，整体值不会「回到原样」。
8. 读到过期值意味着 `next_[index]` 在这期间被改过，而改它的操作（`push`）同时改了 `head_` 的 tag，CAS 会失败并重试；所以错值永远不会被安装。
9. 先对槽位版本号做 `compare_exchange_strong(g → g+1)`：只有一个线程从 `g` 推到 `g+1`，另一个看到版本号已不是 `g` → `DoubleFree`；成功者再把槽位压回链表，所以槽位只入链表一次。
</details>

**练习**：把 `ConcurrentPool` 改成每线程缓存 + 批量补货，量一量吞吐，再说清楚丢掉了哪些保证。
