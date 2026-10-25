# hc15 · Streaming Median（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。语义与 Java 版完全相同（约定、样例、边界见 `problem.md`）。

## 1. 题目

成交价（`long long` tick）一笔一笔到达，随时回答中位数与百分位。

| Part | 内容 |
|---|---|
| 1 | `StreamingMedian`：两个堆，`add` O(log n)，`median` O(1)；偶数个取**下中位数**；`doubled_median` 返回中位数的两倍 |
| 2 | `WindowMedian(k)`：最近 k 笔的滑动窗口中位数；惰性删除；堆的大小不随流增长 |
| 3 | 任意百分位（最近秩法）：`TwoHeapPercentile(p)` 固定 p；`OrderStatistics` 任意 p |
| 4 | `TickHistogram(max_tick)`：价格有界，树状数组，构造后零分配；100 万次操作 |

约定：

* **偶数个数时取下中位数**（第 ⌈n/2⌉ 小）：结果是真实出现过的价格、仍是整数 tick、等于 p = 50 的最近秩。
* **最近秩法**：n 个数的 p% 分位（`1 ≤ p ≤ 100` 的整数）是排序后第 `⌈p·n/100⌉` 个。`{15, 20, 35, 40, 50}`：P5 = 15，P30 = P40 = 20，P50 = 35，P100 = 50。
* 空结构取值 → `std::out_of_range`；参数非法 → `std::invalid_argument`（先于空检查）；`doubled_median` 溢出 → `std::overflow_error`。

## 2. 前置知识

### 2.1 `std::priority_queue`

默认是**最大堆**：`std::priority_queue<long long>`。最小堆要写 `std::priority_queue<long long, std::vector<long long>, std::greater<>>`。`top()` O(1)，`push` / `pop` O(log n)。没有 `clear()`（赋一个空队列：`q = decltype(q)()`），**不能删任意元素**。

```cpp
using MaxHeap = std::priority_queue<long long>;
using MinHeap = std::priority_queue<long long, std::vector<long long>, std::greater<>>;
```

### 2.2 两个堆为什么能找中位数

排好序的数列从中间切开：较小的一半放进最大堆 `lo_`，较大的一半放进最小堆 `hi_`。不变式：`lo_` 里每个数 ≤ `hi_` 里每个数；`lo_.size() == hi_.size()` 或 `hi_.size() + 1`。则 `lo_.top()` 就是下中位数；加一个数：放对边，最多挪一个元素恢复平衡。

### 2.3 有符号溢出是未定义行为

C++ 里 `long long` 溢出不是回绕而是 UB。`(a + b) / 2` 在两个大数时溢出；`std::abs(LLONG_MIN)` 也是 UB。要检查就用 `__builtin_add_overflow`：

```cpp
inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow");
    return r;
}
```

测试用 `-fsanitize=undefined` 编译：一溢出就终止。

### 2.4 树状数组（Fenwick tree）与 `std::bit_floor`

`tree_[i]` 存区间 `(i − lowbit(i), i]` 的计数，`lowbit(i) = i & -i`。点加 `for (i = x + 1; i <= T; i += i & -i)`；第 r 小用倍增下降，起点是不超过 `T` 的最大 2 的幂：`std::bit_floor(T)`（`<bit>`，C++20）。

## 3. Part 1：两个堆

```cpp
class StreamingMedian {
public:
    void add(long long price) {
        if (lo_.empty() || price <= lo_.top()) lo_.push(price);
        else hi_.push(price);
        if (lo_.size() > hi_.size() + 1) { hi_.push(lo_.top()); lo_.pop(); }
        else if (hi_.size() > lo_.size()) { lo_.push(hi_.top()); hi_.pop(); }
    }
    long long median() const {
        if (lo_.empty()) throw std::out_of_range("no prices yet");
        return lo_.top();
    }
    long long doubled_median() const {
        if (lo_.empty()) throw std::out_of_range("no prices yet");
        const long long upper = lo_.size() == hi_.size() ? hi_.top() : lo_.top();
        return add_exact(lo_.top(), upper);        // 奇数个：中间值 × 2；偶数个：两个中间值之和
    }
    std::size_t size() const noexcept { return lo_.size() + hi_.size(); }
private:
    MaxHeap lo_;
    MinHeap hi_;
};
```

