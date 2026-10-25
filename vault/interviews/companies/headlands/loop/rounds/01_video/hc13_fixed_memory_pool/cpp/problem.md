# hc13 · 定长内存池（C++20 版）

低延迟系统（行情网关、撮合引擎）不愿意在热路径上调用 `new` / `malloc`：分配器要找空闲块、可能加锁、可能向操作系统要内存，耗时不稳定，表现为偶发的尾延迟毛刺。常见做法是启动时一次性准备好 `capacity` 个等大的块，运行时只在池里「借」（allocate）和「还」（free）。你要写四个池，一层比一层难：整数编号的池、带版本号的 handle、一块对齐的内存、线程安全的无锁池。C++ 版的追问都落在内存上：未初始化的对象、对齐、移动之后的对象、数据竞争（data race）。签名都在 `starter.hpp`（命名空间 `pool`）。

## 读题前你需要知道

- **空闲链表**（free list）：把没被借走的块串成一条链，借 = 摘链头，还 = 插链头，都是 O(1)。这里的链不用指针，用下标：`next[i]` 存「i 之后的下一个空闲块」。
- **CAS**（compare-and-swap）：`compare_exchange(x, expected, new)` 原子地「当 x 仍等于 expected 才写入 new」，失败时把 x 的当前值回写给 `expected`。
- **ABA 问题**：x 从 A 变成 B 又变回 A，CAS 看不出中间发生过变化而误判成功。常见解法是给值附一个每次修改都递增的版本号（tag）。
- **对齐**（alignment）：`alignof(T)` 是 T 允许放置的地址间隔；缓存行（cache line）是 64 字节，连续排布的记录一次读入就带进好几条。
- **placement 构造**：`new (ptr) T(...)` 在已有的原始内存上创建对象。只 `malloc` 不构造就读写，对象的生命周期还没开始。
- **有符号溢出是 UB，无符号回绕有定义**：版本号、tag 一律用无符号类型。

## 公共类型（starter 已给出）

```cpp
enum class FreeResult { Freed, DoubleFree, Invalid };
struct StateError : std::logic_error { using std::logic_error::logic_error; };  // 陈旧 handle、已关闭的池

struct Order {                       // 24 字节载荷
    long long id, px;
    int qty, side;
    friend bool operator==(const Order&, const Order&) = default;
};
inline constexpr Order kZeroOrder{0, 0, 0, 0};
inline constexpr int kMaxCapacity = 1 << 28;
inline void check_capacity(int capacity);   // 越界抛 std::invalid_argument
```

共同约定：

- **池满不是错误**：`allocate()` 返回 `NONE`，不抛异常。`IndexPool::NONE = -1`；handle 池的 `NONE` 是全 1 的 `uint64_t`（`~0ull`）。
- **归还返回 `FreeResult`**：`Freed` 成功；`DoubleFree` 这块当前不在使用中（已经还过，或 handle 已陈旧）；`Invalid` 根本不是这个池发出的编号（越界、`NONE`、全零 handle、从没发过的版本号）。
- 容量必须在 `[1, 1 << 28]`，否则构造函数抛 `std::invalid_argument`。
- **分配顺序**：先依次 `0, 1, 2, …`；归还的块插在链头，所以最后归还的最先被再分配（LIFO）。测试靠这条约定做确定性断言。

## Part 1 · `IndexPool`：int 编号 + 空闲链表

| 签名 | 要求 |
|---|---|
| `explicit IndexPool(int capacity)` | 容量越界抛 `std::invalid_argument` |
| `int capacity() const` · `int available() const` | 总块数 · 当前空闲块数 |
| `int allocate()` | 先 `0, 1, 2, …`，再 LIFO；池满返回 `NONE` |
| `FreeResult free(int block)` | 越界（含负数）→ `Invalid`；不在用 → `DoubleFree`；否则 `Freed` |
| `bool is_allocated(int block) const` | 越界返回 `false` |
| `void free_or_throw(int block)` | `DoubleFree` 抛 `StateError`，`Invalid` 抛 `std::invalid_argument` |

