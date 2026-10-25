# hc15 · 思路与追问（C++20 版）

流式中位数从两个堆开始，面试官一路追问：偶数个数取谁、窗口里怎么删、p 不固定怎么办、值域有界怎么更快。每一问都在看你会不会按条件选结构，并且在边界上不写错。下面按 Part 写清怎么写、面试官在探什么、该说出口的那句话，C++ 特有的坑（有符号溢出 UB、无符号下溢、`vector` 扩容让引用悬空、零分配）放在对应的 Part 里。详细推导和可运行的示例在讲义 [[hc15_streaming_median_cpp]]。

## 30 秒版本

- **两个堆**：`lo` 最大堆装较小一半，`hi` 最小堆装较大一半；偶数个取下中位数，`median()` 就是 `lo.top()`。
- **窗口**：堆不能删任意元素，用惰性删除；每个堆各一张 `delayed` 表、各自的有效个数；失效元素超过 `2k` 就整体重建。
- **百分位**：`rank = n/100·p + ((n%100)·p + 99)/100`，不先算 `p·n`。p 固定用两个堆，p 任意用树堆（treap）。
- **有界价格**：树状数组做直方图，构造时一次分配，之后零分配。
- **C++ 坑**：有符号溢出是 UB；`size_t` 相减会下溢；递归插入时不要持有 `vector` 元素的引用。

## Part 1 · 两个堆

**写法**

```cpp
if (lo_.empty() || price <= lo_.top()) lo_.push(price); else hi_.push(price);
if (lo_.size() > hi_.size() + 1) { hi_.push(lo_.top()); lo_.pop(); }
else if (hi_.size() > lo_.size()) { lo_.push(hi_.top()); hi_.pop(); }
```

`median()` 返回 `lo_.top()`，空时抛 `std::out_of_range`。`doubled_median()` 取两个中间值（奇数个时是同一个值）用 `add_exact` 相加，溢出抛 `std::overflow_error`。

**面试官在探什么**

1. **偶数个数取谁**。下中位数：结果是真实出现过的价格、仍是整数 tick、与 p = 50 的最近秩一致。要平均数就返回两倍（整数，免去舍入约定）。
2. **为什么 `(a + b) / 2` 不行**。两个大数相加有符号溢出，是 UB，不是回绕。要平均数写成 `a + (b - a) / 2`（`a ≤ b`），或者像 `doubled_median` 那样返回两倍并用 `__builtin_add_overflow` 检查。`std::abs(LLONG_MIN)` 同理是 UB。
3. **新数放哪边**。`price <= lo_.top()` 放 `lo_`。写成 `<` 时，等于堆顶的重复值会进 `hi_`，结果仍然正确：不变式只要求 `lo_` 里每个数 ≤ `hi_` 里每个数，相等的值放在哪一边都满足；再平衡只是把一个堆的堆顶移到另一个堆，这个关系不会被破坏，所以中位数不变；平衡条件写反会让 `lo_` 比 `hi_` 少一个，中位数就读错成上中位数。
4. **为什么不用 `std::multiset`**。加删 O(log n)，但取中位数要 `std::next(begin, n/2)`，是 O(n)。可以维护一个指向中位数的迭代器随插入微调（`multiset` 的迭代器在其它元素增删时不失效），但边界很细，两个堆更简单。
5. **`doubled_median` 的溢出**。`[LLONG_MAX]` 的两倍溢出；`[LLONG_MAX, LLONG_MIN]` 两个中间值之和是 `-1`，不溢出。不能看到极端值就直接抛。

**该说出口的话**：「两个堆把有序序列从中间切开，加一个数最多挪一个元素；偶数个取下中位数，因为它是真实价格，并且和 p50 一致。」

## Part 2 · 滑动窗口（惰性删除）

**写法**：环形缓冲 `ring_` 记最近 k 个值，每个堆各有一张 `unordered_map<long long, int>` 的 `delayed` 表和一个有效个数。窗口满时，旧值 `old <= lo_.top()` 就记在 `lo_` 的表里，否则记在 `hi_` 的表里。加入新值、记账、平衡之后，对两个堆各做一次 `prune`：堆顶在 `delayed` 里就弹掉并减计数。

```cpp
if (lo_valid_ > hi_valid_ + 1)  { prune(lo_, delayed_lo_); /* 挪一个到 hi_ */ }
else if (lo_valid_ < hi_valid_) { prune(hi_, delayed_hi_); /* 挪一个到 lo_ */ }
prune(lo_, delayed_lo_); prune(hi_, delayed_hi_);
```