检查：`5, 15, 1, 3` → `5, 5, 5, 3`（加 3 时 `lo_={3,1}`，`hi_={5,15}`，`top = 3`）。`doubled_median` 在 `[LLONG_MAX]` 上溢出，在 `[LLONG_MAX, LLONG_MIN]` 上得 `-1`（不溢出）。

## 4. Part 2：滑动窗口（惰性删除）

堆不能删任意元素。滑出窗口的旧值记进 `delayed` 表（`unordered_map<long long, int>`），等它浮到堆顶再弹；平衡按**有效个数**；每次操作之后两个堆顶都是有效的。

* 环形缓冲 `std::vector<long long> ring_` 记最近 k 个值。
* 两个堆各有一张 `delayed` 表（相等的值可能同时在两个堆里，共用一张表会记错堆）和一个有效个数。
* 旧值归属：`old <= lo_.top()` ⇒ `lo_`（`lo_` 里每个数 ≤ `hi_` 里每个数；相等时 `lo_` 顶本身就是一份有效拷贝）。

```cpp
void add(long long price) {
    long long old = 0;
    const bool evict = count_ == ring_.size();
    if (evict) { old = ring_[head_]; ring_[head_] = price; head_ = (head_ + 1) % ring_.size(); }
    else { ring_[(head_ + count_) % ring_.size()] = price; ++count_; }

    if (lo_valid_ == 0 || price <= lo_.top()) { lo_.push(price); ++lo_valid_; }
    else { hi_.push(price); ++hi_valid_; }

    if (evict) {
        if (old <= lo_.top()) { ++delayed_lo_[old]; --lo_valid_; }
        else                  { ++delayed_hi_[old]; --hi_valid_; }
    }
    if (lo_valid_ > hi_valid_ + 1)      { prune(lo_, delayed_lo_); hi_.push(lo_.top()); lo_.pop(); --lo_valid_; ++hi_valid_; }
    else if (lo_valid_ < hi_valid_)     { prune(hi_, delayed_hi_); lo_.push(hi_.top()); hi_.pop(); --hi_valid_; ++lo_valid_; }
    prune(lo_, delayed_lo_);
    prune(hi_, delayed_hi_);
    if (retained() - lo_valid_ - hi_valid_ > 2 * ring_.size()) rebuild();
}
```

```cpp
template <class Heap> static void prune(Heap& heap, std::unordered_map<long long, int>& delayed) {
    while (!heap.empty()) {
        const auto it = delayed.find(heap.top());
        if (it == delayed.end()) return;
        if (--it->second == 0) delayed.erase(it);
        heap.pop();
    }
}
```

**无符号运算的坑**：`lo_valid_`、`hi_valid_` 是 `std::size_t`。`lo_valid_ < hi_valid_` 没问题，但 `lo_valid_ - hi_valid_ > 1` 会在 `lo_valid_ < hi_valid_` 时下溢成一个巨大的数。所以比较写成 `lo_valid_ > hi_valid_ + 1`（只加不减）；`retained() - lo_valid_ - hi_valid_` 可以相减，因为 `retained()` 一定不小于有效个数之和。

**内存**：升序流里，旧的小值沉在 `lo_` 堆底永远浮不上来，堆会长到 O(n)。失效元素超过 `2k` 就**整体重建**：把环形缓冲里的值排序，前一半进 `lo_`，后一半进 `hi_`，清空 `delayed`。至少隔 `2k` 次 `add` 才发生一次，摊还 O(log k)。`retained() ≤ 4k` 是测试的上界。

