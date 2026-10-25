# hc04 · 思路与追问（C++20 版）

队列均值第一问几分钟就能写完，分数在后面：面试官每追一句，就是在看你有没有想到浮点漂移、128 位和、移动语义、悬空引用、数据竞争这些 C++ 的坑。下面按 Part 写清三件事：怎么写、面试官在探什么、该说出口的那句话。详细推导和可运行的示例在讲义 [[hc04_queue_mean_snapshot_cpp]]。

## 30 秒版本

- **队列**：`std::vector<long long>` 环形缓冲，容量恒为 2 的幂，用 `& (容量 - 1)` 代替 `%`；扩容按**逻辑顺序**复制，`head` 归零。
- **和**：`__int128` 累加器，push 加、pop 减，`get_mean` 只做一次除法；不用 `double`，不用 `long long`。
- **均值**：返回约分的分数 `Mean`（分母恒正）；`get_mean()` 对精确值只舍入一次。
- **移动**：成员里有 `int` / `size_t` / `__int128`，编译器生成的移动构造只拷贝它们，源对象会谎称自己还有元素；自己写，用 `std::exchange` 清零。
- **快照**：`Correct` 直接换一个新队列；要保留历史就用持久化队列，版本只是三个数，不复制内容。
- **读者**：seqlock（版本号奇偶 + relaxed 原子字段 + 栅栏），写者无分配；普通变量被并发读是 UB。

## Part 1 · 队列 + 均值

**写法**

```cpp
void push(long long x) {
    if (size_ == buf_.size()) grow();                 // 先扩容再改状态：抛异常时队列没动过
    buf_[(head_ + size_) & (buf_.size() - 1)] = x;
    ++size_;  sum_ += x;                              // sum_ 是 i128
}
```

`pop` 先判空，取 `buf_[head_]`，`head_` 前进，`sum_ -= x`。`grow` 先复制 `[head_, 容量)`，再复制 `[0, head_)`，新 `head_ = 0`。`mean()` 返回 `Mean(sum_, size_)`，构造函数用 `u128` 的欧几里得算法约分。

**面试官在探什么**

1. **为什么不每次求和**：`get_mean` 遍历是 O(n)，100 万次操作就是 O(n²)；维护 running sum 后 push / pop / mean 都是 O(1)。
2. **为什么不用 `double` 累加**：`1e16 + 1 + 1` 里每个 `+1` 都被舍掉，弹出 `1e16` 后得到 0 而不是 2。整数和是精确的，可逆的。
3. **为什么是 128 位**：`n` 个 `long long` 的和不超过 `n · 2^63`，元素个数小于 2^63 时一定小于 2^126。两个 `LLONG_MAX` 的和是 2^64 − 2，已经放不进 `long long`。`long double` 不行：宽度随平台变，Apple arm64 上它就是 64 位 `double`。
4. **`deque` 还是环形数组**：两者的操作都是 O(1)。环形数组是一块连续内存、一次分配、扩容才复制；`std::deque` 是分块的，指针多一层，缓存局部性差一点，但扩容不复制元素。没有性能要求时 `std::deque` 更省代码，要说出这个让步。
5. **`get_mean` 为什么不是 `(double)sum / n`**：和不超过 ±2^53 时，两个操作数都是精确的 `double`，一次 IEEE 除法就是正确舍入，这是快路径。超过之后 `(double)sum` 先舍入一次，除法再舍入一次，两次舍入会出错。例：和 `2^53 + 1`、`n = 3`，精确值 3002399751580331，`(double)sum / 3` 先把和舍入成 2^53，再除以 3，得到 3002399751580330.5。慢路径是 `Mean::to_double`：长除法凑出 54 位商，再加一个**粘滞位**（sticky bit，丢掉的位里有没有非零），最后按「向最近、平局取偶」舍入一次。没有粘滞位，就分不清「恰好在两个 `double` 正中间」和「略大于一半」。
6. **移动构造的坑**：`QueueMean b = std::move(a)` 时，隐式生成的版本移动 `vector`，却**拷贝** `head_`、`size_`、`sum_`。`a` 的缓冲区空了，`size_` 还是 5，之后 `a.push(1)` 判断 `size_ == buf_.size()` 不成立，直接写越界（ASan 会报）。要求被移动的对象是合法的空队列，所以自己写移动构造和移动赋值，用 `std::exchange` 清零，并标 `noexcept`：`std::vector<QueueMean>` 扩容时只有 `noexcept` 的移动构造才会被用，否则退回拷贝。
7. **`LLONG_MIN`**：`-x`、`std::abs(x)`、`x > 0 ? x : -x` 对它都是有符号溢出，UB。取绝对值要转到 `u128` 或无符号类型里做（`u128{0} - static_cast<u128>(x)`）。
8. **空队列**：用 `std::out_of_range` 报错；除以 0 得到 `NaN` 然后当合法答案，是最差的结果。
9. **拷贝**：默认的拷贝（`vector` 加三个标量）本来就是对的，但要测 `head` 在缓冲区中间的情况：拷贝必须保留回绕状态。

