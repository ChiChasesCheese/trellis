# ld01 · 思路与追问（C++20 版）

这道设计题的分数不在「写出一个环形缓冲区」，而在你能不能把每一个设计决定的原因说出口：为什么不需要 CAS、release / acquire 各保护什么、为什么 PAD 要单独发布、为什么 `closed` 先读。下面按 Part 写清三件事：怎么写、面试官在探什么（所有权、内存序、不变量）、该说出口的那句话。完整的推导和可运行的示例在讲义 [[ld01_spsc_channel_cpp]]。

## 30 秒版本

- **单写者原则**：`tail` 只有生产者写，`head` 只有消费者写。没有读-改-写竞争，所以不要锁、不要 CAS，只要可见性和顺序，release / acquire 就够。
- **计数自由增长**：`head / tail` 用 `std::uint64_t`，只增不减，下标 = `计数 & mask`。空和满是两个不同的差值；无符号回绕有定义，有符号溢出是 UB。
- **三条内存序**：写完槽位再 `tail.store(release)`；消费者 `tail.load(acquire)` 之后才读槽位；读完槽位再 `head.store(release)`；生产者 `acquire` 读到新 `head` 之后才覆盖槽位。
- **布局**：生产者写的成员和消费者写的成员各占独立的缓存行（`alignas(kCacheLine)`）；cached index 让稳态下每批消息只碰一次对方的缓存行。
- **变长消息**：记录不跨过数据区末尾，放不下就先写 PAD。PAD 必须**单独发布**，否则空环 + `tail` 靠近末尾 + 大消息会死锁。
- **drained**：`closed` 且 `head == tail`，先读 `closed` 再读 `tail`；共享内存里的 `head / tail / closed` 用 `std::atomic_ref`，映射和描述符用 RAII。

## Part 1 · `LongRing`

**写法**

```cpp
bool offer(long long v) {
    if (tail_ - head_ == buf_.size()) return false;   // 满：不覆盖
    buf_[tail_ & mask_] = v;
    ++tail_;
    return true;
}
long long poll() {
    if (head_ == tail_) throw EmptyError("ring is empty");
    return buf_[head_++ & mask_];
}
```

计数和 `mask_` 都用 `std::uint64_t`。容量检查：`std::has_single_bit` 加范围 `[1, 2^30]`，否则抛 `std::invalid_argument`。

**面试官在探什么**

1. **为什么计数自由增长**。下标存成取模后的值时，`head == tail` 既可能是空也可能是满。补救办法要么空一格（浪费一个槽位），要么另存 `size`（多一个要维护的变量，两个线程都要改它）。自由增长的计数让空和满是两个不同的差值，`tail - head` 就是元素个数。
2. **为什么用无符号**。有符号溢出是 UB；无符号回绕有定义，而且回绕之后 `tail - head` 仍然正确。64 位计数每秒加 10 亿也要几百年才回绕。
3. **为什么用掩码**。容量是 2 的幂，`& mask` 比 `%` 便宜，且对无符号数结果相同。这是容量必须是 2 的幂的唯一原因。
4. **没有哨兵值**。每个 `long long` 都可能是合法消息，所以空环 `poll` 只能抛 `EmptyError`；不能返回 `-1` 或 `0` 表示「没有」。
5. **移动之后的环**。`buf_` 和 `mask_` 相互依赖：默认的移动会搬空 vector 而 `mask_` 原样保留，下一次 `offer` 越界写。starter 只声明了拷贝构造和拷贝赋值，编译器就不再生成隐式移动，`std::move(a)` 退化成拷贝，`a` 仍是合法的环。这是五法则的一个具体后果：成员之间有不变量时，默认的逐成员移动会破坏它。

**该说出口的话**：「计数只增不减，用无符号数；空是 `head == tail`，满是差等于容量，不浪费槽位，下标用掩码。」

## Part 2 · `SpscLongRing`

**写法**

```cpp
bool offer(long long v) {                       // 只有生产者线程
    const std::uint64_t t = producer_tail_;     // 自己是 tail 的唯一写者：读私有副本，不读原子变量
    if (t - cached_head_ == buf_.size()) {      // 按旧值看是满的，才去碰消费者的缓存行
        cached_head_ = head_.load(std::memory_order_acquire);
        if (t - cached_head_ == buf_.size()) return false;
    }
    buf_[t & mask_] = v;                                   // (1) 写数据
    producer_tail_ = t + 1;
    tail_.store(t + 1, std::memory_order_release);         // (2) 发布
    return true;
}
```

