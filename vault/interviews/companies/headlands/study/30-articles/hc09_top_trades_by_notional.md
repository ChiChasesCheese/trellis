# hc09 讲义 · Top Trade Events by Notional：从「全部排序」到「滑动窗口」再到「多核并行聚合」

> 读者：会写基本 Java（类、方法、循环、`ArrayList` / `HashMap`），没学过堆、有序集合、整数溢出、线程与并行；每个概念从零讲。

---

## 1. 这道题在问什么

交易所一天会产生很多**成交事件**（trade event）。每个事件有三样东西：股票代码（ticker，比如 `AAPL`）、成交价格（price）、成交数量（volume）。
题目把它们放在**三个平行数组**里——第 `i` 个事件就是 `(tickers[i], prices[i], volumes[i])`。

一个事件的 **notional**（名义金额）= 价格 × 数量。它衡量「这笔成交到底有多大」：100 股、每股 10 美元的成交，notional 是 1000 美元；
1 股、每股 1000 美元的成交，notional 也是 1000 美元。

题目分四步升级，就像一小时电面里面试官一路追问：

1. **Part 1**：找出 notional 最大的 `k` 个**事件**。
2. **Part 2**：同一只股票的事件加起来，找出总 notional 最大的 `k` 只**股票**。
3. **Part 3**：数据不是一次性给齐的，而是实时流进来，只关心最近一段时间（滑动窗口）内的成交，随时要回答 top-k。
4. **Part 4**：数据有几千万条，怎么用多个 CPU 核一起算，并且保证结果和单线程**一模一样**。

### 手算一遍

```
下标      0      1      2      3      4      5
ticker  AAPL   MSFT   AAPL   GOOG   MSFT   TSLA
price  18000  40000  18100  14000  40000  25000
volume    10      3      5      9      3      8
notional 180000 120000  90500 126000 120000 200000     ← 价格 × 数量
```

* **Part 1，k = 3**：把 notional 从大到小排：TSLA 200000（下标 5）、AAPL 180000（下标 0）、GOOG 126000（下标 3）、MSFT 120000（下标 1 和 4）、AAPL 90500（下标 2）。取前 3 个：下标 5, 0, 3。
* **k = 4** 呢？第 4 名是 MSFT 120000——但下标 1 和下标 4 的事件 notional 一样、ticker 也一样，选哪个？题目规定：再按下标升序，所以选**下标 1**。**没有这条规定，答案就不唯一**，结果无法验证。这叫 tie-break（打破平局）。
* **Part 2，k = 2**：AAPL = 180000 + 90500 = 270500；MSFT = 120000 + 120000 = 240000；TSLA = 200000；GOOG = 126000。前 2 名：AAPL、MSFT。
  注意：**最大的单个事件是 TSLA，最大的 ticker 却是 AAPL**。两个问题的答案不一样。

---

## 2. 前置知识

> 复杂度记号速记：`O(n)` 表示步数随输入规模 n 线性增长；`O(log n)` 表示 n 翻倍只多一步（二分查找、平衡树、堆）；`O(n²)` 表示每一对元素都要处理一次；`O(1)` 表示与 n 无关。

### 2.1 平行数组（parallel arrays）

**是什么**：用几个**等长**的数组表示一批记录，第 `i` 条记录是 `a[i]`、`b[i]`、`c[i]` 三个数组各取第 `i` 个。

**为什么用它（以及为什么面试官喜欢给这种格式）**：不用建「事件对象」，`prices` 和 `volumes` 是 `long[]`，在内存里是一整块连续的数字。
扫一遍 `prices` 和 `volumes`，CPU 缓存（cache）能一口气预取很多个，速度很快——这叫**局部性**（locality）；对比 `List<Trade>` 里每个对象散落在堆的各处，要一个个「追指针」。
对比：`ArrayList<Long>` 的每个元素是指向堆上 `Long` 对象的指针（AoS，Array of Structures：每条记录一个对象）；平行数组是 SoA（Structure of Arrays：每个字段一个数组），数值连续存放，缓存友好。
注意 `String[] tickers` 例外：它是一个**指针数组**，每个元素指向一个 `String` 对象，所以按 ticker 聚合时仍然要追指针。

**怎么写**：

```java
int n = tickers.length;                 // 三个数组等长，要先检查
for (int i = 0; i < n; i++) {
    long notional = prices[i] * volumes[i];   // 第 i 个事件
}
```

**代价**：数组之间的「对齐」靠约定，没有类型保护——长度不等、下标错位都编译得过。所以第一件事是**检查三个数组等长**，不等就抛 `IllegalArgumentException`。

### 2.2 为什么金额用整数 tick，不用 `double`

**是什么**：tick 是最小报价单位。美股常见 1 tick = 0.01 美元 = 1 美分，所以价格 `180.00` 美元存成整数 `18000`。

**为什么需要**：浮点数（`double`）表示不了 0.1 这种十进制小数，累加会有误差，而且**加的顺序不同结果会不同**：

```java
double a = 0.1, b = 0.2, c = 0.3;
(a + b) + c   // 0.6000000000000001
a + (b + c)   // 0.6
```

金额累加差一点点没关系？不行：
* 两个「应该相等」的 notional 比较时，浮点误差会把 tie（平局）变成「谁大谁小」，**tie-break 规则就失效了**；
* Part 4 把数据分块并行累加，每块的和再合并——**合并顺序取决于线程调度**，浮点结果每次运行都可能不同，无法稳定复现；
* 整数加法满足**结合律**（`(a+b)+c == a+(b+c)`）和**交换律**，所以怎么分块、按什么顺序合并，结果都一样。这是 Part 4 能正确的根本原因。

**怎么写**：价格、数量都用 `long`。真题的价格类型未知，这是 的选择；金融公司的惯例是「钱用整数最小单位，或者 `BigDecimal`」。

### 2.3 整数溢出与 `Math.multiplyExact`

**是什么**：`long` 有 64 位，范围 −9223372036854775808 到 9223372036854775807（约 ±9.2 × 10¹⁸）。结果超出范围时 Java **不报错，悄悄绕回去**：

```java
long x = Long.MAX_VALUE;         // 9223372036854775807
long y = x * 2;                  // -2 ！（绕回负数）
long z = Math.multiplyExact(x, 2L);   // 抛 ArithmeticException("long overflow")
```

**为什么本题要管**：price × volume 看起来不大，但「价格是 `long`」就意味着有人会传大数。一个绕回成负数的 notional，会让一笔天价成交在排名里排到最后——**静默地给错答案**，在金融系统里比崩溃危险得多。所以：乘法用 `multiplyExact`，累加用 `addExact`，溢出就抛异常。

