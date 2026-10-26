# hc15 · 流式中位数与百分位（C++20 版）

成交价（`long long` 的整数 tick）一笔一笔到达，你要随时回答「到现在为止的中位数是多少」。从两个堆的经典做法开始，接着加上滑动窗口（只看最近 k 笔，堆不能删任意元素，要用惰性删除），再推广到任意百分位（p 固定用两个堆，p 在查询时才给要用顺序统计树），最后在价格范围有界时换成直方图。核心是四种结构各自的取舍，以及每种写法在边界上怎么出错。C++ 版的额外考点是：有符号溢出是未定义行为（undefined behavior，UB）、无符号减法下溢、递归插入时 `std::vector` 扩容让引用悬空。题目分 5 个小节（Part 1、2、3a、3b、4），签名都在 `starter.hpp`（命名空间 `median`）。

## 读题前你需要知道

- **中位数与百分位**：奇数个数取中间那个；偶数个数有两个候选，必须先约定取谁（见下）。
- **堆**（`std::priority_queue`）：默认是最大堆；最小堆要写 `std::priority_queue<long long, std::vector<long long>, std::greater<>>`。`top()` O(1)，`push` / `pop` O(log n)，不能删除任意元素。
- **惰性删除**（lazy deletion）：堆不能高效删任意元素时，先记账，等它浮到堆顶再弹。
- **树状数组**（Fenwick tree）：用数组存前缀计数，点加和「第 r 小」都是 O(log T)。
- **有符号溢出是 UB**：`(a + b) / 2`、`std::abs(LLONG_MIN)`、`p * n` 在极端值上都会触发，UBSan 会直接终止测试。要检查就用 `__builtin_add_overflow`。

## 约定（先定规则再写代码）

- **偶数个数时 `median()` 取下中位数**（第 ⌈n/2⌉ 小）。结果是真实出现过的价格、仍是整数 tick，并且等于 p = 50 的最近秩。
- **最近秩法**（nearest-rank）：n 个数的 p% 分位（`1 ≤ p ≤ 100` 的整数）是排序后第 `⌈p·n/100⌉` 小。`{15, 20, 35, 40, 50}`：P5 = 15，P30 = P40 = 20，P50 = 35，P100 = 50。
- 空结构上取值抛 `std::out_of_range`；参数非法抛 `std::invalid_argument`，并且**参数检查先于「是否为空」的检查**；`doubled_median` 溢出抛 `std::overflow_error`。

## 公共类型（starter 已给出）

```cpp
inline long long add_exact(long long a, long long b);      // __builtin_add_overflow，溢出抛 std::overflow_error
using MaxHeap = std::priority_queue<long long>;
using MinHeap = std::priority_queue<long long, std::vector<long long>, std::greater<>>;

// 最近秩：ceil(p * n / 100)。n < 0 或 p 不在 1..100 抛 std::invalid_argument。
// 已写好，且 n 再大也不溢出：把 n 拆成 n / 100 和 n % 100，而不是算 p * n。
inline long long nearest_rank(long long n, int p) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (p < 1 || p > 100) throw std::invalid_argument("p must be in 1..100");
    return n / 100 * p + ((n % 100) * p + 99) / 100;
}
```

## Part 1 · 两个堆：`StreamingMedian`

| 签名 | 要求 |
|---|---|
| `void add(long long)` | O(log n) |
| `long long median() const` | 下中位数，O(1)；空抛 `std::out_of_range` |
| `long long doubled_median() const` | 中位数的两倍：两个中间值之和（奇数个时是中间值乘 2）；和放不进 `long long` 抛 `std::overflow_error`；空抛 `std::out_of_range` |
| `std::size_t size() const noexcept` | 已加入的个数 |

starter 给的提示：`lo` 是较小的一半（最大堆），`hi` 是较大的一半（最小堆）；`lo` 里每个数 ≤ `hi` 里每个数，并且 `lo.size() == hi.size()` 或 `hi.size() + 1`。

