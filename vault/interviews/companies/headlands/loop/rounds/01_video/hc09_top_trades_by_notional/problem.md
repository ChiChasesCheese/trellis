# hc09 · Top Trade Events by Notional（按名义金额取 top-k 成交 / ticker）

一天里交易所产生很多成交事件，每个事件的名义金额（notional）等于价格乘以数量。这个任务要你取名义金额最大的 k 个事件，再扩展到按 ticker 汇总、滑动窗口里的 top-k，以及多线程分块并行聚合。核心工具是大小为 k 的最小堆和有序集合，追问集中在 tie-break、溢出和多核结果是否一致。

## 读题前你需要知道

* **堆（heap）与「大小为 k 的最小堆」**：为什么取最大的 k 个要用*最小*堆；
* **哈希表聚合**（`HashMap.merge`）和 **有序集合**（`TreeSet`，红黑树）为什么能在 O(log n) 里「删旧键、插新键」；
* **整数溢出**和 `Math.multiplyExact`；
* **并行聚合**：为什么「各算各的、最后合并」不需要锁，以及 `parallel()` 流 / ForkJoin / `StructuredTaskScope` 各自是什么。

## 背景

一天里交易所产生了很多成交事件（trade event）。它们以三个**平行数组**（parallel arrays）给出：第 `i` 个事件是
`(tickers[i], prices[i], volumes[i])`。一个事件的 **notional**（名义金额）= `price × volume`。

* 价格用**整数 tick**（最小报价单位，比如 1 tick = 1 美分），数量用整数股数。所以 notional 是精确的 `long`，没有浮点误差。
  选整数，是因为「金额不能用 `double` 累加」是交易公司面试的老生常谈，而且后面的并行合并要靠整数加法的结合律。
* 价格 ≥ 0，数量 ≥ 0。乘法和累加都用 `Math.xxxExact`：**溢出就抛 `ArithmeticException`**，绝不静默回绕成负数。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `TopTrades.topEvents(tickers, prices, volumes, k)` | top-k 事件，大小为 k 的最小堆 + 完整 tie-break + 溢出检查；`topEventsSorted` 是排序基线 |
| 2 | `TopTrades.topTickers(...)` · `topOf` · `topTickersStream` · `summarize` | 按 ticker 聚合后取 top-k：HashMap + 堆 vs `groupingBy` + 排序；`teeing` 一趟算两个聚合 |
| 3 | `SlidingTopK`（`add` / `advanceTo` / `top` / `replay`） | 流式：事件按时间顺序到达，只看滑动窗口内的成交，旧成交过期 |
| 4 | `ParallelNotional`（`totalsParallelStream` / `totalsForkJoin` / `totalsScoped` / `totalsSharedMap` / `topTickersParallel`） | 数组切块并行聚合、最后合并；合并为什么正确、溢出怎么办 |

record / sealed 类型 `Trade`、`TickerTotal`、`Summary`、`SlidingTopK.Feed`（`Fill` / `Tick` / `Ask`）、`Answer` 在 starter 里已给出，签名以 starter 为准，这里只写语义。

## Part 1 · top-k 事件

`topEvents(String[] tickers, long[] prices, long[] volumes, int k)` → `List<Trade>`，按下面的顺序排列，最多 `k` 个：

1. notional **大**的在前；
2. notional 相同，`ticker` 字典序**升序**（`String.compareTo`）；
3. 再相同，数组下标 `index` **升序**。

三条规则合起来是**全序**——任意两个事件都有先后——所以结果唯一、可复现。`Trade(index, ticker, price, volume)` 带 `notional()`。

* `k` 大于事件数 → 返回全部；`k == 0` 或空输入 → 空列表；`k < 0` → `IllegalArgumentException`。
* 三个数组长度不等 → `IllegalArgumentException`；任一数组为 `null`、任一 ticker 为 `null` → `NullPointerException`；价格或数量为负 → `IllegalArgumentException`。
* **每一个事件**都要校验并计算 notional，*即使它进不了 top-k*：溢出一定会被发现（`Long.MAX_VALUE × 2` → `ArithmeticException`）。
* 输入数组不得被修改；返回的列表不可变。
* 复杂度要求：O(n log k) 时间、O(k) 额外空间；百万事件 < 2 s。随机顺序下绝大多数事件连堆都进不去——想想怎么做到**零分配**的快速拒绝。

