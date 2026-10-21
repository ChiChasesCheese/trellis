# hc09 讲义 · Top Trade Events by Notional：从「全部排序」到「滑动窗口」再到「多核并行聚合」

> 读者：会写基本 Java（类、方法、循环、`ArrayList` / `HashMap`），没学过堆、有序集合、整数溢出、线程与并行；每个概念从零讲。

---

## 1. 这道题在问什么

**成交事件**（trade event）有股票代码（ticker，如 `AAPL`）、价格（price）、数量（volume），放在**三个平行数组**里：第 `i` 个事件是 `(tickers[i], prices[i], volumes[i])`。事件的 **notional**（名义金额）= 价格 × 数量，衡量「这笔成交有多大」（100 股 × 10 美元与 1 股 × 1000 美元都是 1000）。题目分四步升级：

1. **Part 1**：notional 最大的 `k` 个**事件**。
2. **Part 2**：同一股票的事件加起来，总 notional 最大的 `k` 只**股票**。
3. **Part 3**：数据实时流入，只关心最近一段时间（滑动窗口）内的成交，随时回答 top-k。
4. **Part 4**：几千万条数据，用多个 CPU 核一起算，结果和单线程**一模一样**。

### 手算一遍

```
下标      0      1      2      3      4      5
ticker  AAPL   MSFT   AAPL   GOOG   MSFT   TSLA
price  18000  40000  18100  14000  40000  25000
volume    10      3      5      9      3      8
notional 180000 120000  90500 126000 120000 200000     ← 价格 × 数量
```

* **Part 1，k = 3**：notional 从大到小：TSLA 200000（下标 5）、AAPL 180000（0）、GOOG 126000（3）、MSFT 120000（1 和 4）、AAPL 90500（2）。前 3 个：下标 5, 0, 3。
* **k = 4**：第 4 名 MSFT 120000，但下标 1 和 4 的 notional、ticker 都一样，规定再按下标升序，选**下标 1**。**没有这条规定答案就不唯一**——tie-break（打破平局）。
* **Part 2，k = 2**：AAPL = 270500；MSFT = 240000；TSLA = 200000；GOOG = 126000。前 2 名：AAPL、MSFT。**最大的单个事件是 TSLA，最大的 ticker 却是 AAPL**。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 平行数组（parallel arrays）

用几个**等长**数组表示一批记录，第 `i` 条记录是各数组第 `i` 个。`prices` 和 `volumes` 是 `long[]`，内存连续，CPU 缓存（cache）能一口气预取很多个——**局部性**（locality）好；`List<Trade>` 的对象散落堆各处要「追指针」。这是 SoA（Structure of Arrays，每字段一个数组），对比 AoS（每条记录一个对象）。例外：`String[] tickers` 是指针数组，按 ticker 聚合时仍要追指针。

```java
int n = tickers.length;                 // 三个数组等长，要先检查
for (int i = 0; i < n; i++) {
    long notional = prices[i] * volumes[i];   // 第 i 个事件
}
```

**代价**：数组间「对齐」靠约定，长度不等编译也过，所以先**检查等长**，不等抛 `IllegalArgumentException`。

### 2.2 为什么金额用整数 tick，不用 `double`

tick 是最小报价单位（美股常见 1 tick = 0.01 美元，`180.00` 存成 `18000`）。`double` 表示不了 0.1 这类小数，累加有误差，且**加的顺序不同结果不同**：

```java
double a = 0.1, b = 0.2, c = 0.3;
(a + b) + c   // 0.6000000000000001
a + (b + c)   // 0.6
```

浮点误差会把两个「应相等」的 notional 变成「谁大谁小」，**tie-break 失效**；Part 4 分块并行累加再合并，**合并顺序取决于线程调度**，浮点结果每次可能不同。整数加法满足**结合律**（`(a+b)+c == a+(b+c)`）和**交换律**，怎么分块、什么顺序合并都一样——这是 Part 4 正确的根本原因。价格、数量用 `long`（金融惯例：钱用整数最小单位，或 `BigDecimal`）。

### 2.3 整数溢出与 `Math.multiplyExact`

`long` 范围约 ±9.2 × 10¹⁸。结果超出时 Java **不报错，悄悄绕回去**：

```java
long x = Long.MAX_VALUE;         // 9223372036854775807
long y = x * 2;                  // -2 ！（绕回负数）
long z = Math.multiplyExact(x, 2L);   // 抛 ArithmeticException("long overflow")
```

绕回成负数的 notional 会让天价成交排到最后——**静默地给错答案**，在金融系统比崩溃更危险。所以乘法用 `multiplyExact`、累加用 `addExact`，溢出就抛（HotSpot 当**内联函数**处理，JIT 后通常是一条乘法加一次溢出检查，几乎无成本）。

**边界**：`Long.MAX_VALUE` 的平方根向下取整是 **3037000499**。`3037000499²= 9223372030926249001` 不溢出，`3037000500² = 9223372037000250000` 溢出。测溢出边界用这两个数。

### 2.4 top-k 与「大小为 k 的最小堆」

全排序再取前 k 个要 O(n log n) 且全放内存，但我们只要 k 个。**做法**：维护「目前最大的 k 个」，每来一个 x 看它是否比这 k 个里**最小的**大：不大 → 扔；大 → 踢掉最小的，x 加进来。需要「随时拿最小值、删最小值、插入」的结构——**最小堆**（min-heap）。**最大的 k 个要用最小堆**，反直觉但关键：堆顶是 k 个里最差的「守门员」，新来的要比守门员强才能进。

k = 3，流 `5, 1, 9, 3, 7, 8`（堆画成排序后，最左是堆顶即最小）：

```
来 5 :  堆未满，加入            堆 = [5]
来 1 :  堆未满，加入            堆 = [1, 5]
来 9 :  堆未满，加入            堆 = [1, 5, 9]        满了，守门员 = 1
来 3 :  3 > 1，踢掉 1，加入 3   堆 = [3, 5, 9]        守门员 = 3
来 7 :  7 > 3，踢掉 3，加入 7   堆 = [5, 7, 9]        守门员 = 5
来 8 :  8 > 5，踢掉 5，加入 8   堆 = [7, 8, 9]        守门员 = 7
结果（从大到小）: 9, 8, 7
```

