# C13 · 内存模型、`std::atomic`、`memory_order`、无锁基础、伪共享

> 目标：说清为什么多线程下普通变量不可靠、`atomic` 做什么、acquire/release 在保证什么、怎样写一个无锁 SPSC 队列、什么是伪共享。

## 1. Java 对照

Java 内存模型（JMM）用 `volatile`、`synchronized`、`final` 定义可见性和有序性（happens-before）；`java.util.concurrent.atomic` 提供 CAS。
C++11 起有同样严格的内存模型：`std::atomic<T>` 的每个操作可以指定 `memory_order`，默认 `seq_cst` 最强（类似 Java `volatile` 的语义），你可以按需放松换取性能。**C++ 的 `volatile` 不是线程同步工具**（它只阻止编译器优化掉访问），不要用它代替 `atomic`。

## 2. 为什么普通变量不行

三个原因让"线程 A 写、线程 B 读"不可靠：

1. **编译器重排/缓存到寄存器**：没有同步，编译器可以把循环里读取的变量提到循环外。
2. **CPU 乱序与存储缓冲**：写入先进核心私有的存储缓冲，别的核心稍后才看到；不同核心看到不同顺序。
3. **撕裂**：多字节值可能被拆成多次访存。

标准规定：两个线程无同步地访问同一内存且至少一个写 = **数据竞争 = 未定义行为（UB）**。同步手段只有：`mutex`、`atomic`、线程创建/`join`、`condition_variable` 等。

## 3. `std::atomic` 基础

`atomic<T>` 保证对它的读、写、读改写是**不可分割**的，并附带内存序语义。常用操作：`load`、`store`、`exchange`、`fetch_add/sub/and/or`、`compare_exchange_weak/strong`（CAS）。

```cpp
std::atomic<long> hits{0};
long locked_hits = 0;
std::mutex mu;

void work(int n) {
    for (int i = 0; i < n; ++i) {
        hits.fetch_add(1, std::memory_order_relaxed);   // atomic read-modify-write: no lost updates
        std::lock_guard<std::mutex> g(mu);              // the mutex version of the same counter
        ++locked_hits;
    }
}
```

```cpp
// Lock-free "update the max": retry until our compare_exchange wins or someone stored a bigger value.
void update_max(std::atomic<long>& m, long v) {
    long cur = m.load(std::memory_order_relaxed);
    while (cur < v && !m.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {
        // on failure, cur was refreshed with the current value; loop re-checks cur < v
    }
}
```

```text
atomic counter 400000, mutex counter 400000 (both exact)
max via CAS loop: 3999
is_lock_free: atomic<bool> true, atomic<uint64_t> true, atomic<64-byte struct> false (falls back to a hidden lock)
sizeof(atomic<long>)=8
```

* `fetch_add` 是原子读改写，不会丢更新（`++` 在 `atomic` 上也是）；`mutex` 版本同样正确但更重（阻塞、内核介入）。
* **CAS 循环**是无锁算法的积木：读当前值 → 计算 → `compare_exchange` 仅在值未变时写入；失败说明别人先改了，`cur` 被刷新，重来。`_weak` 允许伪失败（在循环里更快），`_strong` 不会伪失败。
* `is_lock_free()`：小型整数/指针的 `atomic` 是真正的无锁（单条原子指令）；大结构会退化为内部加锁。

## 4. `memory_order`：到底在保证什么

| 序 | 保证 |
|---|---|
| `relaxed` | 只保证这个操作本身原子；不对其它内存访问排序。适合计数器、统计 |
| `release`（store） | 本线程在这条 store **之前**的所有读写，不会被重排到它之后 |
| `acquire`（load） | 本线程在这条 load **之后**的所有读写，不会被重排到它之前 |
| `acq_rel` | 读改写操作兼有两者 |
| `seq_cst`（默认） | 在 acq/rel 之上，所有 `seq_cst` 操作有**一个全局总顺序** |

**配对规则**：线程 A 对原子变量做 `release` 写，线程 B 的 `acquire` 读读到了这个值，则 A 在 release 之前的所有写入，B 在 acquire 之后都能看到（synchronizes-with / happens-before）。这是「发布数据」的标准方式：