**面试官在探什么**

1. **堆为什么不能删任意元素**。`std::priority_queue` 只暴露堆顶。惰性删除把「删」推迟到它浮上堆顶的时候。
2. **平衡按什么**。按有效个数，不是 `size()`：堆里还躺着失效元素，`size()` 比窗口里真实的个数大。
3. **为什么每个堆一张表**。相等的值可能同时在两个堆里；共用一张表会把本该记在 `hi_` 的账记到 `lo_` 上，弹错堆。
4. **旧值归属**。`lo_` 里每个数 ≤ `hi_` 里每个数，所以 `old <= lo_.top()` 就在 `lo_`；相等时 `lo_` 顶本身就是一份有效拷贝。
5. **无符号下溢**。`lo_valid_` 和 `hi_valid_` 是 `std::size_t`。错误写法 `lo_valid_ - hi_valid_ > 1` → 当 `lo_valid_ < hi_valid_` 时下溢成巨大的数，条件恒为真 → 改成只加不减：`lo_valid_ > hi_valid_ + 1`。
6. **内存会不会涨**。升序流里旧的小值沉在 `lo_` 底部永远浮不上来，堆会长到 O(n)。失效元素超过 `2k` 时整体重建：把环形缓冲里的值排序，前一半进 `lo_`，后一半进 `hi_`，清空两张表。至少隔 `2k` 次 `add` 才重建一次，摊还 O(log k)；测试要求 `retained() <= 4k`。
7. **替代方案**。`std::multiset` 支持按值删除，但取第 k/2 小是 O(k)；顺序统计树两者都 O(log k)。

**该说出口的话**：「堆只能删堆顶，所以我记账、等它浮上来再弹；平衡看有效个数，失效太多就整体重建，内存才不会随流增长。」

## Part 3a · 固定 p：两个堆

**写法**：`lo_` 装最小的 `nearest_rank(n, p)` 个数。每次 `add` 后 n 加 1，rank 最多加 1，所以只需要挪一两个元素：

```cpp
const auto target = static_cast<std::size_t>(nearest_rank(n_, p_));
while (lo_.size() > target) { hi_.push(lo_.top()); lo_.pop(); }
while (lo_.size() < target) { lo_.push(hi_.top()); hi_.pop(); }
```

**面试官在探什么**

1. **rank 为什么向上取整**。第 `⌈p·n/100⌉` 小：`{15, 20, 35, 40, 50}` 的 P30 是第 2 个（20），向下取整会得到第 1 个（15）。
2. **为什么不能 `(p * n + 99) / 100`**。`n` 接近 `LLONG_MAX` 时 `p * n` 有符号溢出是 UB。拆成 `n/100·p + ((n%100)·p + 99)/100`，`nearest_rank` 已经写好。
3. **p = 50 就是 Part 1**。检查参数先于检查空：`TwoHeapPercentile(0)` 构造时就抛 `std::invalid_argument`。
4. **局限**。p 在构造时固定；要同时回答多个 p，或者 p 到查询时才给，就换 Part 3b。

**该说出口的话**：「固定 p 就让 `lo` 装最小的 ⌈p·n/100⌉ 个，每次加一个数最多挪一两个，查询 O(1)。」

## Part 3b · 任意 p：树堆（顺序统计树）

**写法**：结点放在平行的 `std::vector`（`key_`、`cnt_`、`left_`、`right_`、`total_`、`prio_`）里，下标 0 表示空结点。相同的值合并成一个结点，`total_[t] = cnt_[t] + total_[left_[t]] + total_[right_[t]]`。插入先按值下降，回溯时若孩子的优先级比自己高就旋转。`kth(rank)` 从根往下一次走完：`rank <= 左子树总数` 往左，`<= 左子树总数 + cnt` 就是当前结点，否则减掉这部分往右。

**面试官在探什么**

