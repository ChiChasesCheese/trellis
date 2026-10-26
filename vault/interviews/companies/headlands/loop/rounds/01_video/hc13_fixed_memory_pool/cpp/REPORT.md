# hc13 · 思路与追问（C++20 版）

定长内存池的代码不长，分数在追问里：面试官每问一句，就是在看你对 C++ 的某一层有没有概念，包括未初始化的对象、对齐、移动之后的对象、数据竞争和内存序。下面按 Part 写清三件事：怎么写、面试官在探什么、该说出口的那句话。详细的推导和可运行的示例在讲义 [[interviews/companies/headlands/loop/rounds/01_video/hc13_fixed_memory_pool/cpp/problem|C++ 题面]]。

## 30 秒版本

- **空闲链表藏在数组里**：`std::vector<uint32_t>` 的一个字同时是「下一个空闲块」和「在用」标记，借还都是 O(1)，重复归还靠哨兵值识别。
- **handle = 版本号 + 下标**：`generation << 32 | index`，偶数空闲、奇数在用，借还各加 1。旧 handle 动不了新主人的块。
- **版本号用 `uint32_t`**：无符号回绕有定义，有符号溢出是 UB；2^32 是偶数，回绕后奇偶性不变。
- **arena**：一次 `aligned_alloc`（大小要向上取整到对齐值的倍数），用 placement 构造创建记录，`unique_ptr` + `std::free` 管生命周期。
- **无锁**：Treiber 栈，tag 和栈顶塞进**同一个** 64 位原子数，`compare_exchange_weak` 放进循环；`free` 先对版本号做 CAS 选出唯一赢家。
- **池的价值是可预测的延迟，不是吞吐**；池满返回 `NONE`，由调用方决定怎么办。

## Part 1 · `IndexPool`

**写法**

```cpp
FreeResult free(int block) {
    const auto b = static_cast<std::uint32_t>(block);   // -1 变成 0xFFFFFFFF
    if (b >= next_.size()) return FreeResult::Invalid;  // 一次比较挡住两端
    if (next_[b] != kAllocated) return FreeResult::DoubleFree;
    next_[b] = head_; head_ = b; ++available_;
    return FreeResult::Freed;
}
```

初始 `next_[i] = i + 1`，最后一个是 `kEnd`；`allocate` 摘链头并把 `next_[block]` 写成 `kAllocated`。两个哨兵（`0xFFFFFFFF`、`0xFFFFFFFE`）都比最大容量 2^28 大，不会和真实下标冲突。移动构造要手写：搬走 `next_` 之后把对方重置成空池。

**面试官在探什么**

1. **O(1) 怎么来的**：不扫描找空闲块，链头永远就是下一个空闲块。近满池随机换块 150 万次，扫描版会慢得多，随机 50/50 负载却测不出来。
2. **重复归还**：不检查状态就插链头，同一块会进链表两次，之后被发给两个人。`next_[b]` 里放「在用」哨兵，检查不需要另开数组。
3. **`-1` 为什么能被一次比较挡住**：`static_cast<uint32_t>(-1)` 是 `0xFFFFFFFF`，大于等于容量。要能说出这是显式转换后的无符号比较，不是靠隐式转换碰运气。
4. **被移动的池**：默认移动对 `head_` 只是拷贝，`next_` 却空了，下一次 `allocate` 读 `next_[head_]` 越界。手写移动，让对方成为合法的空池。
5. **局限**：下标没有身份。`a` 还掉块，`b` 借到同一块，`a` 的旧副本还能把 `b` 的块还掉。这就是 Part 2 的动机。

**该说出口的话**：「链接和在用标记放在同一个数组里，借还都是 O(1)；重复归还靠哨兵识别，所以一个块不会进链表两次。」

## Part 2 · `GenPool`

**写法**：`allocate` 取链头，`++gens_[index]`（偶 → 奇），返回 `handle(index, g)`。`free` 的判定顺序：

```cpp
if (index >= gens_.size() || (g & 1u) == 0) return FreeResult::Invalid;  // 没发过
if (gens_[index] != g) return FreeResult::DoubleFree;                    // 发过，但已经陈旧
gens_[index] = g + 1;                                                    // 奇 → 偶
```

**面试官在探什么**

