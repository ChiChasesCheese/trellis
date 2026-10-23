---
id: hl-hc11-sweep-vs-segtree
node: problems.hc11-order-interval-overlap
type: qa
step: 12
---
## Q
只要全局最大重叠时，扫描线和线段树哪个更好？线段树什么时候才值得用？

## A
扫描线答「全局最大」是最优的：30 万个 10¹⁸ 量级的区间，扫描线只要约 21 ms，建线段树索引约 100 ms（10 万次 `maxIn` 约 27 ms）。

线段树值得用于：
1. **更新顺序任意**：先撤后加、`add` 与 `remove` 交错，扫描线必须一次读完；
2. **区间查询**「`[from, to)` 内最大重叠」，线段树 O(log n)；
3. 在线反复查询。
并且先做坐标压缩。构造 O(m log m)，每次 `add/remove/liveAt/maxIn` O(log m)，m ≤ 2n。

`IntervalIndex.max()` 全局最大；`of(long[][])` / `maxOverlap(long[][])` 用压缩 + 线段树算 Part 1，必须与扫描线一致。要求：坐标接近 `Long.MAX_VALUE` 不能溢出（二分、比较都不做减法）；30 万个 10¹⁸ 量级区间 + 10 万次 `maxIn` < 2 s。

堆 vs 两数组：堆（Meeting Rooms II）可行；两数组不分配对象、tie 规则直观、容易扩展到方向和撤单。

线段树 vs Fenwick：求和用 Fenwick；区间加 + 区间最大必须线段树。

这个问题的 Java 特性：record + 紧凑构造器（`Peak/Place/Cancel/Report/Order`，`Place` 的紧凑构造器让 `end < start` 构造不出来；`Lane` 频繁改字段所以是普通类）；sealed `OrderEvent`；模式匹配 switch + 记录模式；`switch` 表达式与 `yield`：`Lane lane = switch (p.side()) { case BUY -> buy; case SELL -> sell; };`；`TreeMap` 是 `SequencedMap`/`NavigableMap` 的 `firstEntry/pollFirstEntry/floorEntry`；`_` 未命名模式（预览）。

C++：`std::variant + std::visit(overloaded{...})`；`std::sort` 比较器写成 `<=` 不是严格弱序，是 UB（有很多相等元素时可能越界），要用 `<`；`span<const Interval>` 只读视图不会是 null。