**一个有用的边界**：`Long.MAX_VALUE` 的平方根向下取整是 **3037000499**。所以 `3037000499 × 3037000499 = 9223372030926249001` 不溢出，`3037000500 × 3037000500 = 9223372037000250000` 就溢出了（比 `Long.MAX_VALUE = 9223372036854775807` 大）。测溢出边界时就用这两个数。

**怎么工作**（直觉）：`multiplyExact(x, y)` 先算 64 位乘积，再检查「用高 64 位 / 除法回验」确认没有丢位，丢了就抛。HotSpot 把它当作**内联函数**（intrinsic）处理，JIT 编译后通常就是一条乘法加一次溢出检查，几乎没有额外成本。 数学与字符串小工具。

### 2.4 top-k 与「大小为 k 的最小堆」

**是什么**：从 n 个元素里选出最大的 `k` 个（k 通常远小于 n）。

**为什么需要特殊办法**：最直接的是把 n 个元素全部排序再取前 k 个，要 O(n log n)，并且需要把 n 个元素全放进内存。但我们只要 k 个——为什么要为剩下 n−k 个浪费工夫？

**它怎么工作**：维护一个「目前见过的最大的 k 个」的集合。每来一个新元素 x，问：x 比这 k 个里**最小的**那个大吗？
* 不大 → x 肯定进不了前 k，扔掉；
* 大 → 把那个最小的踢出去，x 加进来。

所以需要一个「随时能拿到最小值、能删除最小值、能插入」的结构——这正是**最小堆**（min-heap）。**最大的 k 个要用最小堆**，这反直觉但是关键：堆顶是 k 个里最差的，是「守门员」，新来的要比守门员强才能进。

用 k = 3 在流 `5, 1, 9, 3, 7, 8` 上走一遍（堆里画成排序后的样子，最左是堆顶，即最小）：

```
来 5 :  堆未满，加入            堆 = [5]
来 1 :  堆未满，加入            堆 = [1, 5]
来 9 :  堆未满，加入            堆 = [1, 5, 9]        满了，守门员 = 1
来 3 :  3 > 1，踢掉 1，加入 3   堆 = [3, 5, 9]        守门员 = 3
来 7 :  7 > 3，踢掉 3，加入 7   堆 = [5, 7, 9]        守门员 = 5
来 8 :  8 > 5，踢掉 5，加入 8   堆 = [7, 8, 9]        守门员 = 7
结果（从大到小）: 9, 8, 7
```

每个元素最多一次插入 + 一次删除最小，都是 O(log k)，总共 **O(n log k)** 时间、**O(k)** 额外空间。k = 100、n = 10⁶ 时，log k 约 7，比排序的 log n 约 20 小得多；更重要的是，**如果输入是随机顺序，绝大多数元素连堆都进不去**，只花一次比较（见 3.1 节与 4.1 节的数据）。

堆是用数组存的完全二叉树，最小堆要求每个父节点 ≤ 子节点，所以最小值永远在堆顶（数组下标 0），读取是 O(1)。插入时放到数组末尾再**上浮**（sift-up：和父节点比较，更小就交换）；删除最小时把末尾元素换到堆顶再**下沉**（sift-down：和较小的子节点比较，更大就交换）。两者最多走树高 log₂ n 层，所以都是 O(log n)。Java 里就是 `PriorityQueue`：

```java
var heap = new PriorityQueue<Integer>();   // 默认最小堆
heap.add(5);                // 插入 O(log k)
heap.peek();                // 看堆顶（最小）O(1)，空堆返回 null
heap.poll();                // 取出并删除堆顶 O(log k)，空堆返回 null
new PriorityQueue<>(cmp);   // 自定义顺序：cmp 认为「小」的在堆顶
```

### 2.5 比较器（`Comparator`）、全序与 tie-break

**是什么**：`Comparator<T>` 是一个函数 `compare(a, b)`，返回负数（a 排前）、0（平局）、正数（a 排后）。

**为什么本题的关键是「写全」**：排序规则如果只写「notional 大的在前」，那么两个 notional 相同的事件**谁在前是未定义的**——取决于堆内部的实现细节、输入顺序。后果：
* `topEvents(k=4)` 的第 4 名可能是下标 1，也可能是下标 4，不同实现、不同 JDK 版本可能不同；
* 写不出稳定的期望值；
* Part 4 并行后，不同线程调度下平局的结果会变——**不可复现的 bug 最难查**。

**怎么办**：把比较器写成**全序**（total order）：任意两个不同事件，比较结果一定不是 0。本题的规则链是：

```
1. notional 降序      （大的在前）
2. ticker 升序        （String.compareTo，按 UTF-16 编码字典序）
3. 下标 index 升序    （下标全局唯一，所以第 3 条一定能分出胜负）
```

**Java 里怎么写**：

```java
Comparator<Trade> BEST_FIRST =
    Comparator.comparingLong(Trade::notional).reversed()   // 1. notional 降序
              .thenComparing(Trade::ticker)                // 2. ticker 升序
              .thenComparingInt(Trade::index);             // 3. 下标升序
```

⚠️ `reversed()` 只反转它**前面**的整条链。`comparingLong(A).thenComparing(B).reversed()` 会把 B 也反过来。所以 `reversed()` 要紧跟在第一个条件后面。

### 2.6 `HashMap.merge`：聚合的标准写法

**是什么**：`map.merge(key, value, f)`：key 不存在就放入 `value`；存在就用 `f(旧值, value)` 的结果替换。

**为什么用它**：Part 2 要「同一 ticker 的 notional 加起来」。老写法：

```java
Long old = map.get(key);
map.put(key, old == null ? v : old + v);     // 两次哈希查找，还要手写 null 判断
```

`merge` 一行搞定，并且对 `ConcurrentHashMap` 来说是**原子**的（Part 4 的对照组用到）：

```java
map.merge(ticker, notional, Math::addExact);   // Math::addExact 溢出时抛异常
```

哈希表的原理：用哈希函数把 key 映射成数组下标（桶）；两个 key 落到同一个桶叫冲突，桶内用链表（或树）串起来；元素太多时扩容并重新哈希，保持平均每桶元素很少，所以 `merge`/`get`/`put` 平均 O(1)。

### 2.7 有序集合 `TreeSet`：能「删掉任意一个、再放回去」的有序结构

**是什么**：`TreeSet<E>` 把元素按比较器排好序存放（底层是红黑树，一种自平衡的二叉搜索树），支持 `add`、`remove`、`first`、按顺序遍历，**每个操作 O(log m)**，m 是元素个数。红黑树是自平衡二叉搜索树：每次插入 / 删除后通过旋转和染色保证树高不超过 2·log₂(m+1)，所以增删查都是 O(log m)。