每个元素最多一次插入 + 一次删最小，都 O(log k)，总共 **O(n log k)** 时间、**O(k)** 空间。k = 100、n = 10⁶ 时 log k 约 7（排序的 log n 约 20）；更重要的是**输入随机时绝大多数元素连堆都进不去**，只花一次比较。

堆是数组存的完全二叉树，父 ≤ 子，最小值在堆顶（下标 0）读取 O(1)。插入放末尾再**上浮**（与父比较，更小就交换）；删最小把末尾元素换到堆顶再**下沉**（与较小的子比较，更大就交换），都最多走树高 log₂ n 层。Java 是 `PriorityQueue`：

```java
var heap = new PriorityQueue<Integer>();   // 默认最小堆
heap.add(5);                // 插入 O(log k)
heap.peek();                // 看堆顶（最小）O(1)，空堆返回 null
heap.poll();                // 取出并删除堆顶 O(log k)，空堆返回 null
new PriorityQueue<>(cmp);   // 自定义顺序：cmp 认为「小」的在堆顶
```

### 2.5 比较器（`Comparator`）、全序与 tie-break

`compare(a, b)` 返回负数（a 排前）、0（平局）、正数（a 排后）。

**关键是「写全」**：只写「notional 大的在前」时，notional 相同的事件**谁在前未定义**（取决于堆内部实现和输入顺序）：`topEvents(k=4)` 的第 4 名可能是下标 1 或 4，写不出稳定期望；Part 4 并行后平局随线程调度而变——**不可复现的 bug 最难查**。**办法**：写成**全序**（total order）：任意两个不同事件比较结果必不是 0。规则链：

```
1. notional 降序      （大的在前）
2. ticker 升序        （String.compareTo，按 UTF-16 编码字典序）
3. 下标 index 升序    （下标全局唯一，所以第 3 条一定能分出胜负）
```

```java
Comparator<Trade> BEST_FIRST =
    Comparator.comparingLong(Trade::notional).reversed()   // 1. notional 降序
              .thenComparing(Trade::ticker)                // 2. ticker 升序
              .thenComparingInt(Trade::index);             // 3. 下标升序
```

⚠️ `reversed()` 反转它**前面**的整条链。`comparingLong(A).thenComparing(B).reversed()` 会把 B 也反过来，所以 `reversed()` 要紧跟第一个条件。

### 2.6 `HashMap.merge`：聚合的标准写法

`map.merge(key, value, f)`：key 不存在就放 `value`，存在就用 `f(旧值, value)` 替换。Part 2 要「同一 ticker 的 notional 加起来」。老写法：

```java
Long old = map.get(key);
map.put(key, old == null ? v : old + v);     // 两次哈希查找，还要手写 null 判断
```

`merge` 一行搞定，对 `ConcurrentHashMap` 还是**原子**的（Part 4 对照组用）：

```java
map.merge(ticker, notional, Math::addExact);   // Math::addExact 溢出时抛异常
```

哈希表：哈希函数把 key 映射成桶下标，冲突的 key 在桶内用链表（或树）串起，元素太多就扩容重新哈希，所以 `merge`/`get`/`put` 平均 O(1)。

### 2.7 有序集合 `TreeSet`：能「删掉任意一个、再放回去」

`TreeSet<E>` 按比较器排序（底层红黑树，自平衡二叉搜索树，树高 ≤ 2·log₂(m+1)），`add`、`remove`、`first`、按序遍历**每个操作 O(log m)**。

**Part 3 的核心**：堆只能高效取最小，而 ticker 总额会**变大**（新成交）也会**变小**（旧成交过期），要「找到它、改它的键」。`PriorityQueue.remove(Object)` 先线性扫描 O(m)，`TreeSet` 能 O(log m) 删任意元素：

```java
var set = new TreeSet<TickerTotal>(BEST_TICKER_FIRST);
set.add(new TickerTotal("AAPL", 500));
set.remove(new TickerTotal("AAPL", 500));   // 按比较器找到并删除，O(log m)
set.add(new TickerTotal("AAPL", 300));      // 以新键放回去
set.stream().limit(k).toList();             // 按顺序取前 k 个
```

⚠️ **TreeSet 用比较器判断「是不是同一个元素」**：`compare(a, b) == 0` 即同一个，`add` 会被拒绝。所以比较器必须是全序且和「身份」一致。`BEST_TICKER_FIRST`（总额降序 + ticker 升序）里 ticker 唯一，没问题；只看总额的话，总额相同的两个 ticker 会有一个被悄悄吞掉。

### 2.8 滑动窗口与 FIFO 队列的过期

只关心「最近 W 个时间单位」，左端之外的数据**过期**（expire）。事件**按时间顺序到达**，先到先过期（FIFO），过期只发生在队列最前面：`ArrayDeque` 队尾 `addLast`，队头 `peekFirst` 看最老的，过期就 `removeFirst`。每个事件**进一次、出一次**，过期总代价 O(n)，**摊还**（amortized，看一长串操作的总代价再平均）到每个事件 O(1) 次出队（每次出队还要付 TreeSet 的 O(log m)）。

### 2.9 并行：线程、数据竞争、结合律、ForkJoin、虚拟线程

**线程**是操作系统可同时调度的执行流，12 核机器真正并行跑 12 个线程。**并行**（parallelism）= 为更快而同时做多件事。

**数据竞争（data race）**：两线程同时读写同一变量，至少一个在写，又无同步。典型「丢失更新」：

```
线程 A: 读 total (=10)            线程 B: 读 total (=10)
线程 A: 算 10 + 5 = 15            线程 B: 算 10 + 7 = 17
线程 A: 写 total = 15
                                  线程 B: 写 total = 17      ← A 的更新丢了，应该是 22
```

