# hc15 · Streaming Median（成交价的流式中位数与百分位）

成交价一笔一笔到达，你要随时回答「到现在为止的中位数是多少」。这个任务从两个堆的经典做法开始，接着加上滑动窗口（只看最近 k 笔，需要惰性删除），
再推广到任意百分位（p 固定用两个堆，p 任意用顺序统计树），最后在价格范围有界时换成直方图。核心是 4 种结构各自的取舍，以及每种写法在边界上会怎么错。
价格是整数 tick（`long`），不用浮点数。

## 读题前你需要知道

* **中位数**（median）与**百分位**（percentile）：奇数个取中间那个，偶数个有两个候选，需要约定；
* **堆**（heap / priority queue）：最大堆与最小堆各自 O(1) 取顶、O(log n) 插入与弹出；为什么「一个大顶堆 + 一个小顶堆」能把有序序列从中间切开；
* **惰性删除**（lazy deletion）：堆不能高效删除任意元素时，先记账、等它浮到堆顶再弹；
* **平衡二叉搜索树**与**树状数组**（Fenwick tree）：它们怎么回答「第 k 小」。

## 约定（先定规则再写代码）

* 价格是 `long` tick，Part 1–3 允许任意 `long`（包括负数、`Long.MIN_VALUE`）。
* **偶数个数时 `median()` 取下中位数**（lower median，第 ⌈n/2⌉ 小的那个）。理由：结果一定是真实出现过的价格、仍是整数 tick、而且等于 Part 3 的最近秩百分位 p = 50。
  需要真正的平均数时用 `doubledMedian()`：返回中位数的**两倍**（奇数个：2 × 中间值；偶数个：两个中间值之和），是整数，不需要舍入约定；和溢出 `long` → `ArithmeticException`。
* **最近秩法**（nearest-rank）：n 个数的 p% 分位（`1 ≤ p ≤ 100` 的整数）是排序后第 `rank = ⌈p·n/100⌉` 小的那个（`rank ≥ 1`）。
  例：`{15, 20, 35, 40, 50}`：P5 → 第 1 个 = 15；P30、P40 → 第 2 个 = 20；P50 → 第 3 个 = 35；P100 → 第 5 个 = 50。
* 空结构上取值 → `NoSuchElementException`（C++：`std::out_of_range`）；参数非法 → `IllegalArgumentException`（C++：`std::invalid_argument`）。**参数检查先于「是否为空」的检查**。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `StreamingMedian.add / median / doubledMedian / size` | 两个堆，O(log n) 加入、O(1) 取中位数 |
| 2 | `WindowMedian(k).add / median / size / retained`，`slide` | 最近 k 笔的滑动窗口中位数：惰性删除，堆的大小不随流增长 |
| 3 | `OrderStatistics.rank / add / kth / percentile / countAtMost`，`TwoHeapPercentile(p)` | 任意百分位：固定 p 用两个堆；p 在查询时才给，用顺序统计树 |
| 4 | `TickHistogram(maxTick)` + 100 万次操作的性能测试 | 价格有界时用树状数组直方图：O(log T)，构造后零分配 |

## Part 1 · 两个堆

`StreamingMedian`：

* `add(long price)`：O(log n)。
* `median()`：下中位数，O(1)；没有数据 → `NoSuchElementException`。
* `doubledMedian()`：见上；没有数据 → `NoSuchElementException`。`[MAX_VALUE]` 与 `[MIN_VALUE]` 的两倍都溢出；`[MAX, MIN]` 的下中位数 MIN + 上中位数 MAX = −1，不溢出。
* `size()`。查询不改变状态。

做法：`lo`（最大堆，较小的一半）+ `hi`（最小堆，较大的一半），不变式：`lo` 里每个数 ≤ `hi` 里每个数，且 `|lo| = |hi|` 或 `|hi| + 1`；`median()` 就是 `lo` 的堆顶。

样例：依次加入 `5, 15, 1, 3`，每次之后的 `median()`：

