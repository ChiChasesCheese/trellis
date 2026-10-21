# hc09 · 思路与追问

## 概要

「订单簿 / 交易事件处理」是这类面试里的典型题型。这题最容易开口：十分钟写完 Part 1；真正考的是追问——tie-break 写没写全、溢出、流式（堆为什么不够）、多核结果一致。

## 逐 Part 思路

1. **topEvents**：大小 k 的最小堆，堆顶是保留集合里最差的「守门员」（比较器 `BEST_FIRST.reversed()`）。每个事件先 `notionalAt(i)`（校验 + `multiplyExact`），堆满后用 `notional < 堆顶`（严格小于）做零分配快速拒绝，之后才建 `Trade`。排序键 (notional 降, ticker 升, index 升) 是全序。输出 poll 后 `ArrayList.reversed()` + `List.copyOf`。`topEventsSorted` 是 O(n log n) 基线。
2. **topTickers / topOf / topTickersStream / summarize**：`HashMap.merge(…, Math::addExact)` O(n)，再对 m 个 ticker 用同样的堆取 top-k（`topOf`，Part 4 复用）。Stream 版 `groupingBy` + `reducing`；`summarize` 用 `Collectors.teeing` 一趟算总额和最大事件。
3. **SlidingTopK**：`ArrayDeque<Fill>`（FIFO 过期）+ `HashMap<String, Acc>`（总额 + 活跃笔数）+ `TreeSet<TickerTotal>`（排名）。add：先推进时钟，先算 `addExact`（溢出就抛，未动结构），再删旧键 → 改总额 → 插新键。过期条件 `now - time >= window`（防溢出）。replay 用 sealed `Feed` + record 模式 switch。
4. **ParallelNotional**：parallel 流三参数 collect、`RecursiveTask`、`StructuredTaskScope.ShutdownOnFailure` + 虚拟线程、共享 `ConcurrentHashMap`（对照）。前三种都是「每块私有 HashMap + mergeInto」。合并为什么正确：整数加法满足结合律、交换律；没有共享可变状态；notional 非负 ⇒ 部分和单调 ⇒ 是否溢出与分块方式无关。`accumulate` 每 4096 个事件检查一次中断标志，取消才真正生效。

## 隐藏测试会打的坑

tie-break 只写 notional；快速拒绝写成 `<=`；`p*v` 不检查（`MAX*2` 绕回 -2；3037000499² 不溢出、3037000500² 必须报错）；只对进堆的事件做校验；`reversed()` 位置放错；聚合溢出（两个 `MAX/2+1`）；零 notional 的 ticker 丢失；窗口边界差一；总额溢出后状态损坏；`TreeSet` 比较器只看总额，吞掉同额 ticker；先改 total 后删旧键；combiner 方向反了；supplier 共享同一个 Map；`n*c` 溢出 int；合并时才溢出；失败后不取消其余块。

## 复杂度

12 核，噪声大，只看数量级。

* Part 1，n=1e6、k=100、随机：堆 O(n log k) 2–14 ms；排序基线约 220 ms；k=1000、严格递增（每个都进堆）约 120 ms。
* Part 2，n=1e6、m=1e5、k=50：HashMap + 堆 41–58 ms；Stream 82–103 ms。
* Part 3，1e6 笔成交 + 1e4 次查询，窗口 5000，m=2000：约 430–480 ms。
* Part 4，2e6 事件 / 5e4 ticker：顺序约 45 ms，各并行变体 20–110 ms（几乎没有加速）；2e7 / 200 ticker：顺序 210–330 ms，parallel 流 75–110 ms，共享 Map 300–350 ms；2e7 / 2e6 ticker：顺序 2.4–4.2 s，共享 Map 0.8–0.9 s 最快（合并成了瓶颈）。

## Java 21 特性

| 特性 | 用在哪 |
|---|---|
| record + 紧凑构造器 | `Trade` 构造器里 `multiplyExact`，保证 `notional()` 不溢出 |
| sealed | `Feed` |
| 模式匹配 switch + record 模式 + `when` 守卫 | replay |
| `var` | 局部变量 |
| Sequenced Collections | `reversed()` / `peekFirst` / `removeFirst` / `getFirst` / `getLast` |
| Stream API | `groupingBy` + `reducing`、`teeing`、`toList` |
| 数学工具 | `multiplyExact` / `addExact`、`formatted` |
| Comparator 组合子 | 多级 tie-break 排序 |
| 虚拟线程 / `StructuredTaskScope`（预览） | 并行分块聚合 |
| 并发工具 | `ConcurrentHashMap.merge`、`CountDownLatch` |
| 文本块 | 多行输入脚本 |

## 面试官可能的追问

1. **为什么取最大 k 个用最小堆？** 堆顶是守门员；O(n log k) 时间、O(k) 空间、可以流式处理。
2. **溢出怎么办？** `multiplyExact` / `addExact` 抛 `ArithmeticException`，每个事件都检查；`double` 只有 53 位精度且累加不满足结合律；`BigInteger` 只作慢路径。
3. **（Part 3）为什么不用堆？** 一个 ticker 的总额既会涨也会跌，要改任意元素的键；`PriorityQueue` 没有 decrease-key，`remove(Object)` 是 O(m)；惰性删除会累积垃圾；`TreeSet` 删旧键 / 插新键各 O(log m)。
4. **（Part 3）ticker 很多时 TreeSet 太慢？** 先测量；ticker → int 编号 + 原始数组；分片后 k 路归并；惰性堆 + 缓冲。
5. **（Part 4）合并为什么是对的？** 结合律 / 交换律；每块私有 Map、输入只读；非负 ⇒ 溢出与分块无关（允许负数就不成立）。
6. **（Part 4）为什么 parallel() 有时更慢？** 事件太少；key 多时串行合并成为瓶颈（Amdahl 定律）；公共 ForkJoin 池被共享；内存带宽。
7. **一块失败了其余怎么办？** `ShutdownOnFailure` 关闭 scope 并中断其余任务，但取消是协作式的，任务里要检查 `isInterrupted`；`ExecutorService` + `Future` 不会自动取消。
8. **100 亿条放不下？** 按 `hash(ticker) % S` 分片，各片聚合取 top-k，再合并 S 个 top-k。