- 提示（starter 已给）：一个 `std::vector<std::uint32_t>` 同时装链接和「在用」标记（用一个哨兵值）；负数转成 `uint32_t` 会变成很大的数，一次无符号比较就能同时挡住两端；默认的移动构造会让被移动的池带着旧的链头。
- `IndexPool p(3)`：`allocate()` 依次得 `0, 1, 2`，之后一直是 `NONE`；`free(1)`、`free(3)` 之后再 `allocate()` 先得 3 再得 1（容量 4 的池）。
- `free(a)` 两次：第二次是 `DoubleFree`，`available()` 不能超过容量。从没借过的块 `free(1)` 也是 `DoubleFree`。
- 连续 `free(b)` 三次之后，`b` 只能被发出去一次，不能进链表三次。
- `free(-1)`、`free(-2)`、`free(INT_MAX)`、`free(INT_MIN)` 都是 `Invalid`。
- 记录局限的测试：容量 1 的池里，`a` 还掉块再由 `b` 借到，`a == b`，旧的 `a` 还能把 `b` 的块释放掉。下标没有身份，这是 Part 2 要补的洞，不用在这里修。
- 近满换块：65536 块的池填满后，随机换块 150 万次要在 2 秒内完成，所以不能用线性扫描找空闲块；随机 300 万次借还也要在 2 秒内。
- C++ 专属测试：被移动的池是合法的空池（`capacity() == 0`，`allocate()` 返回 `NONE`，`free(0)` 返回 `Invalid`），移动构造和移动赋值都要；拷贝是深拷贝，在副本里还块不影响原池；`-1` 转成 `uint32_t` 得到 `0xFFFFFFFF`，`-2` 得到 `0xFFFFFFFE`，都不能和你自己的哨兵混淆。

## Part 2 · `GenPool`：带版本号的 handle

| 签名 | 要求 |
|---|---|
| `explicit GenPool(int capacity)` · `GenPool(int capacity, std::uint32_t initial_generation)` | 初始版本号必须是偶数，否则抛 `std::invalid_argument` |
| `static constexpr uint64_t handle(uint32_t index, uint32_t generation)` · `index_of(h)` · `generation_of(h)` | **已给出**：`generation << 32 \| index` 的打包与拆包 |
| `std::uint64_t allocate()` | 池满返回 `NONE` |
| `FreeResult free(std::uint64_t h)` | 下标越界或版本号为偶数 → `Invalid`；版本号为奇数但和槽位当前的不同 → `DoubleFree`；否则 `Freed` |
| `bool is_live(std::uint64_t h) const` | 下标合法、版本号为奇数、且等于槽位当前版本号 |

规则：每个槽位一个 `uint32_t` 版本号，起始都等于 `initial_generation`；偶数 = 空闲，奇数 = 在用；借和还各加 1。

- `GenPool p(3)`：三次 `allocate()` 依次得 `handle(0,1)`、`handle(1,1)`、`handle(2,1)`，第四次 `NONE`。
- `GenPool(1)`：`allocate` 得 `0x1'0000'0000`，`free` 之后再 `allocate` 得 `0x3'0000'0000`（同一槽位，版本号 +2）；用旧 handle 再 `free` 是 `DoubleFree`，且 `is_live(新)` 仍为真。
- `Invalid` 的 handle：`0`、`~0ull`、`1`（版本号 0）、`0x0000'0002'0000'0000`（版本号 2，偶数）、`0x0000'0001'0000'0003`（下标 3 越界）、`0x0000'0001'FFFF'FFFF`、`0x0000'0001'8000'0000`（下标最高位为 1）。
- 回绕：`GenPool(1, 0xFFFFFFFE)`：第一次借得到版本号 `0xFFFFFFFF`（奇，在用），归还后回绕成 0（偶，空闲），下一次借得到 1。旧 handle 仍是 `DoubleFree`。`GenPool(1, 1)` 抛 `invalid_argument`，`GenPool(2, 0xFFFFFFFF)` 也抛，`GenPool(2, 0)` 和 `GenPool(2, 0xFFFFFFFE)` 不抛。
- 近满换块 150 万次、随机 300 万次借还（夹杂对已死 handle 的探测，必须一直被拒绝）都要在 2 秒内完成。
- C++ 专属测试：`handle` 是 `constexpr`，`handle(0xFFFFFFFF, 0)` 的版本号仍是 0（下标最高位不能蔓延到版本号）；从 `0xFFFFFFFC` 起借还 8 轮，最后一轮的版本号是 `0xFFFFFFFC + 2·7 + 1` 回绕后的值（`0xB`），整个过程在 UBSan 下不能终止。