1. **为什么标准库不够**。`std::set` / `std::map` 的 `std::next(begin, k)` 是 O(k)。需要每个结点记子树大小的结构，标准库没有；`__gnu_pbds` 是 libstdc++ 扩展，在 libc++ 上没有。
2. **悬空引用**。错误写法 `auto& n = left_[t]; n = insert(n, x);` → 递归里的 `push_back` 让 `vector` 重新分配，`n` 指向已释放的内存，之后写入是 use-after-free，AddressSanitizer 会报 → 改成先 `const int c = insert(left_[t], x);` 再 `left_[t] = c;`，每次访问都用下标重新取元素。
3. **有序输入**。不平衡的 BST 会退化成链表，递归深度 O(n) 会栈溢出或超时；随机优先级让期望高度是 O(log n)。
4. **重复值**。合并成一个带 `cnt_` 的结点，`kth` 里每个重复值各算一个。
5. **有符号与无符号比较**。`size()` 返回 `int`、`kth` 的参数是 `long long`，都是有符号，直接比较没问题；如果 `size()` 返回 `std::size_t`，`rank > size()` 在 `rank = -1` 时会把 `-1` 转成巨大的无符号数，结果变成 `false`。
6. **检查顺序**。`percentile(p)` 先查 `p`，再查是否为空：空结构上 `percentile(0)` 抛 `std::invalid_argument`，`percentile(50)` 抛 `std::out_of_range`。

**该说出口的话**：「标准库没有按名次取值的树，我写一棵树堆，结点存子树总数，`kth` 一次下降；结点用下标而不是引用，免得 `vector` 扩容后悬空。」

## Part 4 · 直方图 + 树状数组

**写法**

```cpp
for (int i = static_cast<int>(price) + 1; i <= max_tick_; i += i & -i) ++tree_[i];   // 下标从 1 起
// kth：pos = 0；step 从 std::bit_floor(max_tick) 起每次减半
if (pos + step <= max_tick_ && tree_[pos + step] < r) { pos += step; r -= tree_[pos]; }
// 返回 pos：下标 pos + 1 对应价格 pos
```

构造函数里 `tree_.assign(max_tick + 1, 0)` 一次分配完；`add` 和 `percentile` 之后不再分配。

**面试官在探什么**

1. **先查范围再转型**。`price` 在 `long long` 里检查 `0 <= price < max_tick`，再 `static_cast<int>`；先转后查，`LLONG_MAX` 被截断成 `-1` 之类的值就蒙混过关了。越界的 `add` 不能计数。
2. **`max_tick` 不是 2 的幂**。倍增下降要有 `next <= max_tick_` 这个上界，否则读到数组外面。起点用 `std::bit_floor`（`<bit>`，C++20）。
3. **下标从 1 起**。`i & -i` 在 0 上不变，循环不会前进，会死循环；所以树状数组下标是价格加 1。
4. **怎么证明零分配**。测试把全局 `operator new` 换成计数版，构造之后做 20 万次操作，计数必须是 0。`std::vector` 的 `push_back`、临时 `std::string` 都会破坏这一点。
5. **内存上限**。`MAX_TICKS = 2^22` 个 `long long` 约 32 MiB；价格范围到 10^9 就放不下了，要换顺序统计树或近似草图（t-digest / HdrHistogram）。
6. **怎么选结构**。一个固定分位 → 两个堆；任意分位、值域无界、要名次 → 树堆；值域有界 → 直方图。

**该说出口的话**：「价格有界我就用树状数组直方图：构造时一次分配，`add` 单点加，`kth` 倍增下降，每次操作 O(log T)，没有堆分配。」

## 性能与追问

- 限时（`-O2`，无 sanitizer）：直方图 1 秒、`StreamingMedian` / `WindowMedian` / `TwoHeapPercentile` 各 2 秒、`OrderStatistics` 3 秒，每项 100 万次操作。
- **多线程**：每个线程一份局部结构，定期合并；直方图逐桶相加最容易，堆不好合并；或者单写者加快照。
- **近似分位数**：t-digest / GK / 对数分桶，空间 O(1/ε)，误差有界。先问对精度的要求。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 堆 | `PriorityQueue<Long>`（装箱） | `std::priority_queue<long long>`，最小堆要显式 `std::greater<>` |
| 清空堆 | `clear()` | 赋值一个新堆 |
| 溢出 | `Math.addExact` 抛异常 | `__builtin_add_overflow`；有符号溢出是 UB |
| 空 / 非法 | `NoSuchElementException` / `IllegalArgumentException` | `std::out_of_range` / `std::invalid_argument` |
| 树堆结点 | 数组，注意扩容后旧数组的引用 | `vector` + 下标，不持有引用 |
| 零分配证明 | `ThreadMXBean` | 替换全局 `operator new` 计数 |
| `size()` | `int` | `std::size_t`：无符号减法下溢 |