### 样例

```
tickers = [AAPL, MSFT, AAPL, GOOG, MSFT, TSLA]
prices  = [18000, 40000, 18100, 14000, 40000, 25000]
volumes = [   10,     3,     5,     9,     3,     8]
notional=  180000 120000  90500 126000 120000 200000

topEvents(k=3) → [TSLA(i=5, 200000), AAPL(i=0, 180000), GOOG(i=3, 126000)]
topEvents(k=4) → 第 4 名是 i=1 而不是 i=4：二者 notional 与 ticker 都相同（MSFT, 120000），下标小的在前
```

## Part 2 · top-k ticker

`topTickers(tickers, prices, volumes, k)` → `List<TickerTotal>`：同一 ticker 的所有事件 notional 相加，取总额最大的 `k` 个；
总额降序，相同按 ticker 升序。累加用 `Math::addExact`——**每个事件都不溢出，合起来也可能溢出**，要报。没出现过的 ticker 不存在；出现过但总额为 0 的 ticker 存在（排在最后）。

| 方法 | 含义 |
|---|---|
| `topTickers` | `HashMap.merge` 聚合 O(n)，再对 m 个不同 ticker 用大小为 k 的堆 O(m log k) |
| `topOf(Map<String,Long>, k)` | 从现成的「ticker → 总额」表取 top-k（Part 4 合并后复用） |
| `topTickersStream` | `Collectors.groupingBy` + `reducing(addExact)` + `sorted().limit(k).toList()`，更短但整体排序 O(m log m) |
| `summarize` | `Collectors.teeing`：一趟遍历同时算「总额」和「最大事件」，合成 `Summary(grandTotal, Optional<Trade> largest)` |

```
topTickers(k=2) → [AAPL 270500, MSFT 240000]      （TSLA 200000, GOOG 126000 落选）
```

注意**最大的事件（TSLA）不属于最大的 ticker（AAPL）**——两个问题的答案不同，别混。

## Part 3 · 流式：滑动窗口 top-k ticker

成交事件按时间顺序一个个到达，面试官问：「如果数据是实时流，只关心最近 W 个时间单位内的成交，随时要能报出当前 top-k ticker，怎么做？」

`SlidingTopK(long window, int k)`：

| 方法 | 含义 |
|---|---|
| `add(Fill)` | `Fill(time, ticker, price, volume)`；先把时钟推进到 `time`（过期旧成交）再计入。`time` 比当前时间小 → `IllegalArgumentException`（相等允许） |
| `advanceTo(t)` | 只推进时钟（没有新成交，但旧成交要过期）；`t` 倒退 → IAE |
| `top()` | 窗口内 top-k ticker，排序规则同 Part 2 |
| `totalOf(ticker)` · `liveEvents()` · `distinctTickers()` · `now()` | 窗口内总额、活跃成交数、不同 ticker 数、当前时间 |
| `replay(window, k, List<Feed>)` | 回放一串 `Fill` / `Tick(time)` / `Ask(time)`，返回每个 `Ask` 的 `Answer(time, top)` |

* **窗口语义**：`now - time < window` 的成交是活的，`now - time >= window` 过期。也就是活跃区间 `(now - window, now]`，**恰好差 `window` 就过期**。
* 时间 ≥ 0；`window ≥ 1`；`k ≥ 0`。`add` 里总额溢出 → `ArithmeticException`，**ticker 的状态保持原样**（原子性）。
* 复杂度要求：每个事件 O(log m) 摊还（m = 窗口内不同 ticker 数），查询 O(log m + k)。
* 追问核心：**为什么只用 `PriorityQueue` 不行？**

### 样例（窗口 W = 10，k = 2）