- 依次加入 `5, 15, 1, 3`，每次之后的 `median()` 是 `5, 5, 5, 3`。
- 加入 `10, 42, 50`：`median()` 依次为 `10`（`{10, 42}` 取下中位数）、`42`。`{1, 2}` 的 `doubled_median()` 是 `3`；`{1, 2, 10, 20}` 是 `12`，此时 `median()` 是 `2`。
- 升序 `1..10` 的中位数序列是 `1, 1, 2, 2, 3, 3, 4, 4, 5, 5`；降序 `10..1` 是 `10, 9, 9, 8, 8, 7, 7, 6, 6, 5`。
- `[LLONG_MAX]` 和 `[LLONG_MIN]` 的 `doubled_median()` 抛 `std::overflow_error`；`[LLONG_MAX, LLONG_MIN]` 是 `-1`（不溢出）；再加一个 `5` 变成 `10`。`[LLONG_MAX, LLONG_MAX]` 抛异常，但 `median()` 仍是 `LLONG_MAX`。
- 查询不改变状态：连续调用 `median()` 结果不变。
- C++ 专属测试：`{LLONG_MAX - 1, LLONG_MAX}` 的 `median()` 是 `LLONG_MAX - 1`，`{LLONG_MIN, LLONG_MIN + 1}` 是 `LLONG_MIN`。`median()` 里不能出现 `(lo + hi) / 2` 或 `std::abs`。

## Part 2 · 滑动窗口：`WindowMedian`

| 签名 | 要求 |
|---|---|
| `explicit WindowMedian(int k)` | `k < 1` 抛 `std::invalid_argument` |
| `void add(long long)` | 摊还 O(log k)；窗口满了之后每加一个就挤掉最老的一个 |
| `long long median() const` | 窗口的下中位数；还没加过数抛 `std::out_of_range` |
| `std::size_t size() const noexcept` | `min(已加入个数, k)` |
| `std::size_t retained() const noexcept` | 两个堆里**实际占着**的元素个数（含还没清掉的失效元素），无论流多长都必须 ≤ 4k |
| `static std::vector<long long> slide(const std::vector<long long>&, int k)` | `result[i]` = 加入 `prices[0..i]` 之后的 `median()`；`k < 1` 抛 `std::invalid_argument`；空输入返回空 vector |

starter 给的提示：堆只能删堆顶，所以滑出窗口的旧值记进「待删」表，等它浮到堆顶再弹；平衡按**有效元素个数**，不是 `heap.size()`；每次 `add` 之后两个堆顶都必须有效；旧值属于 `lo` 当且仅当 `old <= lo.top()`。升序流里失效元素会沉在 `lo` 底部浮不上来，积多了要重建。

- `slide({1, 3, -1, -3, 5, 3, 6, 7}, 3)` 得 `{1, 1, 1, -1, -1, 3, 5, 6}`。
- `k = 3` 的窗口依次加 `10, 20` 后 `size()` 是 2、`median()` 是 `10`；再加 `30, 40, 50` 后 `size()` 是 3、`median()` 是 `40`。
- `k = 1` 就是最后一个价格：`slide({7, -2, 9, 9, 0}, 1)` 得 `{7, -2, 9, 9, 0}`。`k = 2` 是最近两个里较小的：`slide({5, 9, 1, 4, 3}, 2)` 得 `{5, 5, 1, 1, 3}`。`k` 大于流长度时等于 Part 1：`slide({5, 15, 1, 3}, 100)` 得 `{5, 5, 5, 3}`。
- 升序流：`k = 100`，加入 `0..99999`，整个过程中 `retained()` 的最大值 ≤ 400，最后 `median()` 是 `99949`（窗口 `99900..99999` 的第 50 小）。
- 所有结果都和「排序窗口后取下中位数」的慢实现对拍：随机流（取值范围 2 到 `LLONG_MAX`）、升序 / 降序 / 锯齿流、`LLONG_MAX` 与 `LLONG_MIN` 混合的窗口、大量重复值（旧值同时等于两个堆顶）。

## Part 3a · 固定百分位：`TwoHeapPercentile`

| 签名 | 要求 |
|---|---|
| `explicit TwoHeapPercentile(int p)` | `p` 不在 `1..100` 抛 `std::invalid_argument` |
| `void add(long long)` | O(log n) |
| `long long value() const` | 当前的 p 分位，O(1)；空抛 `std::out_of_range` |
| `long long size() const noexcept` | 已加入的个数 |

starter 给的提示：`lo` 装最小的 `nearest_rank(n, p)` 个数，`hi` 装其余。