`poll` 对称：旧的 `cached_tail_` 说空才 `tail_.load(acquire)`；读完槽位再 `head_.store(h + 1, release)` 归还。成员分三组：只读的 `buf_ / mask_` 放最前面；`alignas(kCacheLine)` 的 `tail_` 加生产者私有的 `producer_tail_ / cached_head_`；另一个 `alignas(kCacheLine)` 的 `head_` 加消费者私有的两个。

**面试官在探什么**

1. **为什么不需要 CAS**。CAS 解决「多个写者同时改同一个变量」。这里每个变量只有一个写者，没有这个问题。多生产者时 `tail` 才会变成 CAS 竞争；或者每个生产者一个环，消费者轮询，后者没有竞争，通常更快。
2. **四处内存序各保护什么**：

   | 位置 | 序 | 保护 |
   |---|---|---|
   | 生产者 `tail_.store` | release | (1) 的数据写先于 `tail` 可见 |
   | 消费者 `tail_.load` | acquire | 与上面配对，之后才读槽位 |
   | 消费者 `head_.store` | release | 槽位读完才归还 |
   | 生产者 `head_.load` | acquire | 与上面配对，看到新 `head` 之后才覆盖槽位 |

   去掉其中任何一对：消费者可能看到新 `tail` 却读到槽位里上一圈的旧值，或者生产者在消费者读完之前覆盖槽位。
3. **x86 上跑通能说明什么**。什么也说明不了：x86 的 store 不会越过 store，把 release 写成 relaxed 多半碰巧正确；ARM / Apple M 上同样的错误几千条消息内就会出现。测试 `consumer_never_sees_a_stale_slot` 每条值由序号算出，消费者逐条核对。
4. **cached index 为什么安全**。`head` 只增不减，旧快照只会让生产者低估空位：按旧值看有空位，实际一定有空位。误判只会发生在相反方向（旧值说满，实际不满），那时再读一次真实值。
5. **伪共享与布局**。两个线程各写同一缓存行里的不同变量，这一行在两核间来回失效。`alignas(kCacheLine)` 把两组写入者的成员隔开；只读的 `buf_ / mask_` 放最前面，不要放在热成员后面，否则每次写 `tail_` 都会让它们所在的行失效。测试要求 `alignof >= kCacheLine`、`sizeof >= 2 * kCacheLine`；reference 在 Apple clang 上 `sizeof(SpscLongRing)` 是 384（`-O2` 实测）。
6. **为什么常量写死 128**。x86 是 64 字节、Apple M 是 128 字节，写 128 两边都对。不要把 `std::hardware_destructive_interference_size` 写进会被别的进程读的共享布局：不同编译器给出的值不同。
7. **`size()` 的读法**。任何线程可调，先读 `head` 再读 `tail`：`tail` 只增不减，所以差不会是负数；再 `std::min` 到容量，因为中间有可能被对方推进。它是近似值。
8. **`seq_cst` 为什么不需要**。只有两个线程、两对 release / acquire；`seq_cst` 多出来的「所有线程看到同一个全局顺序」在这里没人需要，而它在 x86 上让 store 变成带全屏障的指令。
9. **谁能调什么**。`is_empty()` 只给消费者用，`is_full()` 只给生产者用：它们读自己的私有副本，再读对方的原子变量；换个线程调，读到的私有副本不是它自己的，结果不可信。

**C++ 专属坑**

- 把成员写成 `std::atomic` 之后，类自动不可拷贝、不可移动；不要再手写拷贝构造「帮」它。
- `static_assert(std::atomic<std::uint64_t>::is_always_lock_free)`：藏着锁的 `std::atomic` 会违背「无锁」的承诺。
- 测试里的等待循环要带截止时间；`while (!ring.offer(i)) {}` 在 bug 出现时会让整个测试挂死，不是失败。

**该说出口的话**：「每个共享变量只有一个写者，所以不用 CAS；写完数据再 release 发布 `tail`，对方 acquire 读到才读数据，读完再 release 归还 `head`。」

## Part 3 · `MessageRing`

**写法**