`HashMap` 非线程安全，两线程同时 `put` 可能丢数据甚至损坏内部结构。三类办法：**加锁 / 并发容器**（`ConcurrentHashMap`，正确但线程互相等、扩展性差）；**不共享**（每线程用**私有**结构最后合并——Part 4 主方案，无竞争无需锁）；**不可变数据**（都只读同一份输入）。

**结合律（associativity）与「合并」**：分块算 `a + b` 的前提是怎么加括号结果都一样。整数加法满足，浮点不满足（2.2）；`Map` 合并只要加法满足结合律和交换律，合并顺序就无所谓。

**Fork/Join**（`ForkJoinPool`）：为「把大任务递归切成小任务」设计的线程池。

```
              compute(0..8)
              /            \
    fork: compute(0..4)   当前线程直接算: compute(4..8)
         /      \                 /        \
      ...        ...            ...         ...
```

`fork()` 把子任务放进当前工作线程自己的队列；`join()` 等结果（等时线程去执行别的任务）；**工作窃取**（work stealing）：队列空的线程从别的线程队列**另一端**（最老、通常最大的任务）偷任务，自动负载均衡。`parallel()` 流底层是 `ForkJoinPool.commonPool()`——**整个 JVM 共用的线程池**。

**虚拟线程与结构化并发**：Java 21 的轻量线程，几乎可一任务一线程；`StructuredTaskScope` 保证「try 块里 fork 的线程离开时一定都结束」，一个失败可取消其余。**Amdahl 定律**：必须串行的部分决定并行加速上限——本题「合并各块结果」是串行的，数据读取受内存带宽限制，所以并行不一定快（5.6）。

---

## 3. 从最笨的解法开始

### 3.1 Part 1：全部建对象，整体排序

```java
var all = new ArrayList<Trade>();
for (int i = 0; i < n; i++) all.add(new Trade(i, tickers[i], prices[i], volumes[i]));
all.sort(BEST_FIRST);
return all.subList(0, Math.min(k, n));
```

O(n log n) 时间，O(n) 空间（n 个约 32 字节的 `Trade` 对象加指针数组）。正确，是最好的**对拍基线**。**慢**：n = 10⁶、k = 100 时建 100 万个对象、做 100 万 × 20 次比较，只为 100 个：

| n = 10⁶，k = 100，5000 个 ticker，随机顺序 | 时间 |
|---|---|
| 全部排序（`topEventsSorted`） | 约 220 ms |
| 大小为 k 的最小堆（`topEvents`） | 约 2–14 ms（含 JIT 预热） |

### 3.2 Part 2：对每个 ticker 重新扫一遍

对每个不同 ticker 把整个数组扫一遍：O(n · m)，m = 10⁵、n = 10⁶ 就是 10¹¹，几十分钟。一次扫描 + `HashMap` 降到 O(n)（4.2）。

### 3.3 Part 3：每次查询都重算

每次问 top-k 都把所有「活着的」成交重新聚合再选，O(窗口大小)；窗口 10⁵ 笔、每秒 1000 次查询就是 10⁸ 次操作 / 秒。但它是最好的对拍基线（一定对）。

### 3.4 Part 4：一个线程算完

单线程 O(n)，2 千万事件约 0.2–4 秒（取决于不同 ticker 个数）。不是「错」而是「慢」，面试官想听怎么用多核。

---

## 4. 一步一步改进

### 4.1 Part 1

**第 1 步：只留 k 个，用最小堆**
排序为 n−k 个注定进不了前 k 的元素白付了钱。维护「目前最好的 k 个」，新元素只和其中最差的比（2.4）：每个元素至多一次堆插入和一次删除，O(log k)，堆大小恒为 k。`PriorityQueue<Trade>` 用 `BEST_FIRST.reversed()`（堆顶 = 最差）。O(n log k) 时间，O(k) 空间。

**第 2 步：快速拒绝（fast reject）**
* 随机顺序下堆满后几乎每个新元素都不如堆顶，却还 `new` 了 `Trade` 再比较。**先拿 long 和堆顶 notional 比**，严格小就 `continue`，连对象都不建；notional ≥ 堆顶才建对象走完整比较。正确因为 `BEST_FIRST` 第一条就是 notional 降序。
* 效果：随机输入**零分配**，主循环是「两次数组读取 + 一次乘法 + 一次比较」。最坏：notional 严格递增时每个元素都进堆，退化到真正的 O(n log k)：n = 10⁶、k = 1000 约 120 ms（随机顺序只要几毫秒）。

**第 3 步：全序 tie-break**
* 比较器三级（notional、ticker、index），「新元素比堆顶好」用 `BEST_FIRST.compare(t, heap.peek()) < 0`。index 全局唯一，比较器永不返回 0，结果唯一。
* 易错：快速拒绝必须**严格小于**；写成 `<=` 会把「notional 相同但 ticker 更小」的更好事件也拒掉（下标 1 对下标 4 的样例会错）。

**第 4 步：溢出与输入检查**
* 乘积可能溢出，数组可能有 null、负数。所有事件（包括进不了 top-k 的）都经过同一个 `notionalAt(i)`：检查非空、非负，再 `Math.multiplyExact`。每个事件都检查，因为「是否抛异常」不该依赖数据排列（只查进堆的，溢出事件会在快速拒绝那步被误算）。
* `Trade` 紧凑构造器里再 `multiplyExact` 一次，保证「`Trade` 存在 ⇒ `notional()` 不溢出」，`notional()` 内部可直接 `price * volume`。

**第 5 步：输出顺序**
* 堆「最差先出」，`poll` 出来从差到好；`ArrayList.reversed()`（Java 21）得从好到差，再 `List.copyOf` 变不可变。备选：`new ArrayList<>(heap)` 再 `sort(BEST_FIRST)`，O(k log k)。

### 4.2 Part 2