**为什么需要它（本题 Part 3 的核心）**：堆只能高效地取最小；而 Part 3 里一个 ticker 的总额会**变大**（来了新成交）也会**变小**（旧成交过期），也就是要「找到这个 ticker 在结构里的位置，改它的键」。
`PriorityQueue.remove(Object)` 要先线性扫描找到元素，O(m)。`TreeSet` 能 O(log m) 删掉任意一个元素：

```java
var set = new TreeSet<TickerTotal>(BEST_TICKER_FIRST);
set.add(new TickerTotal("AAPL", 500));
set.remove(new TickerTotal("AAPL", 500));   // 按比较器找到并删除，O(log m)
set.add(new TickerTotal("AAPL", 300));      // 以新键放回去
set.stream().limit(k).toList();             // 按顺序取前 k 个
```

⚠️ **TreeSet 用比较器判断「是不是同一个元素」**：`compare(a, b) == 0` 就认为 a 和 b 是同一个，`add` 会被拒绝。所以比较器必须是全序、并且和「身份」一致——
这里的 `BEST_TICKER_FIRST`（总额降序 + ticker 升序）里，ticker 在集合中唯一，所以 compare 为 0 当且仅当 ticker 和总额都相同，没有问题。如果比较器只看总额，两个总额相同的 ticker 会有一个被悄悄吞掉。

### 2.8 滑动窗口与 FIFO 队列的过期

**是什么**：只关心「最近 W 个时间单位」内的数据。随着时间前进，窗口右端前进，左端也前进，左端之外的数据**过期**（expire）。

**为什么能高效**：事件**按时间顺序到达**，所以先到的先过期（先进先出，FIFO）——过期只发生在队列的最前面，永远不用到中间去找。用一个 `ArrayDeque`：队尾 `addLast` 新事件，队头 `peekFirst` 看最老的，过期就 `removeFirst`。
每个事件**进一次、出一次**，所以过期的总代价是 O(n)，摊还（amortized）到每个事件 O(1) 次出队（每次出队还要付 TreeSet 的 O(log m)）。
**摊还分析**（amortized）：看一长串操作的总代价再平均，而不是只盯最坏的一次。每个事件最多入队一次、出队一次，n 个事件的总出队次数 ≤ n，平均每个事件 O(1) 次出队。

### 2.9 并行：线程、数据竞争、结合律、ForkJoin、虚拟线程

这一节是 Part 4 的全部预备知识，从零讲。

**线程（thread）**：操作系统可以同时调度的执行流。一台 12 核的机器可以同时真正并行跑 12 个线程。**并行**（parallelism）= 为了更快而同时做多件事。

**数据竞争（data race）**：两个线程同时读写同一个变量，而且至少有一个在写，又没有任何同步。典型的「丢失更新」（lost update）：

```
线程 A: 读 total (=10)            线程 B: 读 total (=10)
线程 A: 算 10 + 5 = 15            线程 B: 算 10 + 7 = 17
线程 A: 写 total = 15
                                  线程 B: 写 total = 17      ← A 的更新丢了，应该是 22
```

`HashMap` 不是线程安全的：两个线程同时 `put` 可能丢数据、甚至让内部结构损坏。解决办法有三类：
1. **加锁 / 用并发容器**（`ConcurrentHashMap`）：正确，但线程之间要互相等，扩展性差；
2. **不共享**：每个线程用自己**私有**的数据结构，最后再把结果合并——这是 Part 4 的主方案，因为私有的东西没有竞争，不需要任何锁；
3. 不可变数据：大家都只读同一份输入数组，没有写，自然没有竞争。

**结合律（associativity）与「合并」**：`a + b` 能分块计算的前提是 `(a₁ + a₂) + (a₃ + a₄) == ((a₁ + a₂) + a₃) + a₄`，怎么加括号结果都一样。整数加法满足；浮点加法不满足（2.2 节的例子）。
对 `Map` 的合并来说：「把右边那张表的每一项加进左边那张表」，只要加法满足结合律和交换律，合并顺序就无所谓。

**Fork/Join 框架**（`java.util.concurrent.ForkJoinPool`）：为「把大任务递归切成小任务」设计的线程池。

```
              compute(0..8)
              /            \
    fork: compute(0..4)   当前线程直接算: compute(4..8)
         /      \                 /        \
      ...        ...            ...         ...
```

* `fork()`：把子任务放进当前工作线程自己的队列；
* `join()`：等子任务的结果（等的时候线程不闲着，会去执行别的任务）；
* **工作窃取**（work stealing）：某个线程队列空了，会从别的线程队列的**另一端**（最老、通常也是最大的任务）偷任务，自动负载均衡。

`parallel()` 流底层用的就是 `ForkJoinPool.commonPool()`——**整个 JVM 共用的一个线程池**。

**虚拟线程（virtual thread）与结构化并发**：Java 21 的轻量线程，几乎可以一个任务一个线程；`StructuredTaskScope` 保证「在这个 try 块里 fork 出来的所有线程，离开 try 块时一定都结束了」，并且一个失败可以取消其余的。

**Amdahl 定律**（别被名字吓到）：程序里**必须串行**的部分决定了并行的加速上限。本题里，「把各块的结果合并」是串行的，数据读取受内存带宽限制——所以并行不一定快（5.6 节有数据）。

---

## 3. 从最笨的解法开始

### 3.1 Part 1：全部建对象，整体排序

```java
var all = new ArrayList<Trade>();
for (int i = 0; i < n; i++) all.add(new Trade(i, tickers[i], prices[i], volumes[i]));
all.sort(BEST_FIRST);
return all.subList(0, Math.min(k, n));
```

* 时间 O(n log n)，空间 O(n)（n 个 `Trade` 对象，每个约 32 字节，加上 `ArrayList` 的指针数组）。
* 正确，而且是最好的**对拍基线**。
* **具体慢在哪**：n = 10⁶、k = 100 时，要创建 100 万个对象、做 100 万 × 20 次比较，而我们只要 100 个。数据：

| n = 10⁶，k = 100，5000 个 ticker，随机顺序 | 时间 |
|---|---|
| 全部排序（`topEventsSorted`） | 约 220 ms |
| 大小为 k 的最小堆（`topEvents`） | 约 2–14 ms（含 JIT 预热） |

### 3.2 Part 2：对每个 ticker 重新扫一遍

最笨的写法：先找出所有不同的 ticker，对每个 ticker 把整个数组扫一遍累加。m 个不同 ticker → O(n · m)。m = 10⁵、n = 10⁶ 就是 10¹¹，要几十分钟。
一次扫描 + `HashMap` 就能把它降到 O(n)（4.2 节）。