```cpp
bool offer(std::span<const std::uint8_t> msg) {
    // len > max_payload() -> invalid_argument；已 finish -> StateError
    const std::uint32_t rec = (4 + len + 7) & ~7u;
    std::uint64_t t = tail_;
    std::uint32_t idx = t & mask_, to_end = capacity_ - idx;
    if (rec > to_end) {                                   // 末尾放不下一整条
        if (!has_room(t, to_end)) return false;
        store32(HEADER_BYTES + idx, PAD);                 // PAD 单独发布
        t += to_end; tail_ = t;
        word(OFF_TAIL).store(t, std::memory_order_release);
        idx = 0;
    }
    if (!has_room(t, rec)) return false;
    // memcpy 载荷 -> 写 len -> tail.store(t + rec, release)
}
```

`has_room` 先用缓存的 `head`，不够再 `acquire` 读真正的 `head`。`poll` 遇到 `len == PAD` 就把 `head` 推到数据区末尾、`release` 发布，然后继续循环；读完记录之后再 `release` 发布 `head`。

**面试官在探什么**

1. **布局为什么这样**。`head`（偏移 128）和 `tail`（偏移 256）相隔一整条缓存行，各归一个写者；`closed` 只有生产者写。记录补零到 8 字节，是为了 `len` 和后续记录的首地址对齐。
2. **回绕规则**。一条记录不能被数据区末尾切成两半，因为消费者按连续内存读。放不下就先写 PAD 把末尾填满，消费者看到 `len = -1` 就把 `head` 跳到下一圈的开头。
3. **PAD 为什么单独发布（最重要的活性问题）**。例子：容量 64，空环，`tail = 48`，要放 60 字节的消息，记录占 64 字节。末尾剩 16 字节，PAD 16 字节加记录 64 字节要 80 字节，大于容量 64，整体永远放不下。如果「PAD 加记录」整体判断，生产者永远返回 `false`，消费者无物可读，两边互相等。正确做法是：只要放得下 PAD 就先发布它，随后真记录放不下就返回 `false`。按这个顺序走一遍（已在 reference 上跑过）：第一次 `offer` 返回 `false`，`bytes_pending()` 是 16；消费者 `poll` 返回 `nullopt`（越过 PAD），`bytes_pending()` 变 0；第二次 `offer` 返回 `true`。代价是：`offer` 返回 `false` 时可能已经悄悄发布了一条 PAD。
4. **`false` 和异常的区别**。超过 `max_payload()`（`capacity - 4`）永远放不下，是调用方的错，抛 `std::invalid_argument`；暂时满只是 `false`，重试即可。把两者混成一个返回值，调用方会在永远放不下的消息上空转。
5. **drained 怎么判**。`closed == 1` 且 `head == tail`，**先读 `closed` 再读 `tail`**。生产者先发布最后的 `tail`，后置 `closed`：消费者先读到 `closed == 1`，就保证后面读到的 `tail` 是最终值。反过来先读 `tail` 再读 `closed`：读到旧 `tail`、却看到 `closed`，会漏掉最后几条。末尾残留的 PAD 要等 `poll` 越过它之后才 drained。
6. **`init` 为什么最后才写 `magic`**。`magic` 用 release 写，`attach` 用 acquire 读：看见 `magic` 的人一定看见前面写的 `capacity` 和 `version`；看不见就说明环还没建好，报 `StateError`。
7. **共享内存里怎么做原子访问**。`head / tail / closed` 在一块普通字节里，用 `std::atomic_ref<std::uint64_t>`，它要求地址按 8 字节对齐，所以 `init` / `attach` 先检查首地址，不对齐就拒绝（否则第一次 load 就是 UB）。同一个字对 `atomic_ref` 之外的普通访问与并发访问是数据竞争。`std::vector`、`std::string`、指针不能放进共享内存：它们指向各进程自己的地址。
8. **数据字节为什么不用原子**。它们是普通内存，靠 `tail` 的 release / acquire 保护：生产者写完才发布，消费者看到才读，同一时刻没有人读写同一块字节。
9. **`optional` 的语义**。`nullopt` 是「现在没有」，持有空 vector 的 `optional` 是「收到了一条空消息」，类型层面就是两个不同的值；`poll` 返回 `nullopt` 也不等于结束，结束要看 `is_drained()`。

**C++ 专属坑**

- 一次 `memcpy` 的目标越过数据区末尾 → 越界写，ASan 立刻报；写 PAD 之后一定要把 `idx` 置 0。
- `offer` 把调用方的字节拷进环里，`poll` 返回一份新 `vector`：不要把指向环内部的 `span` 交给调用方，消费者一归还 `head`，生产者就会覆盖它。
- `span<std::byte>` 只是视图，不拥有内存；它指向的内存必须活得比环对象久。