**第 1 步：一趟扫描 + `HashMap.merge`**
```java
var totals = new HashMap<String, Long>();
for (int i = 0; i < n; i++) totals.merge(tickers[i], notionalAt(i), Math::addExact);
```
期望 O(n)。`addExact` 保证「每个事件都不溢出但加起来溢出」也被发现。

**第 2 步：对 m 个不同 ticker 取 top-k**
(a) 全排序 `O(m log m)`；(b) 大小为 k 的最小堆 `O(m log k)`。m = 10⁵、k = 50 时堆版约 41–58 ms，Stream（排序）版约 82–103 ms，都够快：堆版展示「k 小时不排序全部」，Stream 版展示「写得短」。`topOf(Map, k)` 抽成独立方法，Part 4 合并后复用。

**第 3 步：Stream 版和 `teeing`**
```java
// groupingBy + reducing 聚合
Map<String, Long> totals = IntStream.range(0, n).boxed().collect(
    Collectors.groupingBy(i -> tickers[i], Collectors.reducing(0L, i -> notionalAt(i), Math::addExact)));
// 一趟遍历同时算「总额」和「最大事件」
Collectors.teeing(
    Collectors.reducing(0L, Trade::notional, Math::addExact),
    Collectors.minBy(BEST_FIRST),
    Summary::new)
```
`teeing` 把同一个流同时喂给两个收集器，再用第三个参数合并结果（老写法要遍历两次或手写累加器类）。Stream 版比手写循环慢：`IntStream.boxed()` 装箱，`groupingBy` 有中间容器。

### 4.3 Part 3（流式 + 过期）

**第 1 步：为什么只用堆不行**

窗口里 A 总额 500、B 300、C 100，k = 2，堆 {A, B}（堆顶 B = 300，守门员）。
* 事件 1：C 来一笔变 400，比守门员强 → 踢掉 B，C 进堆。**但 B 还在窗口里**，只是被挤出堆，堆不再记得它。
* 事件 2：A 的老成交过期，A 从 500 降到 50。B（300）应回到 top-2，可堆里没有 B 了。**必须重建**。

根本原因：堆高效支持 `add` 和「弹出堆顶」，但不支持：**找到任意元素**（线性扫描）、**改一个元素的键**（`PriorityQueue` 没有 decrease-key）、**删除任意元素**（`remove(Object)` O(m)）。三种补救：

| 方案 | 做法 | 代价 |
|---|---|---|
| A. 查询时重建堆 | 每次 `top()` 把所有活跃 ticker 过一遍选 top-k | 每次查询 O(m log k) |
| B. 惰性删除（lazy deletion） | 总额变化时不删旧条目，只**再插一条新的**；弹出时发现与 `totals` 当前值不符就丢弃 | 堆里累积垃圾，可到 O(事件数)；`top()` 要弹 k 个有效条目再放回 |
| C. 有序集合 `TreeSet` | 总额变化：O(log m) 删旧键、O(log m) 插新键；`top()` 直接按序读前 k 个 | 红黑树常数比堆大；但所有操作有上界 |

选 C：查询要看前 k 个而非仅堆顶，且要任意元素更新，有序集合最自然。

**第 2 步：数据结构设计**

```
ArrayDeque<Fill> live          按时间顺序的活跃成交（队头最老）
HashMap<String, Acc> totals    ticker → (窗口内总额, 窗口内活跃成交笔数)
TreeSet<TickerTotal> ranking   所有活跃 ticker，按 (总额 降序, ticker 升序)
                               —— 与 totals 保持一一对应
```

* `Acc.count`（活跃笔数）：总额可能为 0（价格或数量为 0），不能用「总额 == 0」判断「还有没有活跃成交」；count 减到 0 才从两张表里删掉。

**第 3 步：三个操作**

* `add(fill)`：
  1. `advanceTo(fill.time)` 推进时钟，先让旧成交过期；
  2. 取该 ticker 旧总额 `old`，算 `new = Math.addExact(old, fill.notional)`——**这一步先做，溢出就抛，此时还没动任何结构**（原子性）；
  3. `ranking.remove(TickerTotal(ticker, old))`，更新 `totals`，`ranking.add(TickerTotal(ticker, new))`，`live.addLast(fill)`。
* `advanceTo(t)`：`t` 不能小于当前时间；当 `队头.time` 满足 `now - time >= window` 就 `removeFirst`，对应 ticker 做「减总额、`ranking` 删旧键、（count 不为 0 就）插新键」。
* `top()`：`ranking.stream().limit(k).toList()`，O(log m + k)。

**为什么 `now - time >= window` 而非 `time + window <= now`**：时间很大时 `time + window` 会溢出，`now - time` 不会。每个事件进出一次，每次 O(log m)；查询 O(log m + k)。

**第 4 步：时钟与「Tick / Ask」**：`replay` 把 `Fill`、`Tick`（时钟前进）、`Ask`（询问）封装成 sealed 接口 `Feed`，用模式匹配 `switch` 分派。`Ask(t)` 也先推进时钟，所以「在 t 时刻问」等价于「先 Tick(t) 再问」。

### 4.4 Part 4（并行分块）

**第 1 步：切块、各算各的、最后合并**

```
          事件 0 ........................... n-1
 切块:    [chunk 0][chunk 1][chunk 2]  ...  [chunk C-1]
              |        |        |                |
           私有 Map  私有 Map  私有 Map  ...   私有 Map     ← 各线程只写自己的
              \        |       /                 /
               ──────  合并（串行）  ──────────────
                           ↓
                   Map<String, Long>
```

**合并为什么对**（面试官想听的三点）：