1. **为什么偶数 = 空闲、奇数 = 在用**：版本号本身就是状态位，不需要另一个数组；并发版本里「检查 + 切换状态」可以合成一次 CAS。
2. **回绕**：`uint32_t` 回绕有定义；换成 `int`，`g + 1` 在 `INT_MAX` 上是 UB，UBSan 会直接终止。2^32 是偶数，所以回绕后奇偶性不变。要能说出残余风险：同一个槽位被借还 2^31 次之后，旧 handle 才可能碰巧撞上，真要防就退役这个槽位。
3. **符号扩展**：`handle` 的参数是 `uint32_t`。如果下标是 `int` 的 `-1`，`static_cast<uint64_t>(-1)` 是全 1，高 32 位的版本号会被冲掉；类型本身就是防线。
4. **`Invalid` 和 `DoubleFree` 的区别**：偶数版本号、下标越界是「根本没发过」；奇数版本号但和槽位当前不同是「发过，已陈旧」。`0` 和 `~0ull` 自动落在 `Invalid` 里。
5. **`initial_generation` 为什么必须是偶数**：奇数意味着所有槽位一开始就是「在用」，状态和链表对不上。

**该说出口的话**：「handle 带版本号，槽位每次归还版本号都变，旧 handle 一比就知道陈旧；版本号用无符号数，回绕有定义。」

## Part 3 · `ArenaOrderPool`

**写法**：

```cpp
struct alignas(32) Slot { std::uint32_t gen, next; long long id, px; int qty, side; };
static_assert(sizeof(Slot) == 32 && alignof(Slot) == 32);
static_assert(std::is_trivially_destructible_v<Slot>);   // arena 用 std::free 释放，不跑析构函数
```

构造：按 64 取整字节数 → `std::aligned_alloc(64, rounded)` → 立刻放进 `unique_ptr<void, FreeDeleter>`（后面任何一步抛异常都不会泄漏）→ `std::uninitialized_value_construct_n` 创建并清零记录 → 串起空闲链表。

**面试官在探什么**

1. **为什么 32 字节、32 对齐**：64 字节的缓存行正好放两条，没有一条跨行；arena 本身 64 字节对齐，才保证这一点。
2. **`aligned_alloc` 的大小**：要求大小是对齐值的整数倍。容量 3 是 96 字节，不是 64 的倍数，要取整到 128，否则行为不合规。取整只用于分配，`byte_size()` 仍然返回 `capacity * 32`。
3. **placement 构造**：只 `malloc` 不构造就读写，对象的生命周期还没开始，严格说是 UB。`uninitialized_value_construct_n` 既创建对象又清零。
4. **`static_assert(is_trivially_destructible)`**：arena 整块 `free`，不会逐个调析构；这只有在记录是平凡析构时才合法。
5. **`byte_size()` 返回 `size_t`**：`capacity * 32` 在约 6700 万条记录时就超过 `int`（2^31 / 32 = 2^26 = 67 108 864）；上限 2^28 条是 8 589 934 592 字节，连 32 位无符号数都放不下。
6. **生命周期**：不可拷贝（拷贝一块独占内存没有意义），可移动。被移动的对象变成已关闭状态，所有访问抛 `PoolClosed`。`close()` 是幂等的，析构也调用它，arena 只能释放一次，否则 ASan 报 double free。
7. **热路径**：`put(h, id, px, qty, side)` 是四次写入，不创建对象；`get` 返回副本，不要在热路径用。每个访问先检查 handle 是否陈旧，陈旧抛 `StateError`，不会读到新主人的数据。
8. **清零**：`allocate` 时清零载荷，否则上一个主人的数据泄漏给下一个人。

**该说出口的话**：「一块 64 字节对齐的内存放定长记录，用 placement 构造创建对象，`unique_ptr` 管释放；记录是平凡类型，所以整块 `free` 是合法的。」

## Part 4 · `ConcurrentPool`

**写法**

```cpp
// allocate：弹栈
std::uint64_t h = head_.load(std::memory_order_acquire);
for (;;) {
    const auto i = index_of_head(h);
    if (i == kEmpty) return NONE;
    const auto below = next_[i].load(std::memory_order_relaxed);
    if (head_.compare_exchange_weak(h, pack(tag_of(h) + 1, below),
                                    std::memory_order_acquire, std::memory_order_acquire)) break;
}
```

`free`：先 `gens_[i].compare_exchange_strong(g, g + 1)`，输了就是 `DoubleFree`；赢了再压栈（release）。

**面试官在探什么**