```cpp
struct Msg { int a = 0; int b = 0; };
Msg msg;                                   // plain, non-atomic data
std::atomic<bool> ready{false};

void producer() {
    msg.a = 1; msg.b = 2;                                   // (1) write the data
    ready.store(true, std::memory_order_release);           // (2) publish: everything before this is visible to an acquirer
}
void consumer() {
    while (!ready.load(std::memory_order_acquire)) { }      // (3) acquire pairs with the release store
    assert(msg.a == 1 && msg.b == 2);                       // (4) guaranteed to see the writes from (1)
    std::cout << "consumer saw " << msg.a << "," << msg.b << "\n";
}
```

自旋锁：`test_and_set` 用 acquire，`clear` 用 release——正好形成临界区的边界：

```cpp
class SpinLock {
    std::atomic_flag f_ = ATOMIC_FLAG_INIT;
public:
    void lock() { while (f_.test_and_set(std::memory_order_acquire)) { std::this_thread::yield(); } }   // acquire on entry
    void unlock() { f_.clear(std::memory_order_release); }                                              // release on exit
};
```

```text
consumer saw 1,2
spinlock-protected counter 200000
```

### 为什么需要 `seq_cst`：store-buffering 实验

两个线程：T1 `x=1; r1=y;`，T2 `y=1; r2=x;`。顺序一致性下 `r1==0 && r2==0` 不可能出现；放松后两个线程的 store 都可能还留在存储缓冲里，各自读到对方的旧值 0。实验每轮重置并同时放行两个线程，统计两者都读到 0 的轮数：

```text
rounds: 200000
memory_order_relaxed: r1==0 && r2==0 in 199774 rounds
memory_order_seq_cst: r1==0 && r2==0 in 0 rounds
```

`relaxed` 下几乎每一轮都出现「两个 0」，`seq_cst` 下一次也没有。教训：**没有同步的"我先写了所以你应该能看到"是错的**；默认用 `seq_cst`，有测量证据再降级。

## 5. 无锁 SPSC 队列

单生产者单消费者（SPSC）环形缓冲区，是低延迟系统最常见的无锁结构：

* `tail` 只由生产者写，`head` 只由消费者写——**没有竞争的写者**，不需要 CAS。
* 生产者：写入槽位，然后用 `release` 更新 `tail`（发布）；消费者用 `acquire` 读 `tail`，保证能看到槽位内容。反之消费者 `release` 更新 `head`，生产者 `acquire` 读它以知道槽位已空。
* 容量取 2 的幂，用 `& (N-1)` 代替取模；计数器单调递增（无符号回绕无问题），`tail - head` 即元素数。

```cpp
template <class T, std::size_t N>                       // N must be a power of two: index = counter & (N-1), no modulo
class SpscRing {
    static_assert((N & (N - 1)) == 0, "capacity must be a power of two");
    alignas(64) std::atomic<std::size_t> head_{0};      // written only by the consumer
    alignas(64) std::atomic<std::size_t> tail_{0};      // written only by the producer; own cache line (no false sharing)
    alignas(64) T buf_[N];
public:
    bool push(const T& v) {                             // producer thread only
        std::size_t t = tail_.load(std::memory_order_relaxed);            // our own variable: relaxed is enough
        if (t - head_.load(std::memory_order_acquire) == N) return false; // full (acquire: see the consumer's frees)
        buf_[t & (N - 1)] = v;
        tail_.store(t + 1, std::memory_order_release);                    // publish the slot
        return true;
    }
    bool pop(T& out) {                                  // consumer thread only
        std::size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return false;     // empty
        out = buf_[h & (N - 1)];
        head_.store(h + 1, std::memory_order_release);                    // hand the slot back
        return true;
    }
};
```

```text
transferred 2000000 items in order, sum 1999999000000 (expected 1999999000000)
```

二百万个元素按序、无丢失地传输（和校验匹配）。

要点：`alignas(64)` 把 `head_`、`tail_` 和缓冲区各放在**独立缓存行**，原因见下一节。

## 6. 伪共享（false sharing）

缓存一致性协议（MESI）以**缓存行**为单位工作（x86 通常 64 字节；一些 ARM 芯片 128 字节）。两个线程写**不同的变量**，只要它们落在同一缓存行，每次写都会让对方核心的那一行失效，缓存行在核心之间来回弹跳，性能崩溃，尽管没有任何逻辑共享。

```cpp
struct Adjacent { std::atomic<long> a{0}; std::atomic<long> b{0}; };                     // same cache line
struct Padded64 { alignas(64) std::atomic<long> a{0}; alignas(64) std::atomic<long> b{0}; };
struct Padded128 { alignas(128) std::atomic<long> a{0}; alignas(128) std::atomic<long> b{0}; };
```