### 3.3 Part 3：每次查询都重新算

窗口里的成交是活的，每次问 top-k：把所有「活着的」成交重新聚合一遍，再选 top-k。每次查询 O(窗口大小)。窗口里有 10⁵ 笔成交、每秒查询 1000 次，就是 10⁸ 次操作 / 秒。
这个方案**很有用**：它是最好的对拍基线：每次从头重算，结果一定对。

### 3.4 Part 4：一个线程算完

单线程 O(n)，2 千万事件约 0.2–4 秒（取决于不同 ticker 个数，见 5.4 节）。问题不是它「错」，而是「慢」，并且面试官想听你说出怎么用多核。

---

## 4. 一步一步改进

### 4.1 Part 1

**第 1 步：只留 k 个，用最小堆**
* 发现：我们为 n−k 个注定进不了前 k 的元素付了排序的钱。
* 想法：维护「目前最好的 k 个」，新元素只和其中最差的那个比（2.4 节）。
* 为什么有效：每个元素至多一次堆插入和一次删除，都是 O(log k)，而且堆大小恒为 k，内存 O(k)。
* 代码变化：`PriorityQueue<Trade>` 用 `BEST_FIRST.reversed()`（堆顶 = 最差）。
* 新复杂度：O(n log k) 时间，O(k) 空间。

**第 2 步：快速拒绝（fast reject）**
* 发现：随机顺序下，堆满了之后，几乎每个新元素都不如堆顶——但我们还是为它 `new` 了一个 `Trade` 对象再去比较。
* 想法：notional 是一个 `long`，**先拿 long 和堆顶的 notional 比**，严格小就直接 `continue`，连对象都不建。只有 notional ≥ 堆顶（可能进入或平局）才建对象走完整比较。
* 为什么正确：`BEST_FIRST` 的第一条就是 notional 降序，notional 严格小于堆顶的元素一定排在堆顶后面，进不了前 k。
* 效果：随机输入下**零分配**，主循环变成「两次数组读取 + 一次乘法 + 一次比较」。这也是「顺序扫描连续的 `long[]`」对缓存友好的典型受益场景。
* 最坏情况：notional 严格递增的输入，每个元素都会进堆，退化到真正的 O(n log k)：n = 10⁶、k = 1000 约 120 ms（随机顺序同样规模只要几毫秒）。

**第 3 步：全序 tie-break**
* 发现：堆里元素 notional 相同时，到底谁留下？
* 想法：比较器写满三级（notional、ticker、index）；`topEvents` 里「新元素比堆顶好」用的是 `BEST_FIRST.compare(t, heap.peek()) < 0`，平局由 ticker、index 裁决。
* 注意：这里 index 是**全局唯一**的，所以比较器永远不会返回 0，结果唯一。
* 一个容易写错的地方：快速拒绝用的是 `notional < 堆顶 notional`（**严格小于**）。写成 `<=` 会把「notional 相同但 ticker 更小」的更好事件也拒掉（下标 1 对下标 4 的样例会错）。

**第 4 步：溢出与输入检查**
* 发现：`prices[i] * volumes[i]` 可能溢出；数组可能长度不等、有 null、有负数。
* 想法：所有事件（包括进不了 top-k 的）都经过同一个 `notionalAt(i)`：检查非空、非负，然后 `Math.multiplyExact`。
* 为什么「每个事件都检查」：如果只检查进堆的，溢出的事件恰好在快速拒绝那一步被「拒绝」前就已经被算错了；而且「是否抛异常」不应该依赖于数据的排列。
* 一个细节：`Trade` 的紧凑构造器里再 `multiplyExact` 一次，保证「`Trade` 对象存在 ⇒ `notional()` 不会溢出」。这样 `notional()` 内部可以直接 `price * volume`。

**第 5 步：输出顺序**
* 堆按「最差先出」，`poll` 出来是从差到好；用 `ArrayList.reversed()`（Java 21，Sequenced Collections）得到从好到差，再 `List.copyOf` 变成不可变。
* 备选：`new ArrayList<>(heap)` 再 `sort(BEST_FIRST)`，O(k log k)，同样可以。

### 4.2 Part 2

**第 1 步：一趟扫描 + `HashMap.merge`**
```java
var totals = new HashMap<String, Long>();
for (int i = 0; i < n; i++) totals.merge(tickers[i], notionalAt(i), Math::addExact);
```
O(n) 期望时间（哈希表平均 O(1)）。`addExact` 保证「每个事件都不溢出但加起来溢出」也会被发现。

**第 2 步：对 m 个不同 ticker 取 top-k**
* 两个选择：(a) 全部排序 `O(m log m)`；(b) 大小为 k 的最小堆 `O(m log k)`。
* m = 10⁵、k = 50 时，(b) 稍快。数据（n = 10⁶、m = 10⁵）：堆版约 41–58 ms，Stream 版（排序）约 82–103 ms。两者都够快；选哪个取决于你想强调什么：堆版展示「k 很小时不排序全部」，Stream 版展示「写得短」。
* `topOf(Map, k)` 抽成独立方法：Part 4 合并完分块结果后直接复用。

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
`teeing` 把同一个流同时喂给两个收集器，最后用第三个参数把两个结果合成一个。老写法要遍历两次，或者手写一个可变的累加器类。
Stream 版的代价：`IntStream.boxed()` 把每个 `int` 装箱成 `Integer`，`groupingBy` 里还有额外的中间容器——这是它比手写循环慢的原因。

### 4.3 Part 3（流式 + 过期）

**第 1 步：为什么只用堆不行**

场景：窗口里 ticker A 总额 500、B 总额 300、C 总额 100，k = 2，堆里是 {A, B}（堆顶 B = 300，守门员）。
* 事件 1：来了一笔 C 的成交，C 变成 400。C 比守门员 B 强 → 踢掉 B，C 进堆。**但 B 并没有消失**，它还在窗口里，只是被挤出了堆；堆不再记得它。
* 事件 2：A 的老成交过期了，A 从 500 降到 50。现在 B（300）应该回到 top-2，可是堆里没有 B 的信息了。**必须重建**。

根本原因是：堆是「只进不出」的结构——它高效支持 `add` 和「弹出堆顶」，但不支持：
1. **找到任意一个元素**（要线性扫描）；
2. **降低或提高一个元素的键**（decrease-key / increase-key；`PriorityQueue` 根本没有这个操作）；
3. **删除任意元素**（`remove(Object)` 是 O(m)：扫描找到它，再整理）。

有三种补救办法：