1. **ABA**：线程 1 读到 head = A、next[A] = B 后被挂起；线程 2 弹 A、弹 B、再压 A；线程 1 的 CAS 看到 head 还是 A，成功，把已经在用的 B 装回栈顶，B 被发给两个人。tag 每次成功操作加 1，整个 64 位值不会回到原样。
2. **tag 为什么必须和栈顶在同一个原子数里**：分成两个原子变量，两次读之间可能被改。所以要 `is_always_lock_free` 的 64 位原子，测试里用 `static_assert` 守着。
3. **tag 会回绕**：`uint32_t` 回绕有定义，要 2^32 次操作；测试把初始 tag 设在 `0xFFFFFFF0`，在争用下越过很多次。
4. **`next_` 为什么也是 `atomic`**：弹栈的线程读 `next_[i]`，同时别的线程可能在把 `i` 压回去并写 `next_[i]`。同一位置一读一写、没有 happens-before，就是数据竞争（UB）。`relaxed` 够用：读到过期值，说明 head 的 tag 也变过，CAS 会失败。
5. **内存序**：读 / 弹 head 用 acquire，与压栈的 release 配对，保证压栈者对 `next_[i]` 的写先于弹栈者的读；`next_` 用 relaxed；`in_use_` 只是计数，relaxed。全写 `seq_cst` 不会错但慢，全写 `relaxed` 会错（`next_` 的值没被发布）。
6. **`weak` 与 `strong`**：`weak` 没有竞争也可能失败，必须放循环里，在 ARM 上更便宜；`free` 里对版本号的那一次没有循环，用 `strong`。
7. **并发 double-free**：对版本号做 CAS，只有一个线程能从 `g` 推到 `g+1`，所以槽位只进链表一次。
8. **lock-free 不等于更快**：8 个线程抢同一个 head，每个 CAS 都可能失败重试，一把锁未必更慢。说「要量」，不要断言。要更快就用每线程缓存：批量取、本地借还；代价是块可能被困在某个线程里，`available()` 更不精确，线程退出要归还，LIFO 顺序不再成立。
9. **内存回收**：槽位在固定数组里，永远不释放，所以没有「释放了还有人在读」的问题（那是通用无锁结构要用 hazard pointer 或 epoch 解决的）。
10. **缓存行**：`head_` 和 `in_use_` 各占一条缓存行（`alignas(64)`），所有线程都在改它们，不能和别的数据挤在一起。
11. **lock-free 与 wait-free**：CAS 重试循环是 lock-free（系统整体总有线程前进，单个线程可能饿死），不是 wait-free。

**该说出口的话**：「tag 和栈顶放在同一个 64 位原子里，每次成功操作加 1，所以 ABA 的 CAS 会失败；`free` 先对版本号做 CAS，并发的重复归还只会有一个赢家。」

## C++ 专属陷阱

- 默认移动构造让被移动的池带着旧链头（Part 1），被移动的 arena 要变成已关闭状态（Part 3）。
- 版本号、tag 用有符号类型：回绕是 UB。
- 打包 handle 时下标是有符号数：符号扩展冲掉版本号。
- `aligned_alloc` 的大小不是对齐值的倍数；只分配不构造对象；arena 的删除器和分配函数不配对。
- `compare_exchange_weak` 没放进循环，伪失败被当成真失败。
- 链接数组用普通整数：并发读写是数据竞争。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 为什么要池 | 减轻 GC 压力、削掉停顿造成的尾延迟 | 分配器耗时不稳定（锁、碎片、系统调用），池的借还是常数时间 |
| 堆外内存 | `Arena` / `MemorySegment` + `MemoryLayout` | `aligned_alloc` + `alignas` 结构体，`static_assert(offsetof)` 守布局 |
| 版本号 | `int` 回绕有定义 | 必须 `uint32_t`；`int` 溢出是 UB |
| handle 打包 | `long`，要 `& 0xFFFFFFFFL` 防符号扩展 | `uint64_t`，两个 `uint32_t` 拼起来，类型本身防错 |
| 非法状态异常 | `IllegalStateException` | 自定义 `StateError`（`std::logic_error` 子类）和 `PoolClosed` |
| CAS | `VarHandle.compareAndSet` / `getAcquire` / `setOpaque` | `std::atomic` + 显式 `std::memory_order`；opaque 约等于 relaxed |
| 链接数组并发读写 | opaque 访问 | `vector<atomic<uint32_t>>` + relaxed；普通数组是数据竞争 |
| 计数 | `LongAdder` | 单个 `atomic<int>`（relaxed）；标准库没有分片计数器 |
| 大量短任务 | 虚拟线程 | 没有虚拟线程，用多批短命的 `std::jthread` |
| 对象被移动 / 拷贝 | 不存在这个问题 | 必须规定被移动之后是什么状态 |