```cpp
void rebuild() {
    std::vector<long long> w(count_);
    for (std::size_t i = 0; i < count_; ++i) w[i] = ring_[(head_ + i) % ring_.size()];
    std::sort(w.begin(), w.end());
    lo_ = MaxHeap(); hi_ = MinHeap(); delayed_lo_.clear(); delayed_hi_.clear();
    lo_valid_ = (count_ + 1) / 2; hi_valid_ = count_ - lo_valid_;
    for (std::size_t i = 0; i < count_; ++i) (i < lo_valid_ ? lo_.push(w[i]) : hi_.push(w[i]));   // 三目两边类型都是 void
}
```

`slide(prices, k)` 就是循环 `add` + `median`。

## 5. Part 3：任意百分位

### 5.1 最近秩

```cpp
inline long long nearest_rank(long long n, int p) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (p < 1 || p > 100) throw std::invalid_argument("p must be in 1..100");
    return n / 100 * p + ((n % 100) * p + 99) / 100;      // = ceil(p*n/100)，n 再大也不溢出
}
```

不能直接 `(p * n + 99) / 100`：`n` 接近 `LLONG_MAX` 时 `p * n` 溢出（UB）。`n = 100a + b`：`p·n/100 = a·p + p·b/100`，后一项向上取整。

### 5.2 固定 p：两个堆

`lo_` 装最小的 `nearest_rank(n, p)` 个数。每次 `add` 后 `n` 加 1，`rank` 最多加 1，所以最多挪一两个元素：

```cpp
++n_;
if (lo_.empty() || price <= lo_.top()) lo_.push(price); else hi_.push(price);
const auto target = static_cast<std::size_t>(nearest_rank(n_, p_));
while (lo_.size() > target) { hi_.push(lo_.top()); lo_.pop(); }
while (lo_.size() < target) { lo_.push(hi_.top()); hi_.pop(); }
```

`p_ = 50` 时与 Part 1 相同。局限：`p` 在构造时固定。

### 5.3 任意 p：顺序统计树（树堆）

`std::set` / `std::map` 不能 O(log n) 地回答「第 k 小」（`std::next(begin, k)` 是 O(k)）；标准库没有顺序统计树（libstdc++ 的 `__gnu_pbds` 是扩展，libc++ 没有）。自己写一棵**树堆**：BST（按值）+ 堆（按随机优先级），期望高度 O(log n)。

结点放在平行的 `std::vector` 里，用**下标**当指针，下标 0 = 空结点：

```cpp
std::vector<long long> key_{0};
std::vector<int> cnt_{0}, left_{0}, right_{0}, total_{0};
std::vector<std::uint32_t> prio_{0};
```

相同的值合并成一个结点（`cnt_` 记个数），`total_[t] = cnt_[t] + total_[left_[t]] + total_[right_[t]]`。

```cpp
int insert(int t, long long x) {
    if (t == 0) return new_node(x);
    const auto ti = static_cast<std::size_t>(t);
    if (x == key_[ti]) {
        ++cnt_[ti];
    } else if (x < key_[ti]) {
        const int c = insert(left_[ti], x);            // 递归里 vector 可能扩容
        left_[ti] = c;
        if (prio_[c] > prio_[ti]) { left_[ti] = right_[c]; right_[c] = t; pull(t); pull(c); return c; }   // 右旋
    } else { /* 对称：左旋 */ }
    pull(t);
    return t;
}
```

**悬空引用**：如果写成 `auto& node = nodes_[t]; node.left = insert(node.left, x);`，递归里 `push_back` 让 `vector` 重新分配，`node` 就指向已释放的内存。这里始终用下标，每次访问时重新取元素。测试里插入 4000 个值强迫多次扩容，AddressSanitizer 会报这类错误。

`kth(rank)`：

```cpp
auto t = static_cast<std::size_t>(root_);
long long r = rank;
while (true) {
    const long long l = total_[static_cast<std::size_t>(left_[t])];
    if (r <= l) t = static_cast<std::size_t>(left_[t]);
    else if (r <= l + cnt_[t]) return key_[t];
    else { r -= l + cnt_[t]; t = static_cast<std::size_t>(right_[t]); }
}
```