| 方案 | 做法 | 代价 |
|---|---|---|
| A. 查询时重建堆 | 每次 `top()` 把所有活跃 ticker 过一遍，选 top-k | 每次查询 O(m log k) |
| B. 惰性删除（lazy deletion） | 总额变化时不删旧条目，只是**再插一条新的**；弹出时发现条目与 `totals` 当前值不符，就丢弃 | 堆里累积垃圾，大小可以到 O(事件数)；`top()` 需要弹出 k 个有效条目再放回去 |
| C. 有序集合 `TreeSet` | 总额变化：O(log m) 删旧键、O(log m) 插新键；`top()` 直接按序读前 k 个 | 红黑树常数比堆大；但所有操作都有上界 |

选 C。本题是「查询要看前 k 个」而不仅是「堆顶」，且要支持任意元素更新，有序集合最自然。

**第 2 步：数据结构设计**

```
ArrayDeque<Fill> live          按时间顺序的活跃成交（队头最老）
HashMap<String, Acc> totals    ticker → (窗口内总额, 窗口内活跃成交笔数)
TreeSet<TickerTotal> ranking   所有活跃 ticker，按 (总额 降序, ticker 升序)
                               —— 与 totals 保持一一对应
```

* `Acc.count`（活跃笔数）的作用：一个 ticker 的成交可能总额为 0（价格或数量为 0），不能用「总额 == 0」判断「这个 ticker 还有没有活跃成交」。count 减到 0 才把它从两张表里删掉。

**第 3 步：三个操作**

* `add(fill)`：
  1. `advanceTo(fill.time)`：推进时钟，先让旧成交过期；
  2. 取该 ticker 的旧总额 `old`，算 `new = Math.addExact(old, fill.notional)`——**这一步先做，如果溢出就抛，此时还没动任何结构**（原子性）；
  3. `ranking.remove(TickerTotal(ticker, old))`，更新 `totals`，`ranking.add(TickerTotal(ticker, new))`，`live.addLast(fill)`。
* `advanceTo(t)`：`t` 不能小于当前时间；当 `队头.time` 满足 `now - time >= window` 就 `removeFirst`，对应 ticker 做「减总额、`ranking` 删旧键、（count 不为 0 就）插新键」。
* `top()`：`ranking.stream().limit(k).toList()`，O(log m + k)。

**为什么 `now - time >= window` 而不是 `time + window <= now`**：时间可能很大，`time + window` 会溢出；`now - time` 因为 `time <= now` 且都非负，不会溢出。

**复杂度**：每个事件进一次出一次，每次 O(log m)；查询 O(log m + k)。

**第 4 步：时钟与「Tick / Ask」**

`replay` 把 `Fill`（成交）、`Tick`（时钟前进）、`Ask`（询问）封装成一个 sealed 接口 `Feed`，用模式匹配 `switch` 分派（5.4 节与 6 节）。`Ask(t)` 也会先推进时钟，所以「在 t 时刻问」和「先 Tick(t) 再问」等价。

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

**合并为什么是对的**（面试官真正想听的三点）：

1. **整数加法满足结合律和交换律**：所有分块方式、合并顺序，数学上的和都相同。（对照 2.2 节的 `double` 反例。）
2. **没有共享可变状态**：每块的 `Map` 只被一个任务写；所有任务只读同一份输入数组。没有数据竞争，不需要锁。合并时 `mergeInto(a, b)` 把 b 并进 a，这两张表在此时都已经没有人在写了（子任务已完成：`join()` 建立了 happens-before 关系，保证合并线程看到子任务写的所有内容）。
3. **溢出的行为与分块无关**：所有 notional 非负，所以任何部分和 ≤ 总和。如果总和 ≤ `Long.MAX_VALUE`，**任何**部分和、任何一次合并都不会溢出；如果总和 > `Long.MAX_VALUE`，无论怎么分块，*某个*步骤一定会溢出（最后一次合并至少会），所以「是否抛 `ArithmeticException`」只取决于数据，不取决于分块。
   （这是**非负性**带来的性质。如果允许负数——比如撤销、卖出——中间部分和可能先爆再回来，异常与否就依赖于顺序了。本题明确价格和数量非负，就是为了保证这一点。）

**第 2 步：四种实现**

| 实现 | 切块方式 | 合并方式 | 特点 |
|---|---|---|---|
| `totalsParallelStream` | 框架自动 | `collect` 的 combiner | 最短；用公共线程池；combiner 必须改第一个参数 |
| `totalsForkJoin` | 递归对半，小于 `threshold` 停 | `join()` 后 `mergeInto` | 可控粒度；显式的任务树 |
| `totalsScoped` | 固定 `chunks` 块，每块一个虚拟线程 | 全部 `join` 后按序合并 | 失败即取消其余；异常原样抛出；生命周期受 try 块限制 |
| `totalsSharedMap` | 固定 `chunks` 块 | 没有合并：所有线程直接 `merge` 进一张 `ConcurrentHashMap` | 对照组；无合并代价，但有争用 |

**第 3 步：错误处理与取消**

* 一块里出了异常（溢出、负数）：`totalsScoped` 的 `ShutdownOnFailure` 会让 scope 关闭并**中断**其余子线程。中断是**协作式**的——线程只是被设置了「中断标志」，不会被强行停止。所以 `accumulate` 里每 4096 个事件检查一次 `Thread.currentThread().isInterrupted()`，被中断就抛 `CancellationException`。
  没有这个检查，其余块会老老实实算完才返回，取消形同虚设。
* 异常要**原样**抛给调用者：对每种实现，调用者都应收到同一个 `ArithmeticException`。`throwIfFailed(e -> e instanceof RuntimeException re ? re : new IllegalStateException(e))` 做的就是「如果是运行时异常就原样抛，否则包一层」。

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

* `record`：不可变数据类，自动生成 `equals / hashCode / toString`，可以直接比较两个列表。
* **紧凑构造器**（`public Trade { ... }`，没有参数列表）：在字段赋值之前运行，所有校验放这里——非法的 `Trade` 构造不出来。
* 构造器里调用 `multiplyExact` 但**丢弃结果**：目的就是「提前证明不溢出」，使 `notional()` 里的普通乘法是安全的。这是一个小技巧：*把检查移到对象创建时，后面所有使用都不用再担心*。

```java
public static final Comparator<Trade> BEST_FIRST =
        Comparator.comparingLong(Trade::notional).reversed()
                .thenComparing(Trade::ticker)
                .thenComparingInt(Trade::index);
```

读法：先按 `notional` 比较 → `reversed()` 反过来（大的在前）→ 平局按 `ticker` → 再平局按 `index`。`public static final`：Part 3 的 `TreeSet` 也复用 `BEST_TICKER_FIRST`。

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