**该说出口的话**：「PAD 必须单独发布，否则空环、`tail` 靠近末尾、大消息会死锁；drained 要先读 `closed` 再读 `tail`。」

## Part 4 · `SharedChannel`

**写法**：两个 RAII 小类。`Fd` 的析构关描述符；`Mapping` 持有 `mmap` 的返回值，析构 `munmap`，移动后把原对象置空。`create` 的顺序是：先 `MessageRing::segment_bytes(capacity)`（非法容量在此抛 `std::invalid_argument`，文件还没碰），再 `open(O_RDWR | O_CREAT | O_TRUNC)`、`ftruncate`、`Mapping`、`MessageRing::init`。`open` 先 `fstat` 看大小，小于 `HEADER_BYTES` 直接 `StateError`，再 `Mapping`、`attach`。`close()` 就是 `map_.reset()`；每个公开方法先检查映射还在，不在抛 `StateError`。

**面试官在探什么**

1. **谁拥有映射和描述符**。局部的 `Fd` 在函数结束时关闭（映射建好之后描述符可以关，映射依然有效）；`Mapping` 归 `SharedChannel`。`attach` 抛异常时，`Mapping` 和 `Fd` 的析构自动执行，不泄漏；不用 RAII 的话每个失败分支都要手写清理。
2. **先校验再动文件**。如果先 `O_TRUNC` 再检查容量，非法参数会把已有文件截断。顺序反了就是数据丢失。
3. **移动语义**。`SharedChannel` 不可拷贝（两个所有者会 `munmap` 两次），可移动；被移走的对象 `Mapping` 为空，访问抛 `StateError`。移动赋值要先释放自己原来的映射，再接管对方的，并处理自赋值。
4. **跨进程的内存序还成立吗**。成立的是硬件缓存一致性加 `atomic_ref` 发出的屏障；两个进程映射同一批物理页，release / acquire 的配对和线程之间一样有效。这不是 C++ 标准对「多个进程」的形式化保证，说法要谨慎。
5. **怎么测试跨进程代码、避免挂死**。`fork()` 出子进程，子进程**自己重新 `open` 文件**（模拟真正独立的映射，并顺带测 `attach` 的校验），结果通过 `pipe` 回传，父进程 `waitpid` 带超时、超时就 `SIGKILL`；两端自旋都带截止时间；每条消息的长度和内容由序号决定，丢、重、乱序、损坏都能抓到；绝不靠 `sleep` 对时序。
6. **`fork` 的坑**。多线程程序里 `fork`，子进程只有调用 `fork` 的那个线程，其他线程持有的锁永远不会释放。测试里要在起任何线程之前 `fork`，子进程里只做这一件事然后 `_exit`，不跑析构和 `atexit`。
7. **崩溃恢复**。`head / tail` 都在文件里，消费者崩溃重启后 `attach` 就能接着读；读完才发布 `head`，所以处理到一半崩溃会重读那条消息，语义是至少一次，下游要幂等。
8. **零拷贝的方向**。生产者向环申请一段连续区域（`std::span<std::byte>`）、直接写进去、再提交；消费者用回调读，回调返回才归还。省掉两次拷贝和 `poll` 里的分配。

**该说出口的话**：「先校验参数再碰文件；映射和描述符都包进 RAII，`attach` 抛异常也不泄漏；测试用子进程重新 `open`，两端都带截止时间。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 内存序 | `VarHandle.setRelease / getAcquire` | `std::atomic::store / load` 带 `memory_order`；别人的内存用 `std::atomic_ref` |
| 填充 | 继承链加填充 `long` | `alignas(kCacheLine)`，语言直接支持 |
| 计数溢出 | 有符号回绕有定义 | 有符号溢出是 UB，计数用 `std::uint64_t` |
| 段的内存 | `MemorySegment` + `Arena` | `std::span<std::byte>`，不拥有；映射由 `Mapping` 的析构释放 |
| 「没有」与「空」 | `null` 与 `byte[0]` | `std::nullopt` 与持有空 vector 的 `optional` |
| 异常 | `IllegalStateException`、`NoSuchElementException`、`NoSuchFileException` | `StateError`、`EmptyError`、`std::system_error` + `errc` |
| 资源释放 | `AutoCloseable` / try-with-resources | 析构函数（RAII），移动后源对象置空 |
| 拷贝 | 引用语义，赋值共享同一个环 | 值语义，拷贝是独立的环；要想清楚移动之后的状态 |
| 跨进程测试 | 起子 JVM、拼 classpath | `fork()` + `pipe` + `waitpid` |