`percentile(p)` = `kth(nearest_rank(size, p))`，先检查 p 再检查空；`count_at_most(v)` 从根往下，`v < key` 往左，否则累加 `total[left] + cnt` 再往右。

**符号比较**：`rank` 是 `long long`，`size()` 是 `int`——都是有符号，直接比较没问题；如果 `size()` 返回 `std::size_t`，`rank > size()` 在 `rank = -1` 时会把 −1 转成巨大的无符号数而变成 `false`。minitest 的 `CHECK_EQ` 用 `std::cmp_equal` 避免这个陷阱。

### 5.4 怎么选

| 结构 | 查询 | 适用 | 局限 |
|---|---|---|---|
| 两个堆 | O(1) | 一个固定的 p | p 固定 |
| 顺序统计树 | O(log n) | 任意 p、值域无界、要名次 | 实现复杂，常数大 |
| 直方图（Part 4） | O(log T) | 值域有界 | 只表示 `0..T−1` |
| 近似草图 | O(1) 级 | 数据量巨大、容忍误差 | 不精确 |

## 6. Part 4：`TickHistogram`

```cpp
explicit TickHistogram(int max_tick) : max_tick_(max_tick) {
    if (max_tick < 1 || max_tick > MAX_TICKS) throw std::invalid_argument("max_tick out of range");
    tree_.assign(static_cast<std::size_t>(max_tick) + 1, 0);
    top_ = static_cast<int>(std::bit_floor(static_cast<unsigned>(max_tick)));
}

void add(long long price) {
    if (price < 0 || price >= max_tick_) throw std::invalid_argument("price out of range");
    for (int i = static_cast<int>(price) + 1; i <= max_tick_; i += i & -i) ++tree_[static_cast<std::size_t>(i)];
    ++total_;
}

long long kth(long long rank) const {
    if (rank < 1 || rank > total_) throw std::invalid_argument("rank out of range");
    int pos = 0;
    long long r = rank;
    for (int step = top_; step > 0; step >>= 1) {
        const int next = pos + step;
        if (next <= max_tick_ && tree_[static_cast<std::size_t>(next)] < r) { pos = next; r -= tree_[static_cast<std::size_t>(next)]; }
    }
    return pos;                                   // 下标 pos + 1 对应价格 pos
}
```

要点：

* 所有内存在构造函数里分配（`tree_.assign`）；之后 `add` / `percentile` 不分配——测试把全局 `operator new` 换成计数版，20 万次操作后计数为 0。
* `price` 先在 `long long` 里检查范围，再 `static_cast<int>`——先转再查，`LLONG_MAX` 会被截成 `-1` 之类的值而蒙混过关。
* `max_tick` 不是 2 的幂时，`next <= max_tick_` 必不可少。
* `MAX_TICKS = 2^22` ⇒ `tree_` 最大 32 MB；`i` 用 `int` 足够。

100 万次操作（`-O2`，无 sanitizer）：`TickHistogram` 约 70 ms，`StreamingMedian` / `TwoHeapPercentile` / `WindowMedian` 都在 60 ms 以内，`OrderStatistics` 约 0.4 s。

## 7. 和 Java 版的区别

| 点 | Java | C++ |
|---|---|---|
| 堆 | `PriorityQueue<Long>`（装箱） | `std::priority_queue<long long>`（无装箱），最小堆要显式 `std::greater<>` |
| 清空堆 | `clear()` | 赋值一个新堆 |
| 溢出 | `Math.addExact` 抛异常 | `__builtin_add_overflow`；有符号溢出是 UB |
| 空 / 非法 | `NoSuchElementException` / `IllegalArgumentException` | `std::out_of_range` / `std::invalid_argument` |
| 树堆结点 | 数组 + 注意扩容后旧数组引用 | `vector` + 下标，不持有引用 |
| 零分配证明 | `ThreadMXBean` | 替换全局 `operator new` 计数 |
| `size()` | `int` | `std::size_t`：注意无符号减法下溢 |

