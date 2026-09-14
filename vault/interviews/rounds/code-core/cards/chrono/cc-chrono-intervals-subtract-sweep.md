---
id: cc-chrono-intervals-subtract-sweep
node: chrono.intervals
type: qa
---
## Q
You are given `allowed` intervals and `freeze` intervals; freeze wins. Produce the effective allowed set without pairwise subtraction.

## A
**A boundary sweep.** Turn every endpoint into an event, sort once, and carry one counter per set.

```python
ev = [(s, +1, 0) for s, e in allowed] + [(e, -1, 0) for s, e in allowed] \
   + [(s, 0, +1) for s, e in freeze]  + [(e, 0, -1) for s, e in freeze]
ev.sort()
```

Walk in coordinate order maintaining `n_allowed` and `n_freeze`; a segment is emitted while `n_allowed > 0 and n_freeze == 0`.

- Process **all** events sharing a coordinate before deciding, or a freeze ending exactly where another begins opens a zero-length hole.
- Merge adjacent emitted segments at the end — the sweep naturally splits at every boundary, including ones where nothing changed.
- O((n+m) log(n+m)). Pairwise subtraction is O(n·m) and yields fragments you have to re-merge anyway.
- The same sweep with `+1/−1` on one set only counts overlaps ("how many are busy at t"), which is the difference-array idea on sparse coordinates ([[cc-algorithms-prefix-difference-array]]).

## Q zh
给定 `allowed` 区间和 `freeze` 区间，freeze 优先。不做两两相减，求出实际可用集合。

## A zh
**边界扫描线。** 把每个端点变成事件，排序一次，每个集合各带一个计数器。

```python
ev = [(s, +1, 0) for s, e in allowed] + [(e, -1, 0) for s, e in allowed] \
   + [(s, 0, +1) for s, e in freeze]  + [(e, 0, -1) for s, e in freeze]
ev.sort()
```

按坐标顺序遍历，维护 `n_allowed` 与 `n_freeze`；当 `n_allowed > 0 and n_freeze == 0` 时输出该段。

- 在做判断前先处理完**同一坐标上的所有**事件，否则一个恰好结束在另一个开始处的 freeze 会开出一个零长度空洞。
- 最后再合并相邻的输出段 —— 扫描线天然会在每个边界处切开，包括什么都没变的边界。
- O((n+m) log(n+m))。两两相减是 O(n·m)，而且产生的碎片你还得重新合并。
- 同样的扫描只对一个集合做 `+1/−1` 就是统计重叠数（「t 时刻有多少在忙」），也就是稀疏坐标上的差分数组思路（[[cc-algorithms-prefix-difference-array]]）。