- 流 `35, 20, 50, 15, 40`：`p = 5, 30, 40, 50, 100` 的 `value()` 依次是 `15, 20, 20, 35, 50`。
- `p = 90`：加入 `LLONG_MIN` 后 `value()` 是 `LLONG_MIN`；再加 `LLONG_MAX`，`n = 2`，rank 是 ⌈1.8⌉ = 2，`value()` 是 `LLONG_MAX`。
- `p = 50` 的 `value()` 在每一步都等于 Part 1 的 `median()`。`p` 取 `1, 2, 10, 25, 50, 66, 75, 90, 95, 99, 100`，每一步都和排序后取第 rank 个对拍。

## Part 3b · 任意百分位：`OrderStatistics`

| 签名 | 要求 |
|---|---|
| `static long long rank(long long n, int p)` | 就是 `nearest_rank`（已给出） |
| `void add(long long)` | 期望 O(log n) |
| `int size() const noexcept` | 已加入的个数 |
| `long long kth(long long rank) const` | 第 rank 小（从 1 起，重复值各算一个）；rank 不在 `1..size()` 抛 `std::invalid_argument` |
| `long long percentile(int p) const` | 最近秩百分位；`p` 不在 `1..100` 抛 `std::invalid_argument`（先于空检查）；空抛 `std::out_of_range` |
| `long long count_at_most(long long price) const` | 小于等于 `price` 的个数 |

starter 给的提示：标准库的 `std::set` / `std::map` 回答不了「第 k 小」（O(log n) 做不到）。要自己写一棵每个结点多存「子树元素总数」的平衡 BST，例如树堆（treap：按值排序的 BST，加按随机优先级排序的堆）；相同的值合并成一个带计数的结点；结点放在 `std::vector` 里，用下标当指针。

- `{35, 20, 50, 15, 40}`：`percentile(5, 30, 40, 50, 100)` 得 `15, 20, 20, 35, 50`，`size()` 是 `5`。
- 重复值 `{5, 1, 5, 3, 5, 3, 9}`：`kth(1..7)` 是 `1, 3, 3, 5, 5, 5, 9`；`count_at_most(0, 1, 2, 3, 5, 8, 9)` 依次是 `0, 1, 1, 3, 6, 6, 7`；`count_at_most(LLONG_MAX)` 是 `7`，`count_at_most(LLONG_MIN)` 是 `0`。
- `rank(n, p)` 表：`rank(0, 50) = 0`，`rank(1, 1) = 1`，`rank(3, 50) = 2`，`rank(7, 50) = 4`，`rank(101, 99) = 100`，`rank(20, 95) = 19`，`rank(200, 95) = 190`。
- `rank(LLONG_MAX, 100) = LLONG_MAX`，`rank(LLONG_MAX, 50) = 4611686018427387904`，`rank(LLONG_MAX, 1) = 92233720368547759`。`p = 0 / 101 / -5` 或 `n = -1` 抛 `std::invalid_argument`。
- 空结构：`percentile(50)` 抛 `std::out_of_range`，`percentile(0)` 和 `percentile(101)` 抛 `std::invalid_argument`，`kth(1)` 抛 `std::invalid_argument`，`count_at_most(5)` 是 `0`。只有一个数 `7` 时 `kth(0)`、`kth(2)`、`kth(-1)` 都抛 `std::invalid_argument`。
- `{LLONG_MAX, LLONG_MIN, 0, -1, 1, LLONG_MIN}`：`kth(1..6)` 是 `LLONG_MIN, LLONG_MIN, -1, 0, 1, LLONG_MAX`，`percentile(50)` 是 `-1`。
- 有序输入不能退化成链表：先加 `0..199999`，再加 `-1..-200000`，共 40 万次 `add` 要在 2 秒内完成。
- C++ 专属测试：插入 4000 个值（`i * 7919 % 4001`），迫使结点 `vector` 在递归插入的过程中多次重新分配；持有 `auto& n = nodes[t]` 这类引用的写法会在 AddressSanitizer 下报错。

## Part 4 · 价格有界：`TickHistogram`