## 8. 陷阱

1. `(a + b) / 2`、`std::abs(LLONG_MIN)`、`p * n`：有符号溢出 UB。
2. 无符号减法下溢：`lo_valid_ - hi_valid_ > 1`。
3. 平衡条件写反；`<` 与 `<=` 在重复值上的差别。
4. 惰性删除时用 `size()` 做平衡；一张 `delayed` 表共用；堆顶是失效元素时读中位数。
5. 升序流里堆无限增长（要重建）。
6. 百分位向下取整；`p = 0` / 101 没拒绝；先检查空还是先检查 p。
7. 递归插入时持有 `vector` 元素的引用。
8. 树状数组下标从 0 开始；`max_tick` 不是 2 的幂；先 `static_cast<int>` 再检查范围。
9. 有序输入使不平衡 BST 退化成链表（栈溢出）。

## 9. 面试官会追问什么（senior）

1. **偶数个数时中位数怎么定？** 下中位数：仍是整数 tick、真实价格、与 p50 一致；要平均数就返回两倍（整数）或带舍入规则的定点数；`(a + b) / 2` 溢出，写成 `a + (b − a) / 2`。
2. **为什么不直接用 `std::multiset`？** 加删 O(log n)，但取中位数要 `std::next(begin, n/2)`，O(n)；可以维护一个指向中位数的迭代器随加删微调（C++ 标准保证 `multiset` 迭代器在其它元素插入删除时不失效），但边界很细；两个堆更简单。
3. **滑动窗口的惰性删除内存怎么控？** 失效元素多了就重建；或换成支持按值删除的结构（`multiset` / 顺序统计树）。
4. **两个堆能算 p95 吗？** 能（`lo_` 装 `⌈0.95n⌉` 个）；但 p 固定。
5. **值域有界时？** 直方图 + 树状数组；预分配、零分配、缓存友好。T 太大就用树或近似草图（t-digest / HdrHistogram）。
6. **多线程？** 每线程一份局部结构，定期合并；直方图逐桶相加最容易；或单写者 + 发布快照。
7. **想要近似分位数？** t-digest / GK / 对数分桶：空间 O(1/ε)，误差有界。

## 10. 自测

**Q1** 依次加入 `7, 7, 1, 9`，每次之后的下中位数？

<details><summary>答案</summary>`7, 7, 7, 7`（`{1,7,7,9}` 的第 2 小是 7）。</details>

**Q2** `{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}` 的 p90、p50、p10？

<details><summary>答案</summary>排序 `1 1 2 3 3 4 5 5 6 9`，n = 10：p90 → 第 9 个 = 6；p50 → 第 5 个 = 3；p10 → 第 1 个 = 1。</details>

**Q3** 窗口 k = 2，流 `5, 9, 1, 4`，每步的窗口中位数？

<details><summary>答案</summary>`5, 5, 1, 1`。</details>

**Q4** `if (lo_valid_ - hi_valid_ > 1)` 有什么问题？

<details><summary>答案</summary>`lo_valid_` 和 `hi_valid_` 是无符号的；当 `lo_valid_ < hi_valid_` 时相减下溢成巨大的数，条件恒为真。应写成 `lo_valid_ > hi_valid_ + 1`。</details>

**Q5** 为什么树堆的递归插入里不能写 `auto& n = left_[t]; n = insert(n, x);`？

<details><summary>答案</summary>`insert` 里的 `push_back` 可能让 `left_` 重新分配，`n` 指向已释放的内存；之后的写入是 use-after-free。应先 `const int c = insert(left_[t], x);` 再 `left_[t] = c;`（参数按值传，且赋值时重新取元素）。</details>

**Q6** 价格范围 0 到 10^9，每秒 100 万次更新，要随时查 p99，选什么？

<details><summary>答案</summary>10^9 的直方图要 8 GB，太大。精确：顺序统计树；近似：对数分桶 / HdrHistogram / t-digest（空间小，误差有界）。先问精度要求。</details>