1. **整数加法满足结合律和交换律**：任意分块和合并顺序，和都相同（对照 2.2 的 `double` 反例）。
2. **没有共享可变状态**：每块的 `Map` 只被一个任务写，所有任务只读同一份输入，无数据竞争、不需锁。`mergeInto(a, b)` 合并时两张表都没人在写（子任务已完成：`join()` 建立 happens-before，保证合并线程看到子任务写的所有内容）。
3. **溢出行为与分块无关**：所有 notional 非负，任何部分和 ≤ 总和。总和 ≤ `Long.MAX_VALUE` 则**任何**部分和、合并都不溢出；总和 > `Long.MAX_VALUE` 则无论怎么分块，*某个*步骤（至少最后一次合并）一定溢出——「是否抛 `ArithmeticException`」只取决于数据。（这靠**非负性**；允许负数——撤销、卖出——中间和可能先爆再回来，异常与否就依赖顺序，本题明确非负就为此。）

**第 2 步：四种实现**

| 实现 | 切块方式 | 合并方式 | 特点 |
|---|---|---|---|
| `totalsParallelStream` | 框架自动 | `collect` 的 combiner | 最短；用公共线程池；combiner 必须改第一个参数 |
| `totalsForkJoin` | 递归对半，小于 `threshold` 停 | `join()` 后 `mergeInto` | 粒度可控；显式任务树 |
| `totalsScoped` | 固定 `chunks` 块，每块一个虚拟线程 | 全部 `join` 后按序合并 | 失败即取消其余；异常原样抛出；生命周期受 try 块限制 |
| `totalsSharedMap` | 固定 `chunks` 块 | 无合并：所有线程直接 `merge` 进一张 `ConcurrentHashMap` | 对照组；无合并代价但有争用 |

**第 3 步：错误处理与取消**

* 一块出异常（溢出、负数）时，`ShutdownOnFailure` 关闭 scope 并**中断**其余子线程。中断是**协作式**的——只设标志，不强行停止，所以 `accumulate` 每 4096 个事件检查一次 `isInterrupted()`，被中断就抛 `CancellationException`；否则其余块算完才返回，取消形同虚设。
* 异常要**原样**抛给调用者（每种实现都应收到同一个 `ArithmeticException`）：`throwIfFailed(e -> e instanceof RuntimeException re ? re : new IllegalStateException(e))`，运行时异常原样抛，否则包一层。

---

## 5. 逐段讲解法

### 5.1 数据类型与比较器（`TopTrades.java`）

```java
public record Trade(int index, String ticker, long price, long volume) {
    public Trade {
        Objects.requireNonNull(ticker, "ticker");
        if (index < 0) throw new IllegalArgumentException("index must be >= 0: " + index);
        if (price < 0) throw new IllegalArgumentException("negative price: " + price);
        if (volume < 0) throw new IllegalArgumentException("negative volume: " + volume);
        Math.multiplyExact(price, volume);
    }
    public long notional() { return price * volume; }
}
```

* `record` 不可变，自动生成 `equals / hashCode / toString`，可直接比较两个列表。**紧凑构造器**在字段赋值之前运行，校验都放这里——非法 `Trade` 构造不出来。
* 构造器里 `multiplyExact` 但**丢弃结果**，只为「提前证明不溢出」，使 `notional()` 里的普通乘法安全。小技巧：*把检查移到对象创建时，后面所有使用都不用再担心*。

```java
public static final Comparator<Trade> BEST_FIRST =
        Comparator.comparingLong(Trade::notional).reversed()
                .thenComparing(Trade::ticker)
                .thenComparingInt(Trade::index);
```

先按 `notional` 比较 → `reversed()` 反过来（大的在前）→ 平局按 `ticker` → 再平局按 `index`。`public static final`：Part 3 的 `TreeSet` 也复用 `BEST_TICKER_FIRST`。

### 5.2 `topEvents`

```java
var heap = new PriorityQueue<Trade>(Math.max(1, Math.min(k, n)), BEST_FIRST.reversed());
for (int i = 0; i < n; i++) {
    long notional = notionalAt(tickers, prices, volumes, i);
    if (k == 0) continue;
    if (heap.size() == k && notional < heap.peek().notional()) continue;   // 快速拒绝
    var t = new Trade(i, tickers[i], prices[i], volumes[i]);
    if (heap.size() < k) {
        heap.add(t);
    } else if (BEST_FIRST.compare(t, heap.peek()) < 0) {   // t 比堆顶「更好」
        heap.poll();
        heap.add(t);
    }
}
var worstFirst = new ArrayList<Trade>(heap.size());
while (!heap.isEmpty()) worstFirst.add(heap.poll());
return List.copyOf(worstFirst.reversed());
```

* 比较器取 `BEST_FIRST.reversed()`：`PriorityQueue` 把「最小」放堆顶，反过来后「最小」= 「最差」，堆顶是守门员。初始容量 `max(1, min(k, n))`（不能为 0，也没必要大于 `n`）。
* `k == 0` 时仍走一遍 `notionalAt`（校验），但不碰堆。`BEST_FIRST.compare(t, heap.peek()) < 0` 表示 t 排堆顶前面，即「更好」。
* 不用 `heap.add(t); if (heap.size() > k) heap.poll();`：也对且更短，但每个元素都做两次堆操作；上面的写法只在真会改变堆时才操作。
* `worstFirst.reversed()` 是 `ArrayList` 的**视图**，`List.copyOf` 变成独立的不可变副本。

### 5.3 `topTickers` 与 `topOf`

```java
public static List<TickerTotal> topOf(Map<String, Long> totals, int k) {
    if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
    if (k == 0) return List.of();
    var heap = new PriorityQueue<TickerTotal>(Math.min(k, Math.max(1, totals.size())), BEST_TICKER_FIRST.reversed());
    for (var e : totals.entrySet()) {
        var cand = new TickerTotal(e.getKey(), e.getValue());
        if (heap.size() < k) heap.add(cand);
        else if (BEST_TICKER_FIRST.compare(cand, heap.peek()) < 0) { heap.poll(); heap.add(cand); }
    }
    ...
}
```

与 `topEvents` 同一模式，元素换成 `TickerTotal`（不做 `long` 快速拒绝，因 `Map.Entry` 已是现成对象）。溢出在 `merge(…, Math::addExact)` 时已检查过。

### 5.4 `SlidingTopK`