## Part 3 · `ArenaOrderPool`：一块对齐的内存

一块 `std::aligned_alloc` 出来的内存（arena），64 字节对齐，里面是 `capacity` 条 32 字节的记录（`alignas(32)`）：`gen:uint32 · next:uint32 · id:int64 · px:int64 · qty:int32 · side:int32`。句柄和 `free` 的规则同 `GenPool`。

| 签名 | 要求 |
|---|---|
| `explicit ArenaOrderPool(int capacity)` | 容量越界抛 `std::invalid_argument`；不可拷贝，可移动 |
| `int capacity()` · `available()` · `std::size_t byte_size()` · `static constexpr record_bytes()` · `std::uintptr_t base_address()` | `byte_size() == capacity * 32`；`base_address()` 关闭后为 0 |
| `std::uint64_t allocate()` · `FreeResult free(h)` · `bool is_live(h)` | 同 `GenPool`；`allocate` 把载荷清零 |
| `void put(h, long long id, long long px, int qty, int side)` · `void put(h, const Order&)` | 热路径：四次写入，不创建对象；陈旧或非法 handle 抛 `StateError` |
| `long long px(h)` · `int qty(h)` · `Order get(h)` | 读一个字段 · 读整条记录（返回副本）；陈旧或非法 handle 抛 `StateError` |
| `void close() noexcept` · `bool closed() const` | 幂等；析构也调用它 |

- 提示（starter 已给）：arena 用带 `std::free` 删除器的 `unique_ptr` 持有；记录用 `std::uninitialized_value_construct_n` 在原始字节上创建。
- 关闭之后（或被移动之后），除了 `capacity()` / `available()` / `byte_size()` 以外的所有操作抛 `PoolClosed`（`StateError` 的子类）。
- `put(h, Order{...})` 之后 `get(h)` 逐字段相等，包括极值：`Order{LLONG_MIN, LLONG_MAX, INT_MIN, INT_MAX}` 和全 `-1`。
- 1000 条记录各写 `Order{i, -i, 3i, i%2}`，读回来互不覆盖；第 1001 次 `allocate` 是 `NONE`。
- 复用的记录要清零：`put` 之后 `free` 再 `allocate`，`get` 得到 `kZeroOrder`。
- 旧 handle `a` 在槽位被复用后 `get(a)` 抛 `StateError`，`free(a)` 是 `DoubleFree`，新主人的数据不受影响；`NONE`、`0`、`1`、`0x1'0000'0063` 都是 `Invalid`（`free`）并让 `get` 抛 `StateError`。
- 容量 1000：`byte_size() == 32'000`。100 万条记录的借、写、读、随机还 20 万次，要在 2 秒内完成。
- C++ 专属测试：
  - 对齐：`base_address() % 64 == 0`，第 5 条记录的地址是 32 的倍数。
  - 容量 1、3、5、7（32、96、160、224 字节）都要能用：`aligned_alloc` 要求大小是对齐值的整数倍，ASan 会抓写越界。
  - `byte_size()` 的类型是 `std::size_t`：7000 万条记录是 2'240'000'000 字节，超过 `int` 的上限。
  - 移动之后：旧对象 `closed()`，`allocate` 抛 `PoolClosed`；新对象继续认旧 handle；移动赋值要释放自己原来的 arena。`ArenaOrderPool` 不可拷贝，移动构造是 `noexcept`。
  - `close()` 之后再析构，arena 只能被释放一次（ASan 会抓 double free）。
  - `get` 返回的是副本，改副本不影响池里的记录。
  - 另一线程在同步的交接（`std::async`）之后可以使用池。

## Part 4 · `ConcurrentPool`：无锁 Treiber 栈

| 签名 | 要求 |
|---|---|
| `explicit ConcurrentPool(int capacity, std::uint32_t initial_tag = 0)` | `initial_tag` 让测试把 tag 放在 `2^32` 附近 |
| `std::uint64_t allocate()` · `FreeResult free(h)` · `bool is_live(h) const` · `int available() const` | 顺序行为同 `GenPool`（包括 LIFO）；`available()` 在线程运行中可以是近似值，安静时必须精确 |
| `static bool head_is_lock_free()` | **已给出** |