* 比较器取 `BEST_FIRST.reversed()`：`PriorityQueue` 把比较器认为「最小」的放堆顶，反过来之后「最小」= 「最差」，堆顶就是守门员。
* `new PriorityQueue<>(initialCapacity, comparator)`：初始容量 `max(1, min(k, n))`——不能为 0（`PriorityQueue` 要求 ≥ 1），也没必要大于 `n`。
* `k == 0` 时仍然要走一遍 `notionalAt`（做校验），但不碰堆。
* `BEST_FIRST.compare(t, heap.peek()) < 0`：compare 为负表示 t 排在堆顶前面，也就是「更好」。
* 为什么不用 `heap.add(t); if (heap.size() > k) heap.poll();`？也对，而且更短，但无条件 `add` 然后再 `poll` 每个元素要做两次堆操作；上面的写法只在真的会改变堆时才操作。
* `worstFirst.reversed()` 是 `ArrayList` 的**视图**（Java 21），`List.copyOf` 把它变成独立的不可变副本，调用者拿到后不能 `add`。

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

和 `topEvents` 同一个模式，只是元素换成了 `TickerTotal`（m 个，不用 `long` 快速拒绝，因为每个 `Map.Entry` 已经是现成的对象）。
这里没有「溢出检查」——溢出已经在 `merge(…, Math::addExact)` 时发生过了。

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

* **操作顺序**是正确性的一部分：`ranking.remove` 必须在 `acc.total` 改成新值**之前**，否则用新值去找旧键，红黑树里找不到（按比较器，这是另一个位置），旧键残留，`ranking` 里同一个 ticker 出现两次。
* 为什么 `Acc` 是可变类、而不是 `record`：每个活跃成交都要更新它，建新 record 会产生大量垃圾。可变状态局限在 `SlidingTopK` 内部、`private static final class`，不外泄。

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

* `peekFirst` / `removeFirst`：Sequenced Collections 的统一命名（`ArrayDeque` 原来就有，Java 21 起接口统一）。
* `acc.total -= f.notional()`：减法不会溢出（`total` 是若干个非负数之和，减去其中一个）。

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

* `Feed` 是 `sealed interface ... permits Fill, Tick, Ask`，编译器知道只有这三种，`switch` 不需要 `default`；以后新增 `Feed` 子类型，所有没处理它的 `switch` 编译失败。
* `case Tick(var t)`：**记录模式**（record pattern）一步完成「判断类型 + 解构字段」。
* `when t == w.now()`：**守卫**（guard）。时钟没动就什么都不做。注意 `case Tick(var t) when …` 必须写在不带守卫的 `case Tick(var t)` **之前**——否则后者会遮蔽前者，编译器报「dominated」错误。

### 5.5 `ParallelNotional`

**并行流版：**

```java
return IntStream.range(0, n).parallel().collect(
        HashMap<String, Long>::new,                                               // supplier：每个线程自己的新容器
        (m, i) -> m.merge(tickers[i], notionalAt(...), Math::addExact),           // accumulator：往本线程容器加一项
        (left, right) -> right.forEach((k, v) -> left.merge(k, v, Math::addExact)));   // combiner：把 right 并进 left
```

* 三个参数的含义是 `collect` 的**契约**：supplier 每次产生**新的、互不共享的**容器；accumulator 只改传给它的容器；combiner 把第二个容器并进**第一个**。
* **最常见的 bug**：combiner 写反成 `left.forEach(... right.merge ...)`。`BiConsumer` 没有返回值，框架认为结果在第一个参数里——写反了结果就丢了 left 的内容。
* 另一个 bug：supplier 写成 `() -> sharedMap`（所有线程共享一个 Map）——就回到了数据竞争。

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

* `threshold`（阈值）：太小 → 创建任务的开销超过计算；太大 → 并行度不够。经验是让任务总数约为核数的 4–8 倍。
* `(from + to) >>> 1`：无符号右移，两个接近 `int` 上限的下标相加会溢出成负数，`>>> 1` 在位模式上仍然正确（经典的二分查找 bug，Java 的 `Arrays.binarySearch` 在 2006 年修过）。

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

* `scope.fork(callable)` 在一个新虚拟线程里跑任务，返回 `Subtask`（一个「承诺」）。
* `scope.join()`：等所有子任务结束**或者**有一个失败（`ShutdownOnFailure` 在第一个失败后自动关闭 scope、中断其余）。
* `scope.throwIfFailed(...)`：如果有失败就抛。**不调用它**，失败的子任务的异常会被悄悄忽略，后面 `subtask.get()` 会抛 `IllegalStateException`（因为状态不是 SUCCESS）。
* `boundary(n, chunks, c)` = `(int) ((long) n * c / chunks)`：`n * c` 在 `n = 2×10⁹`、`c = 4` 时超过 `int` 范围，必须先转 `long`。块 c 是 `[boundary(c), boundary(c+1))`，相邻块首尾相接，不重叠、不遗漏。
* **预览 API**：`StructuredTaskScope` 在 Java 21 是预览特性（JEP 453），必须 `--enable-preview` 编译和运行；后续版本 API 有不兼容改动。口头说明这一点。

**共享 Map 版（对照组）：**

```java
shared.merge(tickers[i], notionalAt(...), Math::addExact);   // ConcurrentHashMap：对单个 key 原子
```

对一个 key 来说 `merge` 是原子的，函数抛异常时不记录映射——所以溢出也能正确检测。但热点 ticker（比如 AAPL 占 30% 成交）上所有线程抢同一个桶的锁，扩展性差。

---

### 5.6 数据：并行到底快不快（12 核，JDK 21，Generational ZGC，噪声较大，仅看数量级）

| 场景 | 顺序 | `parallel()` 流 | ForkJoin | `Scoped` | 共享 Map |
|---|---|---|---|---|---|
| 2×10⁶ 事件，5×10⁴ ticker | 约 45 ms | 约 30–110 ms | 约 30–65 ms | 约 40–75 ms | 约 20–55 ms |
| 2×10⁷ 事件，200 个 ticker | 约 210–330 ms | 约 75–110 ms | 约 55–215 ms | 约 75–250 ms | 约 300–350 ms |
| 2×10⁷ 事件，2×10⁶ ticker | 约 2.4–4.2 s | 约 1.6–5.3 s | 约 2.1–3.0 s | 约 1.9–4.4 s | 约 0.8–0.9 s |

读这张表要学到三件事：
1. **并行不是免费的**：事件数不大（2×10⁶）时，线程调度、合并的开销抵消了收益，并行几乎没有提高。
2. **ticker 很少（200）时**，每块的 Map 很小，合并几乎免费，`parallel()` 流有 2–3 倍的加速；共享 Map 反而**更慢**——所有线程抢 200 个桶。
3. **ticker 极多（2×10⁶）时**，每块的私有 Map 巨大，「各算各的」要建 C 张大表，再合并 C−1 次，合并（串行）成了瓶颈（Amdahl）；此时共享 `ConcurrentHashMap` 因为不用合并反而最快。