```java
public void add(Fill f) {
    advanceTo(f.time());
    var acc = totals.get(f.ticker());
    long oldTotal = acc == null ? 0 : acc.total;
    long newTotal = Math.addExact(oldTotal, f.notional());     // 先算：溢出就抛，还没动任何结构
    if (acc == null) { acc = new Acc(); totals.put(f.ticker(), acc); }
    else ranking.remove(new TickerTotal(f.ticker(), oldTotal)); // 删旧键
    acc.total = newTotal;
    acc.count++;
    ranking.add(new TickerTotal(f.ticker(), newTotal));         // 插新键
    live.addLast(f);
}
```

* **操作顺序**是正确性的一部分：`ranking.remove` 必须在 `acc.total` 改成新值**之前**，否则用新值找不到旧键（按比较器是另一个位置），旧键残留，`ranking` 里同一 ticker 出现两次。
* `Acc` 是可变类而非 `record`：每个活跃成交都要更新，建新 record 会产生大量垃圾；可变状态局限在 `private static final class`，不外泄。

```java
while ((f = live.peekFirst()) != null && now - f.time() >= window) {
    live.removeFirst();
    var acc = totals.get(f.ticker());
    ranking.remove(new TickerTotal(f.ticker(), acc.total));
    acc.total -= f.notional();
    acc.count--;
    if (acc.count == 0) totals.remove(f.ticker());
    else ranking.add(new TickerTotal(f.ticker(), acc.total));
}
```

* `acc.total -= f.notional()` 不会溢出（`total` 是若干非负数之和，减去其中一个）。

```java
public static List<Answer> replay(long window, int k, List<? extends Feed> feed) {
    ...
    switch (f) {
        case Fill fill -> w.add(fill);
        case Tick(var t) when t == w.now() -> { }
        case Tick(var t) -> w.advanceTo(t);
        case Ask(var t) -> { w.advanceTo(t); answers.add(new Answer(t, w.top())); }
    }
```

* `Feed` 是 `sealed interface ... permits Fill, Tick, Ask`，`switch` 不需 `default`；新增子类型时所有没处理的 `switch` 编译失败。`case Tick(var t)` **记录模式**一步完成「判断类型 + 解构」。
* `when t == w.now()` **守卫**：时钟没动就什么都不做。带守卫的 `case Tick(var t) when …` 必须在不带守卫的 `case Tick(var t)` **之前**，否则被遮蔽，编译器报「dominated」。

### 5.5 `ParallelNotional`

**并行流版：**

```java
return IntStream.range(0, n).parallel().collect(
        HashMap<String, Long>::new,                                               // supplier：每个线程自己的新容器
        (m, i) -> m.merge(tickers[i], notionalAt(...), Math::addExact),           // accumulator：往本线程容器加一项
        (left, right) -> right.forEach((k, v) -> left.merge(k, v, Math::addExact)));   // combiner：把 right 并进 left
```

* `collect` 的**契约**：supplier 每次产生**新的、互不共享的**容器；accumulator 只改传给它的容器；combiner 把第二个容器并进**第一个**。
* **最常见的 bug**：combiner 写反成 `left.forEach(... right.merge ...)`——`BiConsumer` 没有返回值，框架认为结果在第一个参数里，写反就丢了 left。另一个 bug：supplier 写成 `() -> sharedMap`，回到数据竞争。

**ForkJoin 版：**

```java
protected Map<String, Long> compute() {
    if (to - from <= threshold) { var m = new HashMap<String, Long>(); accumulate(m, ..., from, to); return m; }
    int mid = (from + to) >>> 1;
    var left = new Sum(..., from, mid, threshold);
    var right = new Sum(..., mid, to, threshold);
    left.fork();                 // 左半边放进队列，别的线程可以偷
    var r = right.compute();     // 右半边自己算（不要 fork 两个再 join 两个：浪费一个线程）
    var l = left.join();         // 等左半边
    return mergeInto(l, r);
}
```

* `threshold`：太小 → 创建任务开销超过计算；太大 → 并行度不够。经验是任务总数约为核数的 4–8 倍。
* `(from + to) >>> 1`：两个接近 `int` 上限的下标相加溢出成负数，`>>> 1` 在位模式上仍正确（经典二分查找 bug，`Arrays.binarySearch` 2006 年修过）。