**该说出口的话**：「和用 `__int128` 维护，push 加、pop 减，所以每个操作 O(1) 且精确；`get_mean` 只舍入一次，不在 `double` 里累加。」

## Part 2 · 修正快照事件流

**写法**：`std::variant<Push, Pop, Query, Correct>` 加 `std::visit`，用 `overloaded{...}` 把四个 lambda 拼起来，编译器保证四种都处理。`Correct` 分支是 `q = QueueMean{}`，再逐个 push。解析：按空白切 token，`std::from_chars` 转整数，并检查 `ptr` 走到了 token 末尾；每个错误在外层捕获后重新抛成 `"line k: ..."`，k 用下标加 1（空行也占行号）。

**面试官在探什么**

1. **快照是拷贝还是共享**：`Correct` 把状态换成一个新队列，代价 O(k)（k 是快照长度）。这里不需要共享，所以拷贝最简单；要保留历史就是 Part 3。
2. **`Correct` 要不要防御性拷贝**：不用。`std::vector` 成员是值，构造时就拷贝了，调用者之后改原向量不影响事件；也没有 Java 里的 `null` 元素问题。
3. **为什么不用 `std::stoll`**：`stoll("12abc")` 返回 12，不报错；`strtoll` 接受 `+`、前导空格和十六进制。`from_chars` 不接受这些，加上「整个 token 被消费」的检查，才是严格解析。越界（`9223372036854775808`）它会返回 `errc::result_out_of_range`。
4. **`variant` 的好处**：加一种事件，所有 `visit` 编译报错，不会漏处理。代价是类型都要写在 `variant` 里，不像虚函数可以事后扩展。
5. **哪些错误是哪种异常**：解析错误 `invalid_argument`，空队列 `pop` 是 `out_of_range`，两个不能混。

**该说出口的话**：「事件用 `variant` 加 `visit`，漏一种就编译不过；解析用 `from_chars` 并检查整个 token 都被消费，行号从 1 起，空行也算。」

## Part 3 · 持久化队列

**写法**：每次 push 的值是一棵树的节点（`val, parent, jump, depth`），一个版本是 `(tail, head_depth, sum)` 三个数。`push` 新建节点和版本；`pop` 要队头的值，也就是 `tail` 在深度 `head_depth + 1` 的祖先，用跳跃指针（skew-binary jump pointers）在 O(log n) 里找到，新版本只改 `head_depth` 和 `sum`；`mean` 直接用版本里的 `sum`，O(1)。没有任何版本复制内容。

**面试官在探什么**

1. **三档方案**：整份复制，每版本 O(n)，20 万个版本就是 O(n²)；路径复制（path copying）；树加三个数，内存只增不减。要回收就要引用计数，或者只保留最近 K 个版本。
2. **为什么 pop 要祖先查询**：队列的队头是最早 push 的，而树里节点只指向父节点（更早的那个），从 `tail` 往上走 `size - 1` 步才到队头，朴素走法是 O(n)。跳跃指针让每次查询 O(log n)，每节点只多一个 `int`。
3. **悬空引用**：`const Version& v = at(version);` 之后调用 `new_version`，里面的 `push_back` 可能重新分配 `versions_`，`v` 就指向已释放的内存。参考实现把 `Version` 按值拷贝（`i128` 加两个 `int`，32 字节）。同样，`new_node` 里的 `Node parent` 也是按值取的。ASan 能抓到这一类错误，所以测试在 7 万个节点之后回头查旧版本。
4. **索引类型**：节点和版本用 `int` 下标而不是指针，既是为了重新分配后下标仍然有效，也是因为每个节点更小。
5. **版本号检查**：`version < 0` 或 `>= versions_.size()` 都抛 `invalid_argument`；注意先检查负数再转 `size_t`，否则负数变成巨大的无符号数。

**该说出口的话**：「版本只是三个数，内容在共享的树里；`pop` 用跳跃指针找队头，O(log n)。向量重新分配会让引用失效，所以我按值取版本，或者用下标。」