**结论（可以说出口）**：「分块 + 私有结果 + 合并」是默认方案，因为它没有共享状态、正确性容易证明；但它的收益取决于合并成本 ≈ 不同 key 的个数。key 极多时可以考虑按 key 哈希分区（每个线程只负责一部分 ticker，合并就变成简单拼接），或者共享并发 Map。**先测，再选**。

---

## 6. Java 21 特性小课

### record 与紧凑构造器

旧写法（Java 8）：`final` 类 + 私有 final 字段 + 构造器校验 + getter + 手写 `equals/hashCode/toString`，约 40 行。
新写法一行 `record Trade(int index, String ticker, long price, long volume)`，加紧凑构造器放校验。本题里 `Trade`、`TickerTotal`、`Summary`、`Fill`、`Tick`、`Ask`、`Answer` 都是 record。
**什么时候不该用**：需要可变字段（比如 `Acc`，每次成交都要改它）、或需要继承别的类时。

### sealed 接口 + 模式匹配 switch + 记录模式

`Feed permits Fill, Tick, Ask`。旧写法是 `if (f instanceof Fill) { Fill x = (Fill) f; ... } else if ... else throw new IllegalStateException()`——强转、重复、编译器不检查是否漏了某种情况。
新写法 `switch (f) { case Fill fill -> ...; case Tick(var t) -> ...; case Ask(var t) -> ... }`：编译器检查穷尽性，`case Tick(var t)` 同时完成类型判断和字段解构，`when` 守卫写附加条件。

### Sequenced Collections

`worstFirst.reversed()` 取倒序视图；`ArrayDeque.peekFirst / removeFirst / addLast`；用 `getFirst() / getLast()` 取列表两端。旧写法 `list.get(list.size() - 1)`、`Collections.reverse(copy)` 要么啰嗦要么要复制。注意 `reversed()` 是**视图**，改原列表它也跟着变；要独立副本就 `List.copyOf`。

### Stream 新工具：`toList()` 与 `Collectors.teeing`

`stream.toList()`（Java 16）返回不可变列表，比 `collect(Collectors.toList())` 短、且明确不可变。`teeing`（Java 12）一趟遍历喂给两个收集器。
**什么时候不该用**：热路径上的简单聚合手写循环更快（`IntStream.boxed()` 装箱）；`teeing` 的两个收集器如果有顺序依赖就别用。

### 精确算术

`Math.multiplyExact / addExact`（Java 8 引入，JDK 21 里已成惯用）：溢出就抛，不静默回绕。旧写法是 `long r = a * b; if (a != 0 && r / a != b) throw ...`，要多一次除法还容易写错。

### Comparator 组合子

`comparingLong(...).reversed().thenComparing(...).thenComparingInt(...)`：一条链写出全序，对照 Java 7 的匿名内部类 `compare` 里一串 `if`。

### 虚拟线程与结构化并发（预览）

`Thread.ofVirtual().factory()` + `StructuredTaskScope.ShutdownOnFailure`：旧写法 `ExecutorService` + `Future` 列表，一个失败其余不会取消，忘了 `shutdown` 线程泄漏；新写法生命周期绑定到 try 块。**不该用**：CPU 密集的分块任务其实用虚拟线程并不比平台线程快（虚拟线程擅长的是**阻塞 I/O**），这里选它是为了展示结构化并发的取消语义。

### 并发原语：`ConcurrentHashMap.merge`

共享 Map 对照组用到的原子 `merge`。

---

## 7. 追问预演

**问：为什么求最大的 k 个要用最小堆？**
* 思考：堆顶是「最容易被替换」的元素。要替换的是「k 个里最差的」，所以堆顶必须是最差的，也就是最小堆。
* 答：保留集合是「目前最好的 k 个」，每来一个新元素只需要知道「保留集合里最差的是谁」，最小堆 O(1) 给出，O(log k) 替换。如果用最大堆装全部元素也能做（heapify O(n) 然后弹 k 次，O(n + k log n)），但要 O(n) 空间且不能流式。
* 说出口：「最大的 k 个用最小堆，堆顶是守门员；新来的比守门员强才能进来。时间 O(n log k)，空间 O(k)，还可以流式处理。」

**问：如果 n 很大、k 很小，还能更快吗？**
* 答：随机顺序下，堆满之后期望只有 O(k log(n/k)) 个元素能进堆——绝大多数元素一次 `long` 比较就被拒绝，实际上接近 O(n)。可以用快速拒绝去掉分配。再快就是 quickselect（期望 O(n) 选出第 k 大，但需要把数据放进可修改的数组，不能流式）或并行分块各自 top-k 再合并（top-k 的合并是对的：全局 top-k 一定在各块 top-k 的并集里）。
* 说出口：「堆满后一次 long 比较拒绝，零分配；要更快就分块并行，各块 top-k，再对 C·k 个候选取 top-k。」

**问：notional 溢出怎么办？为什么不用 `double` / `BigInteger`？**
* 答：价格数量都是 `long`，乘积可能超过 2⁶³，用 `Math.multiplyExact` 溢出就抛，不给错答案。`double` 有 53 位尾数，大数会丢精度、累加不满足结合律（并行结果不稳定）。`BigInteger` 能放下任何数，但每次运算分配对象，慢几十倍；只有业务上必须容纳「溢出后的大数」才用，并且应该只用在检测到溢出的慢路径。
* 说出口：「金额用整数最小单位加精确算术，溢出抛异常；如果业务必须处理巨大数值，慢路径再退回 BigInteger。」

**问：Part 3，为什么不用堆？用堆能不能做？**
* 答：见 4.3 节。堆没有 decrease-key，也不能高效删除任意元素；可以用惰性删除（再插一条新的，弹出时丢弃过期条目），但堆里垃圾可以累积到 O(事件数)，`top-k` 查询要弹 k 个有效条目再放回去；`TreeSet` 每个操作有 O(log m) 上界。
* 说出口：「堆只能高效取堆顶；这里一个 ticker 的总额既涨又跌，要改任意元素的键，所以用 `TreeSet`：删旧键、插新键各 O(log m)，top-k 直接顺序读前 k 个。」