| 签名 | 要求 |
|---|---|
| `explicit TickHistogram(int max_tick)` | `1 ≤ max_tick ≤ MAX_TICKS`（`MAX_TICKS = 1 << 22`），否则抛 `std::invalid_argument`；合法价格是 `0..max_tick-1` |
| `void add(long long price)` | 越界抛 `std::invalid_argument`，且不计数；O(log T) |
| `long long count() const noexcept` | 已计数的个数 |
| `long long count_at_most(long long price) const` | `price < 0` 得 0，`price >= max_tick` 得 `count()` |
| `long long kth(long long rank) const` | 第 rank 小；rank 不在 `1..count()` 抛 `std::invalid_argument` |
| `long long percentile(int p) const` | 语义同 `OrderStatistics::percentile` |
| `long long median() const` | 空抛 `std::out_of_range` |

starter 给的提示：计数放进树状数组；第 k 小用倍增下降——从最高位的 2 的幂往下，`tree[pos + step] < r` 就整段跳过，并从 `r` 里减掉。构造函数之后不许再分配内存。

- `max_tick = 100`，加入 `35, 20, 50, 15, 40`：`percentile(5, 30, 40, 50, 100)` 得 `15, 20, 20, 35, 50`，`median()` 是 `35`。
- `max_tick = 10`，加入 `5, 1, 5, 3, 5, 3, 9`：`kth(1..7)` 是 `1, 3, 3, 5, 5, 5, 9`；`count_at_most(0, 1, 3, 8, 9)` 依次是 `0, 1, 3, 6, 7`。
- `max_tick = 10`，加入 `0` 和 `9`：`count_at_most(-1)`、`count_at_most(LLONG_MIN)` 是 `0`；`count_at_most(10)` 和 `count_at_most(LLONG_MAX)` 是 `2`。
- `max_tick = 8` 时 `add(-1)`、`add(8)`、`add(LLONG_MAX)`、`add(LLONG_MIN)` 都抛 `std::invalid_argument`，之后 `count()` 仍是 `0`。空时 `median()` 和 `percentile(99)` 抛 `std::out_of_range`，`percentile(0)` 抛 `std::invalid_argument`。
- `max_tick = 1`：加 5 次 `0`，`median()` 和 `percentile(100)` 都是 `0`；`add(1)` 抛异常。`max_tick = MAX_TICKS`：加入 `0` 和 `MAX_TICKS - 1`，`median()` 是 `0`，`percentile(51)` 是 `MAX_TICKS - 1`。
- `max_tick` 取 `1, 2, 3, 7, 8, 9, 100, 1000, 1024, 1025`（含非 2 的幂），随机数据和排序对拍。
- C++ 专属测试：`max_tick = 1 << 16`，构造完成后做 20 万次 `add` + `percentile`，测试把全局 `operator new` 换成计数版，计数必须是 `0`。

## 性能测试（标签 `perf`）

数据是 100 万个、取值在 `0..2^20-1` 的近似正态分布价格。每项都和排序后的答案核对。

| 测试 | 限时 |
|---|---|
| `TickHistogram`（`max_tick = 2^20`）：100 万次 `add` + `percentile` | 1000 ms |
| `StreamingMedian`：100 万次 `add` + `median` | 2000 ms |
| `WindowMedian`（`k = 10000`）：100 万次 `add` + `median`，最后 `retained() <= 4k` | 2000 ms |
| `TwoHeapPercentile(95)`：100 万次 `add` + `value` | 2000 ms |
| `OrderStatistics`：100 万次 `add` + `percentile` | 3000 ms |

## 边界清单

- 空结构；单个元素；全部相同；升序 / 降序 / 锯齿
- `LLONG_MIN` / `LLONG_MAX`；`doubled_median` 溢出；中位数计算里不能有中点溢出
- 窗口 `k = 1 / 2`、`k` 大于流长度；旧值同时等于两个堆顶；升序流里堆不能无限增长
- `p = 1 / 100` 与 `p = 0 / 101`；`⌈p·n/100⌉` 向上取整；`n` 接近 `LLONG_MAX`；`rank = 0` / `size + 1`；空时先查 `p` 还是先查空
- `max_tick = 1`、非 2 的幂、`MAX_TICKS`；`price = -1 / max_tick`
- 有序输入下的树深度；递归插入时 `vector` 扩容

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc15_streaming_median          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc15_streaming_median --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc15_streaming_median --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc15_streaming_median                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 只要 Part 1，或者把「中位数」换成「第 k 大」（Top-k 流）、「众数」、「去重后的中位数」。
- 数据太多放不下：近似分位数（t-digest / HdrHistogram / 对数分桶）。
- 多线程：每个线程一份局部结构，定期合并；直方图逐桶相加最容易合并。