| 加入 | 已有（排序后） | `median()` | 说明 |
|---|---|---|---|
| 5 | `[5]` | 5 | |
| 15 | `[5, 15]` | 5 | 偶数个：下中位数（上中位数是 15） |
| 1 | `[1, 5, 15]` | 5 | |
| 3 | `[1, 3, 5, 15]` | 3 | 下中位数 3（上中位数 5） |

## Part 2 · 滑动窗口中位数

面试官问：「只看最近 k 笔成交呢？」

`WindowMedian(int k)`（`k ≥ 1`，否则 `IllegalArgumentException`）：

* `add(long price)`：窗口里放最近 `min(已加入个数, k)` 个价格，满了之后每加一个就挤掉最老的一个。摊还 O(log k)。
* `median()`：窗口的下中位数；还没有数据 → `NoSuchElementException`。`size()`：窗口里现在的个数。
* `static long[] slide(long[] prices, int k)`：`result[i]` = 加入 `prices[0..i]` 之后的 `median()`；`k < 1` → `IllegalArgumentException`；`prices == null` → NPE；空数组 → 空数组。
* `retained()`：两个堆里**实际占着**的元素个数（含还没被惰性清掉的失效元素）。要求**始终 ≤ 4k**，不随流的长度增长。

难点：堆只能删堆顶。惰性删除：滑出窗口的旧值记进「待删」表，等它浮到堆顶再真正弹出；两个堆按**有效元素个数**平衡（不是 `heap.size()`）；每次操作之后两个堆顶都必须是有效的。
旧值在哪个堆里？`lo` 里每个数 ≤ `hi` 里每个数，所以 `old ≤ lo.peek()` 就记在 `lo`。
惰性删除的代价：升序的流里，`lo` 的堆顶一直在变大，旧的小值永远沉在底下——不处理的话堆会长到 O(n)。失效元素太多时整体重建一次（至少隔 2k 次 add 才发生一次）。

样例 `slide({1, 3, -1, -3, 5, 3, 6, 7}, 3)` → `{1, 1, 1, -1, -1, 3, 5, 6}`：

| 加入后的窗口 | 排序后 | 下中位数 |
|---|---|---|
| `[1]` | `[1]` | 1 |
| `[1, 3]` | `[1, 3]` | 1 |
| `[1, 3, -1]` | `[-1, 1, 3]` | 1 |
| `[3, -1, -3]` | `[-3, -1, 3]` | -1 |
| `[-1, -3, 5]` | `[-3, -1, 5]` | -1 |
| `[-3, 5, 3]` | `[-3, 3, 5]` | 3 |
| `[5, 3, 6]` | `[3, 5, 6]` | 5 |
| `[3, 6, 7]` | `[3, 6, 7]` | 6 |

## Part 3 · 任意百分位

面试官问：「现在要 p95 呢？p 在查询时才给呢？」

`OrderStatistics`（顺序统计结构）：

* `static long rank(long n, int p)`：`⌈p·n/100⌉`；`n < 0` 或 `p ∉ 1..100` → `IllegalArgumentException`；`n` 很大时也不能溢出（不要先算 `p × n`：拆成 `n/100·p + ((n%100)·p + 99)/100`）。starter 里已给出。
* `add(long price)`：期望 O(log n)。`size()`。
* `kth(long rank)`：第 `rank` 小（从 1 起，重复的值各算一个）；`rank ∉ 1..size()` → `IllegalArgumentException`。
* `percentile(int p)`：最近秩百分位；`p ∉ 1..100` → `IllegalArgumentException`（先于空检查）；空 → `NoSuchElementException`。
* `countAtMost(long price)`：小于等于 `price` 的个数。
* 标准库没有现成的：`TreeMap` 不能按名次取。写一棵每个结点多存「子树元素总数」的平衡 BST（树堆 treap：BST + 随机优先级的堆）。
  相同的值合并成一个带计数的结点，用数组存结点（Java 里注意扩容后 `left[t] = insert(left[t], x)` 会写进旧数组）。有序输入也不能退化成链表。