**问：窗口很大、不同 ticker 非常多，`TreeSet` 常数太大怎么办？**
* 答：几个方向：(1) k 很小时可以只维护「候选集」（top-k 以及一个缓冲区），用堆加惰性删除；(2) 总额用 `long[]` 按 ticker 编号存（先把 ticker 映射成 int），`TreeSet` 里放 `long` 编码（总额高位 + 编号低位）减少对象；(3) 分片：按 ticker 哈希到 S 个分片，每片一个 `TreeSet`，`top()` 做 S 路的 k 路归并（即把 S 个有序序列归并成一个有序序列）。
* 说出口：「先量。如果确实是瓶颈：把 ticker 映射成整数、结构放进原始类型数组，或者按 ticker 分片后做 k 路归并。」

**问：Part 4，`parallel()` 流为什么有时候更慢？**
* 答：5.6 节。(1) 事件太少，调度开销超过收益；(2) 合并是串行的，不同 key 越多合并越贵；(3) 公共线程池是 JVM 共享的，别的并行流或 `CompletableFuture` 会抢；(4) 内存带宽是上限。
* 说出口：「并行流不是免费的午餐。我会先测顺序版，然后在真实数据上测各种分块；key 很多时合并成了瓶颈，考虑按 key 分区或共享并发 map。」

**问：怎么保证并行结果和顺序版完全一样？**
* 答：三点：整数加法的结合律/交换律；每块私有的 `Map` + 只读的输入；排序的 tie-break 是全序（top-k 的结果不依赖遍历顺序）。验证做法：随机打乱事件顺序、变化块数，断言结果 `Map.equals`；重复多轮，并用起跑门闩（`CountDownLatch`）让多个线程同时开始。

**问：一块失败了，其余怎么办？线程会不会泄漏？**
* 答：`StructuredTaskScope.ShutdownOnFailure`：第一个失败后关闭 scope、中断其余；try 块结束前所有子线程一定结束。中断是协作式的，所以计算循环里要定期检查 `isInterrupted()`。如果用 `ExecutorService` + `Future.get()`，一个失败不会取消其他，要手动 `cancel(true)`，且要保证 `shutdown`。

**问：输入有 100 亿条放不进内存？**
* 答：流式读取，分块；按 `hash(ticker) % S` 分片写盘（同一 ticker 一定在同一片），每片内存聚合后 top-k，最后合并 S 个 top-k（因为 ticker 不跨片，全局 top-k 一定在各片 top-k 的并集里）。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| top-k 最大值用最大堆装全部再弹 k 次 | O(n) 空间，不能流式，n log n 级别 | 大小为 k 的**最小**堆 |
| 比较器只写 `notional` 降序 | 平局顺序未定义，结果不可复现，并行后更乱 | 三级全序：notional、ticker、index |
| `comparing(A).thenComparing(B).reversed()` | B 也被反转了 | `comparing(A).reversed().thenComparing(B)` |
| 快速拒绝写成 `notional <= 堆顶` | 平局时 ticker 更小的好事件被误拒 | 严格 `<` |
| `long notional = price * volume;` | 溢出静默绕回，天价成交排最后 | `Math.multiplyExact` |
| 只对进堆的事件做溢出检查 | 检测与数据排列有关 | 每个事件都校验 |
| 用 `double` 存金额并行累加 | 浮点不满足结合律，结果每次不同 | 整数 tick |
| `TreeSet` 的比较器只看总额 | 总额相同的 ticker 被当作同一元素吞掉 | 比较器里带上 ticker（身份） |
| 先改 `acc.total` 再 `ranking.remove(旧键)` | 找不到旧键，树里残留脏数据 | 先按**旧**值删，再改，再按新值插 |
| 溢出检查放在改状态之后 | 抛异常时状态已被破坏 | 先算 `addExact`，成功再改 |
| combiner 写成把 left 并进 right | `BiConsumer` 只能改第一个参数，left 的内容丢了 | `(left, right) -> right.forEach(... left.merge ...)` |
| supplier 返回共享对象 | 数据竞争 | 每次 `new` 一个新容器 |
| 取消时不检查中断标志 | 中断只是个标志，线程仍然算到底 | 循环里定期 `isInterrupted()` |
| `n * c / chunks` 用 `int` | `n * c` 溢出 | 先转 `long` |

---

## 9. 自测题

1. `k = 3`，流 `[4, 8, 1, 9, 2, 7]`，用「大小为 3 的最小堆」手工走一遍，写出每一步堆的内容。
2. 为什么 `BEST_FIRST` 的第三级用 `index` 一定能分出胜负？如果去掉第三级，什么会变得不稳定？
3. 窗口 `W = 10`，一笔成交在 `t = 100`，在 `now = 109` 和 `now = 110` 时它是否还活着？
4. `Long.MAX_VALUE / 2 + 1` 同一个 ticker 出现两次，用 `Math::addExact` 聚合会怎样？如果分到两块里各算一次再合并呢？
5. （小编程）写一个 `Comparator<TickerTotal>`：总额降序，总额相同按 ticker 升序，不用 `reversed()`。
6. （思考）把价格改成可以为负（比如表示卖出）。Part 4 里「溢出结果与分块无关」的论证哪一步失效？

<details><summary>答案</summary>

1. `[4]` → `[4,8]` → `[1,4,8]`（满，守门员 1）→ 9 > 1：`[4,8,9]` → 2 < 4：不变 → 7 > 4：`[7,8,9]`。结果从大到小 9, 8, 7。
2. `index` 是数组下标，全局唯一，任何两个不同事件的 `index` 不同。去掉后「notional 与 ticker 都相同」的事件顺序由堆的内部实现决定（比如样例的下标 1 与 4），结果会因 JDK 版本、输入顺序而不稳定。
3. `now = 109`：`109 - 100 = 9 < 10`，活着；`now = 110`：`110 - 100 = 10 >= 10`，过期。
4. 顺序聚合：第二次 `addExact` 抛 `ArithmeticException`。分到两块：每块的部分和 `MAX/2+1` 不溢出，**合并时**才溢出——`mergeInto` 里的 `merge(…, Math::addExact)` 抛出。结果一致：都抛。
5. `(a, b) -> { int c = Long.compare(b.notional(), a.notional()); return c != 0 ? c : a.ticker().compareTo(b.ticker()); }`。注意 `Long.compare(b, a)` 而不是 `b - a`（后者在极端值会溢出）。
6. 「所有 notional 非负 ⇒ 部分和单调不减 ⇒ 任意部分和 ≤ 总和」失效：有负数时，某个顺序下中间和可能先超过 `Long.MAX_VALUE` 再被负数拉回来。此时某些分块方式抛异常、另一些不抛，结果依赖于分块——要么禁止负数，要么用 `BigInteger` / 更宽的累加器（`Math.multiplyHigh` 做 128 位累加）。

</details>

---

「延伸」Sedgewick《算法》第 2.4 节「优先队列」。