```
F 1 AAPL 100 2     F 3 MSFT 50 10     F 5 AAPL 100 3     Q 5
F 12 TSLA 10 10    Q 12               Q 15               Q 40

Q 5  → [AAPL 500, MSFT 500]    并列按 ticker 升序
Q 12 → [MSFT 500, AAPL 300]    t=1 的 AAPL 200 已过期（12-1=11>=10）
Q 15 → [TSLA 100]              MSFT(t=3)、AAPL(t=5) 都过期（15-5=10>=10，边界算过期）
Q 40 → []
```

## Part 4 · 并行分块聚合

「数据有两千万条，单线程太慢了，怎么用多核？」——切成块，每块各自聚合成 `Map<String, Long>`，最后合并。

| 方法（`ParallelNotional`） | 含义 |
|---|---|
| `totalsSequential` | 顺序基线 |
| `totalsParallelStream` | `IntStream.range(0, n).parallel().collect(supplier, accumulator, combiner)` |
| `totalsForkJoin(…, threshold)` | `RecursiveTask` 递归对半切，区间不大于 `threshold` 就直接算，`fork` / `join` 后合并 |
| `totalsScoped(…, chunks)` | 每块一个虚拟线程，放进 `StructuredTaskScope.ShutdownOnFailure`；一块失败，其余被取消，抛出**原始**异常 |
| `totalsSharedMap(…, chunks)` | 对照组：所有线程往同一个 `ConcurrentHashMap` 里 `merge` |
| `topTickersParallel(…, k, chunks)` | `totalsScoped` + Part 2 的 `topOf` |

* 所有变体：结果与 `totalsSequential` **完全相同**（`Map.equals`），不论块数、线程调度、事件顺序。
* 校验与异常和顺序版一致：负数 → IAE，null → NPE，溢出 → `ArithmeticException`（来自单个事件、某一块的部分和、**或者合并两块时**——这三种都要报）。
  总额恰好等于 `Long.MAX_VALUE` 必须通过；比它大 1 必须报，不论怎么分块。
* 并发要求：多个线程同时调用同一个方法（读同一份数组）互不干扰；一个调用失败不影响别的调用。
* 追问核心：**合并为什么是对的？** 为什么价格用整数而不是 `double`？溢出的行为为什么与分块方式无关？

## 边界清单（隐藏测试会打的）

| 类别 | 例子 |
|---|---|
| 空 / 小 | 空数组；`k = 0`；`k > n`；单个事件 |
| tie | notional 相同 ticker 不同；notional 与 ticker 都相同；总额相同 |
| 零 | 价格或数量为 0 的事件合法，排在最后 |
| 溢出 | `Long.MAX_VALUE × 2`；`3037000499²` 通过而 `3037000500²` 溢出；同一 ticker 两个 `MAX/2+1`；恰好等于 `Long.MAX_VALUE` |
| 非法 | 数组长度不等；负价格；null ticker；`k < 0`；窗口 0；时间倒退 |
| 窗口 | 恰好 `window` 的边界；同一时间戳多笔；ticker 因过期被别人反超；总额溢出后状态不变 |
| 并行 | 块数多于事件数；块边界把同一 ticker 的两笔分开使得合并才溢出；打乱事件顺序结果不变 |

## 相关变体

* 浮点价格（`double`）：notional 用 `BigDecimal` 或先转整数 tick，避免累加误差。
* 「按成交量排序」「按 VWAP（成交量加权均价）排序」：VWAP = Σ(price×volume) / Σvolume，要小心整除与分母 0。
* top-k 在**每个 ticker 内部**（每只股票的前 k 笔最大成交）：`groupingBy` + 每组一个堆。
* 数据放不进内存：外部归并 / 分片按 ticker 哈希，每片各自 top-k，最后 k 路归并（接 hc02）。

## 考什么

Part 1 是 LeetCode 215 / 347 的「top-k」换了个皮：能不能说出**为什么用最小堆而不是最大堆**、tie-break 写没写全、
`price * volume` 会不会溢出（金融公司一定会问）。Part 2 看你会不会在「聚合」和「选择」之间选对数据结构。
Part 3 看你知不知道堆**不能删除任意元素**，以及有序集合如何补上这个洞。Part 4 看你对并行的理解是不是停在 `.parallel()` 三个字上：
合并的正确性（结合律、无共享可变状态）、溢出的单调性、取消是协作式的。