**结构化并发版：**

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("totals", Thread.ofVirtual().factory())) {
    var subtasks = new ArrayList<StructuredTaskScope.Subtask<Map<String, Long>>>(chunks);
    for (int c = 0; c < chunks; c++) {
        final int from = boundary(n, chunks, c), to = boundary(n, chunks, c + 1);
        subtasks.add(scope.fork(() -> { var m = new HashMap<String, Long>(); accumulate(m, ..., from, to); return m; }));
    }
    scope.join();
    scope.throwIfFailed(e -> e instanceof RuntimeException re ? re : new IllegalStateException(e));
    Map<String, Long> acc = subtasks.getFirst().get();
    for (int c = 1; c < subtasks.size(); c++) acc = mergeInto(acc, subtasks.get(c).get());
    return acc;
}
```

* `scope.fork(callable)` 在新虚拟线程里跑任务，返回 `Subtask`（一个「承诺」）；`scope.join()` 等所有子任务结束**或**一个失败（之后 scope 关闭、其余被中断）。
* `scope.throwIfFailed(...)` 有失败就抛。**不调用它**，失败异常会被悄悄忽略，之后 `subtask.get()` 抛 `IllegalStateException`。
* `boundary(n, chunks, c)` = `(int) ((long) n * c / chunks)`：`n = 2×10⁹`、`c = 4` 时 `n * c` 超过 `int`，必须先转 `long`；块 c 是 `[boundary(c), boundary(c+1))`，首尾相接不重叠不遗漏。
* **预览 API**（JEP 453）：需 `--enable-preview`；后续版本 API 有不兼容改动，口头说明。

**共享 Map 版（对照组）：**

```java
shared.merge(tickers[i], notionalAt(...), Math::addExact);   // ConcurrentHashMap：对单个 key 原子
```

对一个 key `merge` 是原子的，函数抛异常时不记录映射，溢出也能检测。但热点 ticker（如 AAPL 占 30% 成交）上所有线程抢同一个桶的锁，扩展性差。

---

### 5.6 数据：并行到底快不快（12 核，JDK 21，Generational ZGC，噪声较大，仅看数量级）

| 场景 | 顺序 | `parallel()` 流 | ForkJoin | `Scoped` | 共享 Map |
|---|---|---|---|---|---|
| 2×10⁶ 事件，5×10⁴ ticker | 约 45 ms | 约 30–110 ms | 约 30–65 ms | 约 40–75 ms | 约 20–55 ms |
| 2×10⁷ 事件，200 个 ticker | 约 210–330 ms | 约 75–110 ms | 约 55–215 ms | 约 75–250 ms | 约 300–350 ms |
| 2×10⁷ 事件，2×10⁶ ticker | 约 2.4–4.2 s | 约 1.6–5.3 s | 约 2.1–3.0 s | 约 1.9–4.4 s | 约 0.8–0.9 s |

1. **并行不免费**：事件不多（2×10⁶）时调度、合并开销抵消收益。
2. **ticker 很少（200）**：每块 Map 很小，合并几乎免费，`parallel()` 流 2–3 倍加速；共享 Map 反而**更慢**（所有线程抢 200 个桶）。
3. **ticker 极多（2×10⁶）**：每块私有 Map 巨大，串行合并成瓶颈（Amdahl）；共享 `ConcurrentHashMap` 不用合并反而最快。

**结论**：「分块 + 私有结果 + 合并」是默认方案（无共享状态、正确性易证），收益取决于合并成本 ≈ 不同 key 个数；key 极多时可按 key 哈希分区（合并变简单拼接）或用共享并发 Map。**先测，再选**。

---

## 6. Java 21 特性小课

### record 与紧凑构造器

旧写法（Java 8）：`final` 类 + 私有字段 + 构造器校验 + getter + 手写 `equals/hashCode/toString`，约 40 行；新写法一行 `record Trade(int index, String ticker, long price, long volume)` 加紧凑构造器校验。**不该用**：需要可变字段（如 `Acc`）或继承别的类时。

### sealed 接口 + 模式匹配 switch + 记录模式

旧写法 `if (f instanceof Fill) { Fill x = (Fill) f; ... } else if ... else throw`——强转、重复、编译器不查漏。新写法 `switch (f) { case Fill fill -> ...; case Tick(var t) -> ...; case Ask(var t) -> ... }`：查穷尽性，同时判断类型和解构，`when` 写附加条件。

### Sequenced Collections、Stream 新工具

`reversed()` 取倒序**视图**（改原列表它也变；要独立副本 `List.copyOf`）；`getFirst() / getLast()` 取两端（旧写法 `list.get(list.size() - 1)`、`Collections.reverse(copy)` 啰嗦或要复制）。`stream.toList()`（Java 16）返回不可变列表；`teeing`（Java 12）一趟喂两个收集器。**不该用**：热路径简单聚合手写循环更快；`teeing` 的两个收集器有顺序依赖就别用。

### 精确算术与 Comparator 组合子

`Math.multiplyExact / addExact` 溢出就抛（旧写法 `r = a * b; if (a != 0 && r / a != b) throw ...` 多一次除法还易错）。`comparingLong(...).reversed().thenComparing(...).thenComparingInt(...)` 一条链写出全序（对照 Java 7 匿名类里一串 `if`）。

### 虚拟线程与结构化并发（预览）

`Thread.ofVirtual().factory()` + `StructuredTaskScope.ShutdownOnFailure`：旧写法 `ExecutorService` + `Future` 列表，一个失败其余不取消，忘 `shutdown` 线程泄漏；新写法生命周期绑定 try 块。**不该用**：CPU 密集的分块任务用虚拟线程不比平台线程快（它擅长**阻塞 I/O**），选它是为展示取消语义。

---

## 7. 追问预演

**问：为什么求最大的 k 个要用最小堆？**
* 要替换的是「k 个里最差的」，所以堆顶必须最差，即最小堆：O(1) 找到，O(log k) 替换。最大堆装全部（heapify O(n) 再弹 k 次）也能做，但要 O(n) 空间且不能流式。
* 说出口：「最大的 k 个用最小堆，堆顶是守门员；新来的比它强才能进来。O(n log k)、O(k)，还能流式。」

**问：n 很大、k 很小，还能更快吗？**
* 随机顺序下堆满后期望只有 O(k log(n/k)) 个元素进堆，绝大多数一次 `long` 比较被拒，接近 O(n)。再快：quickselect（期望 O(n)，要可修改数组、不能流式）或并行分块各自 top-k 再合并（全局 top-k 一定在各块 top-k 的并集里）。

**问：notional 溢出怎么办？为什么不用 `double` / `BigInteger`？**
* `Math.multiplyExact` 溢出就抛，不给错答案。`double` 53 位尾数，大数丢精度、累加不满足结合律。`BigInteger` 放得下任何数但每次运算分配对象，慢几十倍；业务必须容纳溢出后的大数时只用在检测到溢出的慢路径。

**问：Part 3，为什么不用堆？用堆能不能做？**
* 见 4.3：堆没有 decrease-key，也不能高效删任意元素；惰性删除时堆里垃圾可累积到 O(事件数)；`TreeSet` 每个操作有 O(log m) 上界。
* 说出口：「ticker 总额既涨又跌，要改任意元素的键，所以用 `TreeSet`：删旧键、插新键各 O(log m)，top-k 顺序读前 k 个。」

**问：窗口很大、ticker 非常多，`TreeSet` 常数太大怎么办？**
* (1) k 很小时只维护「候选集」（top-k 加缓冲区），用堆加惰性删除；(2) ticker 映射成 int，总额用 `long[]` 存，`TreeSet` 里放 `long` 编码（总额高位 + 编号低位）减少对象；(3) 按 ticker 哈希分 S 片，每片一个 `TreeSet`，`top()` 做 S 路 k 路归并。先量，确实是瓶颈再做。

**问：Part 4，`parallel()` 流为什么有时更慢？**
* 5.6：(1) 事件太少，调度开销超过收益；(2) 合并串行，key 越多越贵；(3) 公共线程池 JVM 共享，别的并行流会抢；(4) 内存带宽是上限。先测顺序版，再测各种分块；key 很多时考虑按 key 分区或共享并发 map。

**问：怎么保证并行结果和顺序版完全一样？**
* 整数加法结合律/交换律；每块私有 `Map` + 只读输入；tie-break 是全序（top-k 不依赖遍历顺序）。验证：随机打乱事件顺序、变化块数，断言结果 `Map.equals`；重复多轮，用 `CountDownLatch` 让线程同时开始。

**问：一块失败了，其余怎么办？线程会泄漏吗？**
* `ShutdownOnFailure`：第一个失败后关闭 scope、中断其余；try 块结束前所有子线程一定结束。中断是协作式的，循环要定期检查 `isInterrupted()`。`ExecutorService` + `Future.get()` 则一个失败不取消其他，要手动 `cancel(true)` 并保证 `shutdown`。

**问：输入有 100 亿条放不进内存？**
* 流式分块读取；按 `hash(ticker) % S` 分片写盘（同一 ticker 必在同一片），每片聚合后 top-k，再合并 S 个 top-k（ticker 不跨片，全局 top-k 一定在各片 top-k 的并集里）。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| top-k 最大值用最大堆装全部再弹 k 次 | O(n) 空间，不能流式，n log n | 大小为 k 的**最小**堆 |
| 比较器只写 `notional` 降序 | 平局顺序未定义，结果不可复现，并行后更乱 | 三级全序：notional、ticker、index |
| `comparing(A).thenComparing(B).reversed()` | B 也被反转 | `comparing(A).reversed().thenComparing(B)` |
| 快速拒绝写成 `notional <= 堆顶` | 平局时 ticker 更小的好事件被误拒 | 严格 `<` |
| `long notional = price * volume;` | 溢出静默绕回，天价成交排最后 | `Math.multiplyExact` |
| 只对进堆的事件做溢出检查 | 检测与数据排列有关 | 每个事件都校验 |
| 用 `double` 存金额并行累加 | 浮点不满足结合律，每次结果不同 | 整数 tick |
| `TreeSet` 比较器只看总额 | 总额相同的 ticker 被当同一元素吞掉 | 比较器带上 ticker（身份） |
| 先改 `acc.total` 再 `ranking.remove(旧键)` | 找不到旧键，树里残留脏数据 | 先按**旧**值删，再改，再按新值插 |
| 溢出检查放在改状态之后 | 抛异常时状态已被破坏 | 先算 `addExact`，成功再改 |
| combiner 把 left 并进 right | `BiConsumer` 只能改第一个参数，left 内容丢了 | `(left, right) -> right.forEach(... left.merge ...)` |
| supplier 返回共享对象 | 数据竞争 | 每次 `new` 新容器 |
| 取消时不检查中断标志 | 中断只是标志，线程仍算到底 | 循环里定期 `isInterrupted()` |
| `n * c / chunks` 用 `int` | `n * c` 溢出 | 先转 `long` |

---

## 9. 自测题

1. `k = 3`，流 `[4, 8, 1, 9, 2, 7]`，用「大小为 3 的最小堆」手工走一遍，写出每步堆的内容。
2. 为什么 `BEST_FIRST` 的第三级用 `index` 一定能分出胜负？去掉第三级什么会变得不稳定？
3. 窗口 `W = 10`，一笔成交在 `t = 100`，`now = 109` 和 `now = 110` 时它是否还活着？
4. `Long.MAX_VALUE / 2 + 1` 同一个 ticker 出现两次，用 `Math::addExact` 聚合会怎样？分到两块各算一次再合并呢？
5. （小编程）写 `Comparator<TickerTotal>`：总额降序，相同按 ticker 升序，不用 `reversed()`。
6. （思考）价格改成可为负（如表示卖出）。Part 4「溢出结果与分块无关」的论证哪一步失效？

<details><summary>答案</summary>

1. `[4]` → `[4,8]` → `[1,4,8]`（满，守门员 1）→ 9 > 1：`[4,8,9]` → 2 < 4：不变 → 7 > 4：`[7,8,9]`。结果从大到小 9, 8, 7。
2. `index` 是数组下标，全局唯一，任何两个不同事件 `index` 不同。去掉后「notional 与 ticker 都相同」的事件顺序由堆内部实现决定（如样例的下标 1 与 4），结果因 JDK 版本、输入顺序而不稳定。
3. `now = 109`：`109 - 100 = 9 < 10`，活着；`now = 110`：`110 - 100 = 10 >= 10`，过期。
4. 顺序聚合：第二次 `addExact` 抛 `ArithmeticException`。分到两块：每块部分和 `MAX/2+1` 不溢出，**合并时**才溢出——`mergeInto` 里的 `merge(…, Math::addExact)` 抛出。结果一致：都抛。
5. `(a, b) -> { int c = Long.compare(b.notional(), a.notional()); return c != 0 ? c : a.ticker().compareTo(b.ticker()); }`。用 `Long.compare(b, a)` 而不是 `b - a`（极端值会溢出）。
6. 「所有 notional 非负 ⇒ 部分和单调不减 ⇒ 任意部分和 ≤ 总和」失效：有负数时某个顺序下中间和可能先超过 `Long.MAX_VALUE` 再被负数拉回。此时某些分块抛异常、另一些不抛，结果依赖分块——要么禁止负数，要么用 `BigInteger` / 更宽的累加器（`Math.multiplyHigh` 做 128 位累加）。

</details>

---

「延伸」Sedgewick《算法》第 2.4 节「优先队列」。