## Part 4 · 单写者、多读者

**写法**：seqlock。写者：`version_` 加 1 变成奇数（正在写）→ release 栅栏 → 用 relaxed 写 `seq_ / size_ / hi_ / lo_` → `version_` 再加 1 变偶数（release）。读者：acquire 读 `version_`，是奇数就 `yield` 重试；偶数就 relaxed 读各字段，acquire 栅栏，再读一次 `version_`，和第一次相等才接受。128 位的和拆成 `hi_`、`lo_` 两个 64 位原子。`pop` 的空队列检查在 `publish()` 之前，所以失败的操作不会让读者看到任何变化。

**面试官在探什么**

1. **撕裂读**：两个 64 位半边分别写，读者可能拿到一半新一半旧；`seq`、`size`、`sum` 也是同理。`std::atomic<__int128>` 在很多平台上不是无锁的，内部可能带锁。
2. **为什么字段是 relaxed 原子而不是普通变量**：读者在写者写的同时读它们，对普通变量这是数据竞争，UB。原子保证每个字不撕裂；它们之间的顺序交给版本号和栅栏。
3. **方案对比**：`std::mutex`（先说它，正确、简单，但读者会阻塞写者）→ 读多写少用 `std::shared_mutex` → 原子发布不可变快照（每次修改分配一个对象，回收靠引用计数，C++20 的 `atomic<shared_ptr>` 并非每个标准库都实现了）→ seqlock（无分配，只适合单写者，读者要重试，所以是 obstruction-free 而不是 wait-free）。
4. **为什么 release / acquire 够用，不必 `seq_cst`**：这里只需要「字段写入夹在两次版本号写入之间」这一个顺序。默认的 `seq_cst` 一定正确，先写它再优化也合理，要说出代价（栅栏开销，ARM 上更明显）。
5. **写者怎么保证只有一个**：第一次写的线程用 `compare_exchange_strong` 把自己的 `std::thread::id` 存进原子的 `owner_`，别的线程再写抛 `SingleWriterViolation`。要补一句：线程 id 在线程结束后可能被复用，写者线程的生命周期要由设计保证。
6. **怎么验证没有数据竞争**：普通测试通不过不代表没有竞争，要用 ThreadSanitizer 跑并发测试。
7. **多个写者怎么办**：串行化（一个队列加单线程执行），或者 CAS 循环更新不可变快照；此时 push / pop 的 FIFO 语义要先问清楚。

**该说出口的话**：「写者把版本号变奇数，改字段，再变偶数；读者读前读后各看一次版本号，不相等或是奇数就重试。字段用 relaxed 原子，因为读写会同时发生，普通变量是数据竞争。」

## C++ 专属坑速查

- 隐式移动构造不清零标量成员；移动构造 / 赋值要自己写，标 `noexcept`。
- `LLONG_MIN` 取负、`std::abs` 都是 UB。
- `(double)sum / n` 在和超过 2^53 时舍入两次。
- `push_back` 之后旧引用、旧迭代器作废；按值取或用下标。
- `std::stoll` 不严格；用 `from_chars` 并检查消费到末尾。
- 普通变量被并发读写是 UB，relaxed 原子不是；`std::atomic<__int128>` 不一定无锁。
- 环形缓冲扩容要按逻辑顺序复制，不能整块 `copy`。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 128 位和 | 自己用两个 `long` 拼（`I128` record） | `__int128`（编译器扩展），`u128` 做约分和取绝对值 |
| 空队列 | `NoSuchElementException` | `std::out_of_range` |
| 事件类型 | `sealed interface` + record + 模式匹配 `switch` | `std::variant` + `std::visit` + `overloaded` |
| 快照拷贝 | `List.copyOf`，`null` 元素抛 NPE | `std::vector` 成员本身就是值，没有 `null` |
| 整数解析 | `Long.parseLong` | `std::from_chars`，要自己检查消费完整 |
| 被移动的对象 | 没有这回事 | 隐式移动不清零标量，要自己写 |
| 发布一致快照 | 不可变 `Stat` + `VarHandle.setRelease/getAcquire`（每次分配） | seqlock：奇偶版本号 + relaxed 原子 + 栅栏（无分配） |
| 悬空引用 | 不存在（GC） | `vector` 重新分配后旧引用作废 |
| 写者身份 | `compareAndSet` 抢占，抛 `IllegalStateException` | `compare_exchange_strong` 存 `thread::id`，抛 `SingleWriterViolation` |