两个线程各自对自己的计数器做 5000 万次自增：

```text
sizeof: Adjacent=16 Padded64=128 Padded128=256
2 threads x 50000000 increments of their own counter:
  adjacent (same line) : 612.738 ms
  alignas(64) padding  : 68.8275 ms
  alignas(128) padding : 68.6776 ms
```

相邻存放比各占一行慢了约 10 倍。修复：`alignas(64)`（或 `std::hardware_destructive_interference_size`）把被不同线程频繁写入的数据隔开；代价是内存浪费，所以只对热点变量使用。

## 7. 无锁的真相

* **lock-free**：系统整体总有进展（某个线程失败是因为别的线程成功了）；**wait-free**：每个线程都在有限步内完成。多数 CAS 循环是 lock-free 不是 wait-free。
* **ABA 问题**：CAS 看到值 A，期间被改成 B 又改回 A，CAS 成功但结构已变。解决：带版本号的指针、hazard pointer、epoch 回收。
* 无锁结构的难点是**内存回收**和**正确性验证**，不是 CAS 本身。除非性能分析证明锁是瓶颈，先用 `mutex`。
* 无锁 ≠ 更快：高争用下 CAS 重试可能比互斥锁更糟。SPSC 之所以好用，是因为它没有争用。

## 8. 坑

1. 用 `volatile` 做线程同步（C++ 里无效）。
2. 对 `atomic` 做「先读再写」两步（`if (a == 0) a = 1;`）：不是原子的，要用 CAS。
3. 把 `relaxed` 用到需要发布数据的地方。
4. 在 `atomic<T>` 外面再读写 T 的普通副本。
5. 伪共享：计数器数组 `atomic<long> c[8]` 被不同线程分别更新，正好在同一缓存行。
6. 无锁结构里的悬空指针（节点被另一线程释放）。
7. 在循环里自旋而不 `yield`/退避，占满核心。

## 9. 面试官接着会问

**Q：`atomic` 和 `mutex` 的区别？什么时候用哪个？**
要点：atomic 针对单个变量的不可分割操作，无锁，延迟低；mutex 保护一段任意临界区（多变量不变式），会阻塞；一个不变式涉及多个变量就用 mutex。

**Q：解释 `memory_order_acquire`/`release`。**
要点：第 4 节；release 之前的写对 acquire 之后可见；一对一配对；比 `seq_cst` 便宜（在弱序 CPU 如 ARM 上尤其明显；x86 上 acq/rel 本来就是免费的）。

**Q：什么是伪共享？怎么发现和避免？**
要点：第 6 节；perf 看缓存未命中/一致性流量；对齐/填充；每线程私有再合并。

**Q：写一个 SPSC 队列。为什么不需要 CAS？**
要点：每个索引只有一个写者；release/acquire 发布与回收；2 的幂容量；缓存行隔离；满/空判断用 `tail-head`。

**Q：`compare_exchange_weak` 和 `strong`？**
要点：weak 可能伪失败（LL/SC 架构上更快），放循环里用 weak。

**Q：ABA 是什么？**
要点：第 7 节。

**Q：与 Java 对比？**
要点：JMM 以 happens-before 描述，`volatile` 近似 `seq_cst`，VarHandle 提供 acquire/release 模式；C++ 把这些做成每次操作的参数。

## 10. 自测

1. 生产者先写 `data`，再 `ready.store(true, relaxed)`；消费者 `while(!ready.load(relaxed)); use(data)`。哪里错了？
2. `atomic<int> a; a = a + 1;` 是原子递增吗？
3. 为什么 SPSC 队列的 `head_` 和 `tail_` 要放在不同缓存行？
4. 什么时候选 `mutex` 而不是无锁？

<details><summary>答案</summary>

1. `relaxed` 不建立 happens-before，消费者可能看到 `ready==true` 却读到旧的 `data`；应 `release` 写、`acquire` 读。
2. 不是：先 load 再 store，两步之间别的线程可以插入；用 `fetch_add` 或 `a++`/`a += 1`。
3. 它们分别由两个线程频繁写；同一行会导致伪共享，缓存行来回失效。
4. 保护多变量不变式、争用不高、没有性能证据、需要阻塞等待条件时。

</details>
