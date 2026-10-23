---
id: hl-hc11-coord-compress
node: problems.hc11-order-interval-overlap
type: qa
step: 11
---
## Q
坐标压缩（coordinate compression）怎么做？订单 `[10,50)`、`[20,60)`、`[40,80)` 映射到哪些基本段？

## A
时间戳可能 10¹⁸，线段树开不出数组；但 n 张订单只有 2n 个**端点**，活跃数只在端点变化，相邻端点之间所有时刻活跃数相同，只关心端点。把很大或稀疏的坐标映射成**保持大小顺序**的小整数下标。

做法：端点排序去重得 `c[0] < … < c[m−1]`（不去重会出现长度为 0 的基本段）；相邻两端点之间 `[c[j], c[j+1])` 是**基本段**，共 m−1 个，每段活跃数为常数。`[s, e)` 恰好覆盖基本段 **`idx(s)` 到 `idx(e)−1`**（`idx(x)` 是 x 在 c 里的下标，二分查找）；误写成 `idx(s)..idx(e)` 会多算 e 所在的段。

例：端点 `c = [10, 20, 40, 50, 60, 80]`，基本段 seg0=[10,20)、seg1=[20,40)、seg2=[40,50)、seg3=[50,60)、seg4=[60,80)。`[10,50)` → seg0..seg2；`[20,60)` → seg1..seg3；`[40,80)` → seg2..seg4。活跃数 1,2,3,2,1，最大 3（seg2）。另一例：`[10, 50, 20, 50, 80]` 排序去重 `[10,20,50,80]`（3 个基本段），`[20,80)` 覆盖 `idx(20)=1..idx(80)-1=2`，即后两段。

`IntervalIndex(long[] coordinates)`：先告知所有会用到的端点（任意顺序、可重复），之后 `add(start, end)` / `remove(start, end)` 两端必须是已知端点否则 `IllegalArgumentException`；`end < start` → IAE；`start == end` 什么都不做。
```java
public void add(long start, long end) {
    int lo = exactIndex(start), hi = exactIndex(end);   // 二分，未知端点抛 IAE
    if (lo == hi) return;
    rangeAdd(1, 0, size - 1, lo, hi - 1, +1);
}
```
`liveAt(t)`：`j = floorIndex(t)`；t 比所有端点小或 `j >= segs`（≥ 最右端点，右端不含）→ 0；否则 `rangeMax(j, j)`。`maxIn(from, to)`：`lo = max(0, floorIndex(from))`，`hi = min(segs−1, lowerBound(to) − 1)`，伸出端点之外的部分活跃数为 0，结果 `max(0, rangeMax(lo, hi))`；`to < from` → IAE，`to == from` → 0。

事先不知道所有坐标：只能离线压缩；在线且坐标未知 → 动态开点线段树（值域 [0, 2⁶⁰)，只在用到时建结点，内存 O(n log C)，深度 60），或自写 order-statistic 平衡树。