- 空闲链表是 Treiber 栈：**一个** `std::atomic<std::uint64_t>` 的 head（高 32 位 tag，每次成功的压栈 / 弹栈加 1；低 32 位栈顶槽位，`0xFFFFFFFF` = 空），用 `compare_exchange_weak` 更新，不用 mutex。
- 链接 `next` 用 `std::atomic<std::uint32_t>`（`relaxed`）：弹栈的线程读 `next[i]` 时，别的线程可能正在把 `i` 压回去，普通的 `uint32_t` 是数据竞争。内存序要显式写：读 / 弹 head 用 acquire，压栈用 release，链接用 relaxed。
- `free` 先用 `compare_exchange_strong` 把槽位版本号从 `g` 推到 `g+1`，再压栈：两个线程同时释放同一个 handle，恰好一个返回 `Freed`，另一个 `DoubleFree`。
- 顺序测试：`ConcurrentPool(3)` 依次得 `H(0,1)`、`H(1,1)`、`H(2,1)`，还掉 `b` 再借，得到下标 1、版本号 3；`free(H(3,1))` 和 `free(H(1,4))` 是 `Invalid`。
- 容量 3 的池，8 个线程各借还 8000 次，任何时刻一个槽位不能有两个主人（测试 12 轮）；跑完后恰好能借出 3 个不同的槽位，第 4 个是 `NONE`。
- 3 个线程对同一批 2000 个 handle 各 `free` 一遍：`Freed` 恰好 2000 次，`DoubleFree` 恰好 4000 次，`Invalid` 0 次，且没有槽位进链表两次。
- 3 个生产者借、3 个消费者还（容量 64，每个生产者 8000 次，经一个 mutex 队列交接）：所有 handle 都是 `Freed`。
- 400 个短命线程（每批 50 个，`std::jthread`）各做 200 轮借还，容量 16。
- 性能：4 个线程各 5 万轮、每轮借 16 个再还 16 个，容量 1024，要在 2 秒内完成，最后 `available() == 1024`。
- C++ 专属测试：
  - `std::atomic<std::uint64_t>` 是 always lock-free，`head_is_lock_free()` 为真。
  - tag 从 `0xFFFFFFF0` 起步，在 6 个线程的争用下越过 `2^32` 很多次，仍然没有违规（tag 的运算必须是无符号）。
  - 单线程做 2 万轮「借满再倒序还」（容量 5），伪失败（spurious failure）不能影响结果。
  - 一个线程反复 `free` 一个死 handle，另一个线程循环借还同一个槽位 2 万次：死 handle 绝不能释放新主人的块。

## 边界清单

- 容量：`0`、`-1`、`INT_MIN`、`(1<<28)+1`、`INT_MAX`、`1`
- 块编号：`-1`、`-2`、`INT_MIN`、`INT_MAX`、等于容量、重复归还、从没借过
- handle：`0`、`~0ull`、偶数版本号、下标越界、下标最高位为 1、版本号 `0xFFFFFFFF`、`0x80000000`
- 版本号回绕、初始版本号为奇数
- 容量不是 64 字节整数倍的 arena（容量 1、3、5、7）、关闭后再析构、移动后再用
- 池满后继续 `allocate`；近满池的 150 万次换块
- 并发：同一 handle 并发 `free`、跨线程借和还、tag 回绕

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc13_fixed_memory_pool          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc13_fixed_memory_pool --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc13_fixed_memory_pool --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc13_fixed_memory_pool --tag conc     # 并发测试
python3 tools/cpptest.py run   loop/rounds/01_video/hc13_fixed_memory_pool                # 全部
```

编译带 `-fsanitize=address,undefined -fno-sanitize-recover=undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 「池满了怎么办」：返回 `NONE` 让调用方决定（丢弃 / 告警 / 背压），或者阻塞，或者扩容但打破固定容量。
- 「每线程缓存」：每个线程一次从全局池批量取一批块，本地借还没有争用；代价是块可能被困在某个线程里，`available()` 更不精确。
- 「放进共享内存」：链接用下标而不是指针，各进程把 arena 映射到不同地址仍然有效。