`TwoHeapPercentile(int p)`（`1 ≤ p ≤ 100`，否则 `IllegalArgumentException`）：固定分位的两堆法——`lo` 装最小的 `rank(n, p)` 个数（最大堆），`hi` 装其余；
每次 `add` 之后 `rank` 最多加 1，所以最多挪一两个元素。`add` O(log n)，`value()` O(1)，空 → `NoSuchElementException`；`size()`。`p = 50` 就是 Part 1。

取舍：

| 结构 | 查询 | 适用 | 局限 |
|---|---|---|---|
| 两个堆 | O(1) | 一个固定的 p | p 在构造时固定；换 p 要重建 |
| 顺序统计树 | O(log n) | 任意 p、值域无界、需要 `kth` / 名次 | 实现最复杂，常数较大 |
| 直方图（Part 4） | O(log T) | 值域有界（tick 范围小） | 只能表示 `0..T-1`；内存 O(T) |

## Part 4 · 价格有界：`TickHistogram` 与 100 万次操作

面试官：「价格就是 0 到 100 万 tick，每秒几百万次更新，p99 随时要。」

`TickHistogram(int maxTick)`（`1 ≤ maxTick ≤ MAX_TICKS = 2^22`，否则 `IllegalArgumentException`）：合法价格 `0..maxTick-1`。

* `add(long price)`：越界 → `IllegalArgumentException`（且不计数）。O(log T)。
* `count()`；`countAtMost(price)`：`price < 0` → 0，`price ≥ maxTick` → `count()`；`kth(rank)`：同 `OrderStatistics`；`percentile(p)`、`median()`：语义同 `OrderStatistics.percentile`。
* **构造之后零分配**：100 万次 add + 查询中，预热后的分配 < 256 KB。
* 做法：计数放进树状数组（Fenwick tree），`add` 是单点加；第 r 小用倍增下降——从最高位的 2 的幂开始，`tree[pos + step] < r` 就整段跳过并从 `r` 里减掉。`maxTick` 不是 2 的幂也要对。

性能测试：每个结构 100 万次 add（带查询），限时 1–4 s（Java 与 C++ 的上限略有不同，以测试为准）；有序输入的 40 万次 add 2 s；`WindowMedian`（k = 10^4）全程 `retained() ≤ 4k`。每个结构的最终答案都和「排序后取第 rank 个」交叉检查。
`TwoHeapPercentile(95)` 3 s；`OrderStatistics` 4 s；有序输入的 40 万次 add 2 s。每个结构的最终答案都和「排序后取第 rank 个」交叉检查。

## 边界清单（隐藏测试多半打这些）

空结构；单个元素；全部相同；升序 / 降序 / 锯齿；负数与 `Long.MIN_VALUE` / `MAX_VALUE`；偶数个数时的下中位数；`doubledMedian` 溢出；
窗口 `k = 1`（最后一个价格）、`k = 2`（较小的那个）、`k` 大于流长度（等于 Part 1）；大量重复值（旧值同时等于两个堆顶）；升序流里堆不能无限增长；
`p = 1 / 100` 与 `p = 0 / 101`；`⌈p·n/100⌉` 向上取整（不是向下）；`n` 接近 `Long.MAX_VALUE`；`rank = 0` / `size + 1`；空时先查 p 还是先查空；
`maxTick = 1`、非 2 的幂、`maxTick = 2^22`；`price = -1 / maxTick`；有序输入下的树深度。

## 相关变体

* 变体可能只要 Part 1，或把「中位数」换成「第 k 大」（Top-k 流）、「众数」、「去重后的中位数」；也可能给整数流并在 `int` 范围里求「最接近平均数的价格」。
* 面试官常见追问：偶数个怎么办？为什么用两个堆而不是排序数组 / `TreeMap`？删除怎么做？数据太多放不下怎么办（近似：t-digest / HdrHistogram / 对数分桶）？多线程怎么合并？

## 考什么

先看你能不能把一个简单题的**规则**说清楚（偶数个取谁、分位怎么定义、边界怎么拒绝），再看你在加窗口后是否知道「堆不能删任意元素」并给出惰性删除，
最后是**取舍判断**：同一个问题有三种结构，按「p 是否固定、值域是否有界、要不要名次」选，并能说出各自的代价。
